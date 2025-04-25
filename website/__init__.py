import logging

from flask import Flask
from pathlib import Path
from datetime import timedelta

PROJECT_ROOT = Path(__file__).parent.parent
IMAGES_PATH = PROJECT_ROOT / "website/static/images"


# Configuration
num_dog_breeds = 120
MODEL_PATH = PROJECT_ROOT / "models/dognet-convnext_large.pth"

logger = logging.getLogger(__name__)
logging.basicConfig(filename="doggydex.log", encoding="utf-8", level=logging.DEBUG)

class ScriptNameMiddleware:
    def __init__(self, app, script_name=''):
        self.app = app
        self.script_name = script_name

    def __call__(self, environ, start_response):
        environ['SCRIPT_NAME'] = self.script_name
        return self.app(environ, start_response)

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
    app.config["SECRET_KEY"] = "1234"
    app.permanent_session_lifetime = timedelta(days=3)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.wsgi_app = ScriptNameMiddleware(app.wsgi_app, script_name='/doggydex')

    from website.views import views

    app.register_blueprint(views)

    return app
