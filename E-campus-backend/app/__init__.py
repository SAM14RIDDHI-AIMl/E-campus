from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Application factory"""
    # Get path to frontend directory (one level up from backend)
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    app = Flask(__name__, static_folder=frontend_path, static_url_path='')
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_bp, admin_bp, student_bp, schedule_bp, attendance_bp, inquiry_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(inquiry_bp)
    
    # Serve static files and index.html for SPA routing
    @app.route('/')
    def serve_index():
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # If file exists, serve it
        if os.path.exists(os.path.join(frontend_path, path)):
            return send_from_directory(frontend_path, path)
        # Otherwise serve index.html for SPA routing
        return send_from_directory(frontend_path, 'index.html')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
