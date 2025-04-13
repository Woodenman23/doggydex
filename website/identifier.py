import torch
import torchvision.transforms as transforms
from torchvision.models import convnext_large, ConvNeXt_Large_Weights

from website import PROJECT_ROOT
from website.classes import classes

num_dog_breeds = 120

MODEL_PATH = PROJECT_ROOT / "models/dognet-convnext_large.pth"


def identify(image):

    weights = ConvNeXt_Large_Weights.DEFAULT
    model = convnext_large(weights=weights)

    model.classifier[-1] = torch.nn.Linear(
        model.classifier[-1].in_features, num_dog_breeds
    )
    model.load_state_dict(torch.load(str(MODEL_PATH), map_location=torch.device("cpu")))

    transform = transforms.Compose(
        [
            transforms.CenterCrop(224),
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

    breed1 = format_name(classes[top3_indices[0][0].item()][10:])
    prob1 = top3_probs[0][0].item() * 100

    breed2 = format_name(classes[top3_indices[0][1].item()][10:])
    prob2 = top3_probs[0][1].item() * 100

    breed3 = format_name(classes[top3_indices[0][2].item()][10:])
    prob3 = top3_probs[0][2].item() * 100

    results = (
        f"<h3 class='mb-3'><strong>{breed1}</strong></h3>"
        f"<p class='text-muted'>Probability: {prob1:.2f}%</p>"
        f"<p class='mt-4'>Not quite right? It might also be a "
        f"<code>{breed2}</code> ({prob2:.2f}%) or <code>{breed3}</code> ({prob3:.2f}%).</p>"
    )

    return results


def format_name(name):
    return " ".join([nm.capitalize() for nm in name.split("_")])
