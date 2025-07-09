#app/routes/__init__.py
from .auth_routes import auth_bp
from .register_routes import register_bp
from .admin_routes import admin_bp
from app.services.client_services import client_services_bp
from app.services.admin_services import admin_services_bp

__all__ = ['auth_bp', 'register_bp','admin_bp','admin_services_bp', 'client_services_bp']
