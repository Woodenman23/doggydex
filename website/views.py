import tempfile
import os
from PIL import Image
import base64
from io import BytesIO

from flask import (
    Blueprint,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)

from website import logger
from website.identifier import identify

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            logger.error("No file part in request")
            return "No file part", 400

        file = request.files["file"]
        if file.filename == "":
            logger.error("No selected file")
            return "No selected file", 400

        if file and file.filename:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
                    file.save(temp_file.name)
                    temp_file_path = temp_file.name

                pil_image = Image.open(temp_file_path)

                # Convert image to base64 for HTML display
                buffered = BytesIO()
                pil_image.save(buffered, format=pil_image.format or "JPEG")
                html_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
                html_image = f"data:image/{pil_image.format.lower() or 'jpeg'};base64,{html_image}"

                results = identify(pil_image)

                try:
                    os.unlink(temp_file_path)
                    logger.debug(f"Deleted temporary file: {temp_file_path}")
                except Exception as e:
                    logger.error(f"Failed to delete temporary file {temp_file_path}: {str(e)}")

                return render_template(
                    "dog.html.j2",
                    dog_image=html_image,
                    results=results,
                )

            except Exception as e:
                logger.error(f"Error processing image: {str(e)}", exc_info=True)
                return f"Error processing image: {str(e)}", 500

    return render_template("home.html.j2")


@views.route("/session_data")
def session_data():
    return jsonify(dict(session))
