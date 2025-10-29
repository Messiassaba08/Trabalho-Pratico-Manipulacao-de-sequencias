from flask import Flask
from web.routes import main as web_routes

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_mapping(
        SECRET_KEY='your_secret_key',
        DATABASE='path_to_your_database',
    )
    
    # Register blueprints
    app.register_blueprint(web_routes)

    return app

app = create_app()