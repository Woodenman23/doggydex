import io
import base64
from flask import (
    Blueprint,
    render_template,
    request,
)
from PIL import Image

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
            pil_image = Image.open(file.stream)
            
            jpeg_io = io.BytesIO()
            pil_image.convert("RGB").save(jpeg_io, format="JPEG")
            jpeg_io.seek(0)
            html_image = base64.b64encode(jpeg_io.read()).decode("utf-8")

            return render_template(
                "dog.html.j2",
                dog_image=html_image,
                results=identify(pil_image),
            )

    return render_template("home.html.j2")
