from flask import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)

from website.drive_access import upload_to_drive, download_from_drive
from website.identifier import identify

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home() -> None:
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part"

        file = request.files["file"]
        if file.filename == "":
            return "No selected file"

        if file and file.filename:
            file_id = upload_to_drive(file.stream, file.filename, file.mimetype)

        pil_image, html_image = download_from_drive(file_id)

        return render_template(
            "dog.html.j2",
            dog_image=html_image,
            results=identify(pil_image),
        )

    return render_template("home.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))
