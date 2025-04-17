import torch
from torchvision.models import convnext_large
from website import PROJECT_ROOT, MODEL_PATH

num_dog_breeds = 120

model = convnext_large(weights_only=True).eval()
# Replace the classifier layer
model.classifier[-1] = torch.nn.Linear(model.classifier[-1].in_features, num_dog_breeds)
model.load_state_dict(torch.load(str(MODEL_PATH), map_location=torch.device("cpu")))

model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
torch.save(model, str(PROJECT_ROOT / "models/dognext_large_quantized.pth"))
