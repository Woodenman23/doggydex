import torch
from torchvision.models import convnext_large
from website import PROJECT_ROOT

model = convnext_large(weights=None).eval()
model.load_state_dict(
    torch.load(str(PROJECT_ROOT / "models/convnext_large_quantized.pth"))
)
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
torch.save(
    model.state_dict(), str(PROJECT_ROOT / "models/convnext_large_quantized.pth")
)
