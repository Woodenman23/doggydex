import torch
import torchvision.transforms as transforms
from website import PROJECT_ROOT
from website.classes import classes


def identify(image):

    model = torch.load(str(PROJECT_ROOT / "models/dognext_large_quantized.pth"))
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

    # Format the results with progress bars
    def get_confidence_class(prob):
        if prob >= 70:
            return "high"
        elif prob >= 40:
            return "medium"
        else:
            return "low"
    
    results = f"""
    <div class="breed-card primary fade-in">
        <h3 class='mb-3'><strong>{breed1}</strong></h3>
        <div class="confidence-bar">
            <div class="confidence-fill {get_confidence_class(prob1)}" style="width: {prob1:.1f}%">
                {prob1:.1f}%
            </div>
        </div>
    </div>
    
    <div class="breed-card secondary fade-in">
        <h5 class="mb-2">Other possibilities:</h5>
        <div class="mb-3">
            <strong>{breed2}</strong>
            <div class="confidence-bar">
                <div class="confidence-fill {get_confidence_class(prob2)}" style="width: {prob2:.1f}%">
                    {prob2:.1f}%
                </div>
            </div>
        </div>
        <div>
            <strong>{breed3}</strong>
            <div class="confidence-bar">
                <div class="confidence-fill {get_confidence_class(prob3)}" style="width: {prob3:.1f}%">
                    {prob3:.1f}%
                </div>
            </div>
        </div>
    </div>
    """

    return results


def format_name(name):
    return " ".join([nm.capitalize() for nm in name.split("_")])
