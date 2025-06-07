from flask import Flask
from server.models import db
from server.routes.restaurant_routes import restaurant_bp
from server.routes.pizza_routes import pizza_bp
from server.routes.restaurant_pizza_routes import restaurant_pizza_bp

def create_app(config_object=None):
    app = Flask(__name__)

    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///app.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if config_object:
        app.config.update(config_object)

    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(restaurant_bp)
    app.register_blueprint(pizza_bp)
    app.register_blueprint(restaurant_pizza_bp)

    return app
