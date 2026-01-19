from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
from .models import User
from .routes import main
from .auth import auth
import os

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath("templates")
    )
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app