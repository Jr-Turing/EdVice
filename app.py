import os
import logging
from flask import Flask, render_template
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_login import LoginManager
from extensions import db
from dotenv import load_dotenv
from flask.cli import with_appcontext
import click

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables early
load_dotenv()

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
    
    # Register routes
    from routes import register_routes
    register_routes(app)

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

    # CLI: Import colleges from CSV
    from admin_tools import import_colleges_from_csv

    @click.command('import-colleges')
    @click.argument('csv_path')
    @with_appcontext
    def import_colleges_command(csv_path):
        try:
            count = import_colleges_from_csv(csv_path)
            click.echo(f"Imported/updated {count} colleges from {csv_path}")
        except Exception as e:
            click.echo(f"Failed to import: {e}")

    app.cli.add_command(import_colleges_command)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('error.html', error_code=404), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('error.html', error_code=500), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('error.html', error_code=403), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
