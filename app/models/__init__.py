# Models package
# Contains all database models for the product management system

from flask import Flask
from config import config
import logging

def create_app(config_name='default'):
    app = Flask(__name__ ,template_folder='../templates')
    app.config.from_object(config[config_name])
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.items import items_bp
    # from app.routes.vendors import vendors_bp
    # from app.routes.customers import customers_bp
    # from app.routes.orders import orders_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(items_bp)
    # app.register_blueprint(vendors_bp)
    # app.register_blueprint(customers_bp)
    # app.register_blueprint(orders_bp)
    
    # Register teardown handler
    @app.teardown_appcontext
    def close_db_connection(error):
        from app.services.database import db_service
        db_service.close_connection()
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app