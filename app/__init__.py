# === app/__init__.py ===
from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, migrate, jwt, mail  # Import from extensions
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # Import blueprints *after* extensions are initialized
    from .routes.auth_routes import auth_bp
    from .routes.register_routes import register_bp
    from .routes.admin_routes import admin_bp
    from .services.client_services import client_services_bp
    from .services.admin_services import admin_services_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(register_bp, url_prefix='/api/userregister')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(client_services_bp, url_prefix='/api/clientservices')
    app.register_blueprint(admin_services_bp, url_prefix='/api/adminservices')

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = MAIL_PASSWORD  # App password, not real password
    app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER

    mail.init_app(app)

    return app
