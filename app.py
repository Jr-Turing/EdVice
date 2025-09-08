import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from extensions import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "career-advisor-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///career_advisor.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'

with app.app_context():
    # Import models and routes only after db/app are ready
    import models  # noqa: F401
    import routes  # noqa: F401

    # Setup user loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(user_id)

    # Create all tables
    db.create_all()

    # Initialize sample data
    from models import initialize_data
    initialize_data()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
