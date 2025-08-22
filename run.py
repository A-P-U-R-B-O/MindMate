from flask import Flask
from app.models import db
from app.routes import routes

def create_app():
    app = Flask(__name__, static_folder='app/static', template_folder='app/templates')
    app.config.from_pyfile('config.py')

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(routes)

    # Optional: Configure session, security, CORS, etc.
    # Example: Secure session with a secret key
    app.secret_key = app.config.get("SECRET_KEY", "supersecretkey")

    # Example: Enable CORS for frontend development
    try:
        from flask_cors import CORS
        CORS(app)
    except ImportError:
        pass  # flask_cors is optional

    # Create DB tables if they don't exist (for development)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
