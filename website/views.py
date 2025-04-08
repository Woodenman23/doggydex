from flask import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from google.cloud import storage
from PIL import Image

from website import PROJECT_ROOT
from website.identifier import identify

views = Blueprint("views", __name__)
client = storage.Client()
bucket_name = "doggydex_store"
bucket = client.get_bucket(bucket_name)

image_path = "path/to/your/image.jpg"
blob = bucket.blob("image.jpg")
blob.upload_from_filename(image_path)


upload_folder = PROJECT_ROOT / "website/static/uploads"
num_dog_breeds = 120


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

        image = Image.open(str(file_path))

        return render_template(
            "dog.html.j2",
            dog_image=url_for("static", filename=f"uploads/{file.filename}"),
            results=identify(image),
        )

    return render_template("home.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))


@views.route("/about")
def about():
    return "this is the about page"
