from pathlib import Path
import torch
import torchvision.transforms as transforms
import torchvision.models as models

from website.classes import classes

num_dog_breeds = 120


def identify(image):
    MODEL_PATH = Path.home() / "dognet-convnext_large.pth"
    model = models.convnext_large(pretrained=True)
    model.classifier[-1] = torch.nn.Linear(
        model.classifier[-1].in_features, num_dog_breeds
    )
    model.load_state_dict(torch.load(str(MODEL_PATH), map_location=torch.device("cpu")))

    transform = transforms.Compose(
        [
            transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    input_tensor = transform(image).unsqueeze(0)

    model.eval()

    with torch.no_grad():
        output = model(input_tensor)

    probabilities = torch.nn.functional.softmax(output, dim=1)
    top3_probs, top3_indices = torch.topk(probabilities, 3)

    results = ""
    for i in range(3):
        results += f"{classes[top3_indices[0][i].item()][10:]}, Probability: {str(top3_probs[0][i].item() * 100)[:5]}%\n"
    return results
