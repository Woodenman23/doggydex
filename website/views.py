from flask import (
    Blueprint,
    render_template,
    request,
    session,
    flash,
    redirect,
    url_for,
    jsonify,
)
from flask_login import logout_user, current_user
import torch
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

from website import db, PROJECT_ROOT

views = Blueprint("views", __name__)

upload_folder = PROJECT_ROOT / "website/static/uploads"
num_dog_breeds = 120

classes = [
    "n02085620-Chihuahua",
    "n02085782-Japanese_spaniel",
    "n02085936-Maltese_dog",
    "n02086079-Pekinese",
    "n02086240-Shih-Tzu",
    "n02086646-Blenheim_spaniel",
    "n02086910-papillon",
    "n02087046-toy_terrier",
    "n02087394-Rhodesian_ridgeback",
    "n02088094-Afghan_hound",
    "n02088238-basset",
    "n02088364-beagle",
    "n02088466-bloodhound",
    "n02088632-bluetick",
    "n02089078-black-and-tan_coonhound",
    "n02089867-Walker_hound",
    "n02089973-English_foxhound",
    "n02090379-redbone",
    "n02090622-borzoi",
    "n02090721-Irish_wolfhound",
    "n02091032-Italian_greyhound",
    "n02091134-whippet",
    "n02091244-Ibizan_hound",
    "n02091467-Norwegian_elkhound",
    "n02091635-otterhound",
    "n02091831-Saluki",
    "n02092002-Scottish_deerhound",
    "n02092339-Weimaraner",
    "n02093256-Staffordshire_bullterrier",
    "n02093428-American_Staffordshire_terrier",
    "n02093647-Bedlington_terrier",
    "n02093754-Border_terrier",
    "n02093859-Kerry_blue_terrier",
    "n02093991-Irish_terrier",
    "n02094114-Norfolk_terrier",
    "n02094258-Norwich_terrier",
    "n02094433-Yorkshire_terrier",
    "n02095314-wire-haired_fox_terrier",
    "n02095570-Lakeland_terrier",
    "n02095889-Sealyham_terrier",
    "n02096051-Airedale",
    "n02096177-cairn",
    "n02096294-Australian_terrier",
    "n02096437-Dandie_Dinmont",
    "n02096585-Boston_bull",
    "n02097047-miniature_schnauzer",
    "n02097130-giant_schnauzer",
    "n02097209-standard_schnauzer",
    "n02097298-Scotch_terrier",
    "n02097474-Tibetan_terrier",
    "n02097658-silky_terrier",
    "n02098105-soft-coated_wheaten_terrier",
    "n02098286-West_Highland_white_terrier",
    "n02098413-Lhasa",
    "n02099267-flat-coated_retriever",
    "n02099429-curly-coated_retriever",
    "n02099601-golden_retriever",
    "n02099712-Labrador_retriever",
    "n02099849-Chesapeake_Bay_retriever",
    "n02100236-German_short-haired_pointer",
    "n02100583-vizsla",
    "n02100735-English_setter",
    "n02100877-Irish_setter",
    "n02101006-Gordon_setter",
    "n02101388-Brittany_spaniel",
    "n02101556-clumber",
    "n02102040-English_springer",
    "n02102177-Welsh_springer_spaniel",
    "n02102318-cocker_spaniel",
    "n02102480-Sussex_spaniel",
    "n02102973-Irish_water_spaniel",
    "n02104029-kuvasz",
    "n02104365-schipperke",
    "n02105056-groenendael",
    "n02105162-malinois",
    "n02105251-briard",
    "n02105412-kelpie",
    "n02105505-komondor",
    "n02105641-Old_English_sheepdog",
    "n02105855-Shetland_sheepdog",
    "n02106030-collie",
    "n02106166-Border_collie",
    "n02106382-Bouvier_des_Flandres",
    "n02106550-Rottweiler",
    "n02106662-German_shepherd",
    "n02107142-Doberman",
    "n02107312-miniature_pinscher",
    "n02107574-Greater_Swiss_Mountain_dog",
    "n02107683-Bernese_mountain_dog",
    "n02107908-Appenzeller",
    "n02108000-EntleBucher",
    "n02108089-boxer",
    "n02108422-bull_mastiff",
    "n02108551-Tibetan_mastiff",
    "n02108915-French_bulldog",
    "n02109047-Great_Dane",
    "n02109525-Saint_Bernard",
    "n02109961-Eskimo_dog",
    "n02110063-malamute",
    "n02110185-Siberian_husky",
    "n02110627-affenpinscher",
    "n02110806-basenji",
    "n02110958-pug",
    "n02111129-Leonberg",
    "n02111277-Newfoundland",
    "n02111500-Great_Pyrenees",
    "n02111889-Samoyed",
    "n02112018-Pomeranian",
    "n02112137-chow",
    "n02112350-keeshond",
    "n02112706-Brabancon_griffon",
    "n02113023-Pembroke",
    "n02113186-Cardigan",
    "n02113624-toy_poodle",
    "n02113712-miniature_poodle",
    "n02113799-standard_poodle",
    "n02113978-Mexican_hairless",
    "n02115641-dingo",
    "n02115913-dhole",
    "n02116738-African_hunting_dog",
]


@views.route("/", methods=["GET", "POST"])
def home() -> None:
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        file_path = upload_folder / file.filename
        file.save(str(file_path))
        dog_image_path = f'static/uploads/{str(file_path).split("/")[-1]}'

        # TODO: fix this path (download model state from google drive)
        MODEL_PATH = (
            f"/content/drive/MyDrive/projects/pokedex/dognet-convnext_large.pth"
        )
        model = models.convnext_large(pretrained=True)
        model.classifier[-1] = torch.nn.Linear(
            model.classifier[-1].in_features, num_dog_breeds
        )
        model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device("cpu")))
        image_path = str(file_path)
        image = Image.open(image_path)

        # transfrom image into tensor
        transform = transforms.Compose(
            [
                transforms.RandomResizedCrop(224),
                transforms.ToTensor(),
                transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
            ]
        )
        input_tensor = transform(image).unsqueeze(0)
        # evaluate tensor
        model.eval()
        # Perform inference
        with torch.no_grad():
            output = model(input_tensor)

        probabilities = torch.nn.functional.softmax(output, dim=1)
        top3_probs, top3_indices = torch.topk(probabilities, 3)

        results = ""
        for i in range(3):
            results += f"  {classes[top3_indices[0][i].item()][10:]}, Probability: {str(top3_probs[0][i].item() * 100)[:5]}%\n"

        return render_template("dog.html.j2", dog_image=dog_image_path, results=results)

    return render_template("home.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))


@views.route("/profile", methods=["POST", "GET"])
def profile():
    pass


# @views.route("/logout")
# def logout():
#     session.pop("user", None)
#     session.pop("email", None)
#     session.pop("user_id", None)
#     logout_user()
#     return redirect(url_for("views.home"))
