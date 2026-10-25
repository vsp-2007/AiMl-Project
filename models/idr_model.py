import math
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Dict, Any, Optional

class TemporalConvBlock(nn.Module):
    """Temporal 1D Convolutional feature extractor with residual connection."""
    def __init__(self, in_channels: int, out_channels: int, kernel_size: int = 5):
        super().__init__()
        padding = kernel_size // 2
        self.conv1 = nn.Conv1d(in_channels, out_channels, kernel_size, padding=padding)
        self.bn1 = nn.BatchNorm1d(out_channels)
        self.conv2 = nn.Conv1d(out_channels, out_channels, kernel_size, padding=padding)
        self.bn2 = nn.BatchNorm1d(out_channels)
        self.leaky = nn.LeakyReLU(0.1, inplace=True)
        
        self.residual = (
            nn.Conv1d(in_channels, out_channels, 1)
            if in_channels != out_channels
            else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        res = self.residual(x)
        out = self.leaky(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return self.leaky(out + res)

class IntelligentDeadReckoningNet(nn.Module):
    """
    Hybrid 1D-CNN + GRU Deep Neural Network for Intelligent Dead Reckoning.
    Processes sequential 6-DOF IMU windows (Accel: X,Y,Z | Gyro: X,Y,Z).
    
    Predicts:
    1. Forward Vehicle Speed (m/s) + predicted log-variance (uncertainty)
    2. Heading Angular Rate (rad/s) + predicted log-variance (uncertainty)
    """

    def __init__(
        self,
        in_channels: int = 6,
        conv_channels: int = 64,
        gru_hidden_size: int = 64,
        gru_layers: int = 2,
        dropout: float = 0.15
    ):
        super().__init__()
        self.in_channels = in_channels
        self.gru_hidden_size = gru_hidden_size

        # Temporal Feature Extraction
        self.conv_block1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv_block2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        # Recurrent Core for sequential temporal dependency
        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=gru_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if gru_layers > 1 else 0.0
        )

        gru_out_dim = gru_hidden_size * 2

        # Velocity prediction head: outputs [mean_velocity, log_var_velocity]
        self.vel_head = nn.Sequential(
            nn.Linear(gru_out_dim, 64),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout),
            nn.Linear(64, 2)
        )

        # Yaw rate prediction head: outputs [mean_yaw_rate, log_var_yaw_rate]
        self.yaw_head = nn.Sequential(
            nn.Linear(gru_out_dim, 64),
            nn.LeakyReLU(0.1),
            nn.Dropout(dropout),
            nn.Linear(64, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Args:
            x: Tensor of shape (Batch, SeqLen, InChannels) or (Batch, InChannels, SeqLen)
        Returns:
            vel_mean: (Batch,) forward velocity in m/s
            vel_var:  (Batch,) predicted variance in (m/s)^2
            yaw_mean: (Batch,) yaw angular rate in rad/s
            yaw_var:  (Batch,) predicted variance in (rad/s)^2
        """
        if x.dim() == 2:
            x = x.unsqueeze(0)
        # Ensure channel-first for 1D convolutions: (Batch, Channels, SeqLen)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        # CNN Feature Extraction
        feat = self.conv_block1(x)
        feat = self.pool1(feat)
        feat = self.conv_block2(feat)
        feat = self.pool2(feat)

        # Reshape for GRU: (Batch, SeqLen_reduced, FeatureDim)
        feat = feat.transpose(1, 2)

        # GRU Sequence Processing
        gru_out, _ = self.gru(feat)

        # Pool over sequence length: use the final step representation
        last_step = gru_out[:, -1, :]

        # Velocity prediction
        vel_raw = self.vel_head(last_step)
        # Vehicle forward velocity is non-negative
        vel_mean = F.softplus(vel_raw[:, 0])
        vel_logvar = torch.clamp(vel_raw[:, 1], min=-6.0, max=4.0)
        vel_var = torch.exp(vel_logvar)

        # Yaw rate prediction
        yaw_raw = self.yaw_head(last_step)
        yaw_mean = yaw_raw[:, 0]
        yaw_logvar = torch.clamp(yaw_raw[:, 1], min=-8.0, max=2.0)
        yaw_var = torch.exp(yaw_logvar)

        return vel_mean, vel_var, yaw_mean, yaw_var

class VelocityNet(nn.Module):
    """
    Dedicated Model 1: Forward Velocity Specialist.
    Processes ONLY 3-axis Accelerations (ax, ay, az).
    Completely isolated from gyroscopes to prevent rotation/bias cross-talk.
    """
    def __init__(self, in_channels: int = 3, conv_channels: int = 32, gru_hidden_size: int = 32, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.conv1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=1,
            batch_first=True
        )
        self.head = nn.Sequential(
            nn.Linear(gru_hidden_size, 32),
            nn.LeakyReLU(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        feat = self.conv1(x)
        feat = self.pool1(feat)
        feat = self.conv2(feat)
        feat = self.pool2(feat).transpose(1, 2)

        out, _ = self.gru(feat)
        raw = self.head(out[:, -1, :])
        vel_mean = F.softplus(raw[:, 0])
        vel_logvar = torch.clamp(raw[:, 1], min=-6.0, max=4.0)
        vel_var = torch.exp(vel_logvar)
        return vel_mean, vel_var


class YawRateNet(nn.Module):
    """
    Dedicated Model 2: Heading & Yaw Rate Specialist.
    Processes ONLY 3-axis Gyroscopes (gx, gy, gz).
    Completely isolated from accelerometers so smartphone tilt and road bumps
    CANNOT induce false turns or phantom circular loops!
    """
    def __init__(self, in_channels: int = 3, conv_channels: int = 32, gru_hidden_size: int = 32, dropout: float = 0.1):
        super().__init__()
        self.in_channels = in_channels
        self.conv1 = TemporalConvBlock(in_channels, conv_channels, kernel_size=5)
        self.pool1 = nn.MaxPool1d(2)
        self.conv2 = TemporalConvBlock(conv_channels, conv_channels * 2, kernel_size=3)
        self.pool2 = nn.MaxPool1d(2)

        self.gru = nn.GRU(
            input_size=conv_channels * 2,
            hidden_size=gru_hidden_size,
            num_layers=1,
            batch_first=True
        )
        self.head = nn.Sequential(
            nn.Linear(gru_hidden_size, 32),
            nn.LeakyReLU(0.1),
            nn.Linear(32, 2)
        )

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.shape[-1] == self.in_channels:
            x = x.transpose(1, 2)

        feat = self.conv1(x)
        feat = self.pool1(feat)
        feat = self.conv2(feat)
        feat = self.pool2(feat).transpose(1, 2)

        out, _ = self.gru(feat)
        raw = self.head(out[:, -1, :])
        yaw_mean = raw[:, 0]
        yaw_logvar = torch.clamp(raw[:, 1], min=-8.0, max=2.0)
        yaw_var = torch.exp(yaw_logvar)
        return yaw_mean, yaw_var


class DecoupledDualModelIDR(nn.Module):
    """
    Dual-Model Decoupled Dead Reckoning System.
    Combines Model 1 (VelocityNet) and Model 2 (YawRateNet) as independent experts.
    Completely prevents gradient interference and cross-axis false turns.
    """
    def __init__(self):
        super().__init__()
        self.vel_model = VelocityNet(in_channels=3)
        self.yaw_model = YawRateNet(in_channels=3)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        # Check channel format
        if x.shape[-1] == 6:
            accel = x[:, :, 0:3]
            gyro = x[:, :, 3:6]
        else:
            accel = x[:, 0:3, :]
            gyro = x[:, 3:6, :]

        vel_mean, vel_var = self.vel_model(accel)
        yaw_mean, yaw_var = self.yaw_model(gyro)
        return vel_mean, vel_var, yaw_mean, yaw_var


class HeteroscedasticLoss(nn.Module):
    """
    Gaussian Negative Log-Likelihood Loss for predicting mean and variance.
    Trains the network to express its own epistemic/aleatoric uncertainty.
    """
    def __init__(self, eps: float = 1e-6):
        super().__init__()
        self.eps = eps

    def forward(self, pred_mean: torch.Tensor, pred_var: torch.Tensor, target: torch.Tensor) -> torch.Tensor:
        # NLL = 0.5 * (log(var) + (target - mean)^2 / var)
        target = target.view_as(pred_mean)
        pred_var = pred_var.view_as(pred_mean)
        log_var = torch.log(pred_var + self.eps)
        precision = 1.0 / (pred_var + self.eps)
        loss = 0.5 * (log_var + precision * ((target - pred_mean) ** 2))
        return torch.mean(loss)
