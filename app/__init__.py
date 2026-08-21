import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize database extension
db = SQLAlchemy()

def create_app():
    """Application factory: creates and configures the Flask instance."""
    app = Flask(__name__)

    # Basic configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Ensure the instance directory exists for SQLite
    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints/routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app