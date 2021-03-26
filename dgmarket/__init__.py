from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from . import config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(config.from_object())
    # init app
    db.init_app(app)
    migrate.init_app(app, db)    
    jwt.init_app(app)

    # error handlers
    from .common import error_handlers
    app.register_error_handler(400, error_handlers.response_not_found)

    # models
    from .models import user_model

    # blueprints
    from .views import user_bp
    app.register_blueprint(user_bp.bp)

    
    
    return app
