import os
import sys
import torch

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.idr_model import IntelligentDeadReckoningNet

def export_torchscript():
    ckpt_path = "idr_model_best.pt"
    out_path = "idr_model_scripted.pt"
    if not os.path.exists(ckpt_path):
        print(f"Error: {ckpt_path} not found")
        return

    net = IntelligentDeadReckoningNet().cpu()
    ckpt = torch.load(ckpt_path, map_location="cpu")
    net.load_state_dict(ckpt["model_state_dict"])
    net.eval()

    dummy_input = torch.randn(1, 50, 6)
    traced = torch.jit.trace(net, dummy_input)
    traced.save(out_path)
    print(f"[Success] Exported TorchScript model to {out_path} ({os.path.getsize(out_path)/1024:.1f} KB)")

if __name__ == "__main__":
    export_torchscript()
