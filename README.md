# AI-ML Based Intelligent Dead Reckoning System (SIH26168)
### ISRO / Smart Vehicles Category

An edge-optimized Intelligent Dead Reckoning (IDR) and Sensor Fusion Engine designed for seamless navigation during GNSS outages (tunnels, dense urban canyons, and underpasses).

---

## 🌟 Key Highlights & Engineering Features

1. **Hybrid 1D-CNN + BiGRU Deep Learning Architecture**
   - Ingests high-frequency 6-DOF IMU windows (3-axis accelerometer + 3-axis gyroscope).
   - Isolates vehicle chassis kinematics from high-frequency road vibrations, bumps, and sensor noise.
   - Dual-head heteroscedastic regression: predicts both forward vehicle velocity ($v$) and heading angular rate ($\omega$) alongside aleatoric predictive uncertainties ($\sigma_v^2, \sigma_\omega^2$).

2. **Runtime Self-Correction & Online Drift Adaptation**
   - While driving under active GNSS (clear skies), the model runs continuously in the background.
   - Compares ML predictions against high-precision GNSS velocity vectors in real time.
   - Uses Online Gradient Descent (OGD) with L2 weight anchoring to learn device-specific hardware bias drift, phone mounting pitch tilt, and scale factors.
   - Executes Zero-Velocity Updates (ZUPT) and Zero-Angular-Rate Updates (ZARU) at traffic lights to lock gyroscope zero-bias.
   - Persists learned device profiles (`device_drift_profile.json`) across sessions.

3. **Intelligent Extended Kalman Filter (EKF) Sensor Fusion**
   - Operates in local metric Tangent Plane (ENU) with ellipsoidal Bowring WGS84 geodetic transformations.
   - Fuses GNSS when locked, continually estimating sensor biases.
   - During GNSS loss (e.g. 50s-100s tunnel), smoothly relies on ML predictions + online-calibrated corrections with zero trajectory jumps.

4. **Hardware Acceleration (NVIDIA GeForce RTX 5050 Laptop GPU)**
   - PyTorch CUDA acceleration enabled for rapid multi-trajectory training and batched temporal convolutions.
   - ONNX Runtime and TFLite ready for ultra-low latency (<2ms) mobile edge inference.

5. **Full-Featured Real-Time Backend & Web Dashboard**
   - FastAPI + WebSocket backend streaming at 50Hz.
   - Interactive Leaflet.js dashboard with live side-by-side comparison:
     - 🔵 **Blue Path**: Ground Truth / GNSS reference
     - 🟢 **Green Path**: AI-ML Intelligent DR + EKF (stays locked on track during tunnels)
     - 🔴 **Red Dashed Path**: Naive IMU baseline (rapidly drifts off-road due to raw smartphone noise)

---

## 📁 Repository Structure

```text
├── models/
│   ├── idr_model.py          # 1D-CNN + BiGRU PyTorch architecture with heteroscedastic loss
│   ├── online_calibrator.py  # Runtime self-correction & online drift adaptation engine
│   ├── train.py              # GPU-accelerated training pipeline & ONNX edge export
│   └── __init__.py
├── sensor_fusion/
│   ├── coordinates.py        # WGS84 Geodetic to Local Tangent Plane (ENU) Bowring transformer
│   ├── ekf.py                # Intelligent EKF with dual GNSS/ML updates & ZUPT
│   └── __init__.py
├── simulation/
│   ├── dataset_generator.py  # Realistic multi-maneuver drive & smartphone IMU noise generator
│   └── __init__.py
├── backend/
│   ├── main.py               # FastAPI backend with REST and WebSocket streaming
│   ├── schemas.py            # Pydantic telemetry models
│   ├── dashboard.html        # Interactive Leaflet live map HUD
│   └── __init__.py
├── data/
│   ├── iovnbd_loader.py      # IO-VNBD 29-col VBOX & 24-col Smartphone parser & sliding-window loader
│   ├── iovnbd_samples/       # Real-schema benchmark drives (V-Drive_Sample1.csv, S-Drive_Sample1.csv)
│   └── __init__.py
├── models/
│   ├── idr_model.py          # 1D-CNN + BiGRU PyTorch architecture with heteroscedastic loss
│   ├── online_calibrator.py  # Runtime self-correction & online drift adaptation engine
│   ├── train.py              # GPU-accelerated training pipeline (IO-VNBD / Hybrid / Synthetic)
│   └── __init__.py
├── sensor_fusion/
│   ├── coordinates.py        # WGS84 Geodetic to Local Tangent Plane (ENU) Bowring transformer
│   ├── ekf.py                # Intelligent EKF with dual GNSS/ML updates & ZUPT
│   └── __init__.py
├── simulation/
│   ├── dataset_generator.py  # Realistic multi-maneuver drive & smartphone IMU noise generator
│   ├── iovnbd_loader.py      # Lateral re-export of IO-VNBD data loader
│   └── __init__.py
├── tests/
│   ├── test_iovnbd.py        # Comprehensive IO-VNBD schema, resampling, dataset, and benchmark tests
│   ├── test_coordinates.py   # WGS84 <-> ENU precision roundtrip tests
│   ├── test_ekf.py           # EKF prediction, GNSS update, and ML update tests
│   ├── test_online_calibrator.py # Self-correction and adaptation convergence tests
│   ├── test_simulation.py    # Multi-maneuver synthetic dataset generator tests
│   └── test_backend.py       # FastAPI REST endpoints integration tests
├── benchmark_iovnbd.py       # GNSS outage drift evaluation suite & comparative ASCII reporting
├── run_backend.py            # Uvicorn server launcher
└── README.md
```

