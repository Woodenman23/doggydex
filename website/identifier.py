import torch
import torchvision.transforms as transforms
from website import PROJECT_ROOT
from website.classes import classes


def identify(image):

    model = torch.load(str(PROJECT_ROOT / "models/dognext_large_quantized.pth"))
    # Set model to evaluation mode
    model.eval()

    # Convert image to RGB (removes alpha channel if present)
    if image.mode != 'RGB':
        image = image.convert('RGB')

    # Preprocess the input image
    transform = transforms.Compose(
        [
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ]
    )
    input_tensor = transform(image).unsqueeze(0)

    # Perform inference
    with torch.no_grad():
        output = model(input_tensor)

    # Process the output
    probabilities = torch.nn.functional.softmax(output, dim=1)
    top3_probs, top3_indices = torch.topk(probabilities, 3)

    # Extract top 3 predictions
    breed1 = format_name(classes[top3_indices[0][0].item()][10:])
    prob1 = top3_probs[0][0].item() * 100

    breed2 = format_name(classes[top3_indices[0][1].item()][10:])
    prob2 = top3_probs[0][1].item() * 100

    breed3 = format_name(classes[top3_indices[0][2].item()][10:])
    prob3 = top3_probs[0][2].item() * 100

    results = {
        'breed1': breed1,
        'prob1': prob1,
        'breed2': breed2,
        'prob2': prob2,
        'breed3': breed3,
        'prob3': prob3
    }

    return results


def format_name(name):
    return " ".join([nm.capitalize() for nm in name.split("_")])
