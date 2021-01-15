from flask import Flask
from .extensions import mongo
from FlaskApp.api.routes import api


def create_app():
    app = Flask(__name__)

    # DB Configuration
    app.config["MONGO_URI"] = "mongodb://localhost:27017/chicago_db"
    mongo.init_app(app)

    # Register blueprints
    app.register_blueprint(api)
    return app
