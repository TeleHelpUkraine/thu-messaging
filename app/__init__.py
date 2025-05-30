from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    from app.main.routes.webhook import webhook_bp as main_bp
    app.register_blueprint(main_bp)

    # Optional: configure DB, CORS, logging, etc.

    return appfrom flask import Flask
