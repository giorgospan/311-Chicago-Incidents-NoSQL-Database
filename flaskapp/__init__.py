from flask import Flask
from .extensions import mongo
from flaskapp.api.routes import api
from flaskapp.site.routes import site


def create_app():
    app = Flask(__name__)

    # DB Configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/chicago_db"
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(site)
    app.register_blueprint(api, url_prefix='/api')
    return app
