from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger, LazyString
import os
import yaml
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from backend.models import db
from backend.routes import register_blueprints
from backend.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # ----------------------------
    # Swagger configuration
    # ----------------------------
    SWAGGER_PATH = os.path.join(os.path.dirname(__file__), "swagger_spec.yaml")

    def load_swagger():
        """Load YAML spec dynamically."""
        with open(SWAGGER_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # Important: initialize SWAGGER config BEFORE creating Swagger(app)
    app.config["SWAGGER"] = {
        "title": "Holberton RPG Portfolio API",
        "uiversion": 3,
        "specs_route": "/apidocs/",
        # Désactive le modèle Swagger 2.0 interne
        "openapi": "3.0.2"
    }

    # Load YAML directly without merging Flasgger's 2.0 defaults
    swagger_template = load_swagger()
    swagger = Swagger(app, template=swagger_template, merge=False, config={
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec_1',
                "route": '/apispec_1.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    })

    # 🧠 Watcher to hot-reload YAML
    class SwaggerFileWatcher(FileSystemEventHandler):
        """Watch swagger_spec.yaml for changes and reload live."""

        def on_modified(self, event):
            if event.src_path.endswith("swagger_spec.yaml"):
                print("🔁 Swagger spec updated — reloading...")
                swagger.template = load_swagger()

    def start_watcher():
        observer = Observer()
        observer.schedule(SwaggerFileWatcher(), os.path.dirname(
            SWAGGER_PATH), recursive=False)
        observer_thread = threading.Thread(target=observer.start, daemon=True)
        observer_thread.start()

    if app.config.get("DEBUG", False):
        start_watcher()

    # ----------------------------
    # Register blueprints
    # ----------------------------
    register_blueprints(app)

    # ----------------------------
    # Global error handlers
    # ----------------------------
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app


# Expose app for Flask
app = create_app()
