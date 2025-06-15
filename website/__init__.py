import logging

from flask import Flask
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"


# Configuration
num_dog_breeds = 120
MODEL_PATH = PROJECT_ROOT / "models/dognet-convnext_large.pth"

logger = logging.getLogger(__name__)
logging.basicConfig(filename="doggydex.log", encoding="utf-8", level=logging.DEBUG)


class Section:
    def __init__(self, name: str) -> None:
        self.name = name
        self.title = " ".join(
            word.capitalize() for word in name.replace("_", " ").split()
        )
        self.route = "/" + name


def get_secret(secret_name):
    secret_path = f"/run/secrets/{secret_name}"
    try:
        with open(secret_path, "r") as secret_file:
            return secret_file.read().strip()
    except FileNotFoundError:
        print(f"Secret {secret_name} not found!")
        return None


def create_app() -> Flask:
    app = Flask(__name__)

    from website.views import views

    app.register_blueprint(views, url_prefix="/")

    return app
