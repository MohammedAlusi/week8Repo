import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from extensions import db
from routes import api_routes
from config import Config

def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DIST_FOLDER = os.path.join(BASE_DIR, "dist")

    app = Flask(__name__, static_folder=DIST_FOLDER, static_url_path="/")
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    app.register_blueprint(api_routes, url_prefix="/api")

    with app.app_context():
        db.create_all()

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def serve(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, "index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)