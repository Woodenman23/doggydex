import torch
import torchvision.transforms as transforms
from torchvision.models import convnext_large
from website import PROJECT_ROOT
from website.classes import classes

# Configuration
num_dog_breeds = 120
MODEL_PATH = PROJECT_ROOT / "models/dognet-convnext_large.pth"


def identify(image):
    # Initialize the base ConvNeXt Large model
    model = convnext_large(weights=None)
    # Replace the classifier with your fine-tuned layer
    model.classifier[-1] = torch.nn.Linear(
        model.classifier[-1].in_features, num_dog_breeds
    )
    # Load your fine-tuned state dictionary
    model.load_state_dict(torch.load(str(MODEL_PATH), map_location=torch.device("cpu")))
    # Apply dynamic quantization to linear layers
    model = torch.quantization.quantize_dynamic(
        model, {torch.nn.Linear}, dtype=torch.qint8
    )
    # Set model to evaluation mode
    model.eval()

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

    # Format the results
    results = (
        f"<h3 class='mb-3'><strong>{breed1}</strong></h3>"
        f"<p class='text-muted'>Probability: {prob1:.2f}%</p>"
        f"<p class='mt-4'>Not quite right? It might also be a "
        f"<code>{breed2}</code> ({prob2:.2f}%) or <code>{breed3}</code> ({prob3:.2f}%).</p>"
    )

    return results


def format_name(name):
    return " ".join([nm.capitalize() for nm in name.split("_")])