---

## 🚗 IO-VNBD Benchmark Dataset Integration

This project natively integrates the **IO-VNBD** (*Inertial and Odometry Vehicle Navigation Benchmark Dataset* - Coventry University: https://github.com/onyekpeu/IO-VNBD.git):

### 1. Schema & Physical Units Handled
- **Vehicle CAN Bus / Racelogic VBOX HD2 (`V-*.csv`, 10 Hz)**:
  - 29 standard columns including: GPS Latitude/Longitude/Height, velocity (km/h -> m/s), Heading (deg -> rad), 4-wheel rotational speeds (rad/s), Indicated Longitudinal & Lateral Accelerations (g -> m/s^2), Yaw Rate (deg/s -> rad/s).
  - Wheel Odometry: Fuses all four wheel speeds ($\omega_{\text{avg}} = \frac{FL + FR + RL + RR}{4}$) using the Ford Fiesta 195/55 R15 tyre rolling radius ($R \approx 0.298\,\text{m}$) for independent velocity verification.
- **Smartphone AndroSensor Recordings (`S-*.csv`, 10 Hz IMU, 1 Hz GPS)**:
  - 24 standard columns including 3-axis Accelerometer ($m/s^2$), Gravity vector ($m/s^2$), 3-axis Gyroscope ($\text{rad}/s$), Magnetic Field ($\mu T$), and GPS coordinates.
- **WGS84 Geodetic to Metric ENU**:
  - Automatically maps GPS coordinates into local Cartesian East-North-Up metric space using the `CoordinateTransformer`.
- **Git LFS Safety**:
  - Automatically identifies and handles Git LFS pointer stubs with clear diagnostics.

### 2. Training with IO-VNBD Data
```bash
# Seamless auto-detection (trains on IO-VNBD logs if found, otherwise falls back gracefully)
python models/train.py --dataset-mode auto

# Dedicated IO-VNBD training
python models/train.py --dataset-mode iovnbd --data-dir data/iovnbd_samples

# Hybrid training (combines IO-VNBD real recordings with domain-randomized synthetic drives)
python models/train.py --dataset-mode hybrid
```

### 3. Outage Evaluation & Drift Benchmarking
Evaluate the trained model during simulated GNSS outages (e.g. 30s tunnel):
```bash
python benchmark_iovnbd.py --data-path data/iovnbd_samples/V-Drive_Sample1.csv --outage-duration 30.0
```
This produces a side-by-side comparative table:
- **Baseline (Pure IMU Integration)**: Uncorrected Euler dead reckoning where sensor bias and noise compound quadratically ($O(t^2)$).
- **Intelligent Dead Reckoning (ML + 5-state EKF)**: Deep learning predicted velocity & yaw rate pseudo-odometry innovations bound drift during GNSS denial.

---

## 🚀 Quickstart Guide

### 1. Run the Backend & Interactive Demo
```bash
python run_backend.py
```
Open your browser at **`http://localhost:8000`** to view the live dashboard.
- Click **"Start 150s Drive Mission"** to simulate an urban drive through an 800m tunnel.
- Click **"Simulate Signal Loss (Tunnel Outage)"** to manually toggle GNSS loss anytime.

### 2. Run Automated Unit & Integration Tests (25 Passing Tests)
```bash
python -m pytest -v tests/
```
All 25 tests verify coordinate accuracy, EKF stability, online drift calibration, IO-VNBD schema parsing, resamplers, sliding windows, and backend routing.
