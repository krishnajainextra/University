from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()
# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///university.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    
    # Import models
    from app.models.user import User
    
    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    from app.routes.user import user as user_blueprint
    app.register_blueprint(user_blueprint)
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # Context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    return app