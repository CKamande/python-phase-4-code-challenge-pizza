from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

from server.models import db, Restaurant, Pizza, RestaurantPizza

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///pizza.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# ------------------ Resources ------------------ #

class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict() for r in restaurants], 200


class RestaurantResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if restaurant:
            return restaurant.to_dict(), 200
        return {"error": "Restaurant not found"}, 404

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        try:
            db.session.delete(restaurant)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete restaurant: {str(e)}"}, 500


class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict() for p in pizzas], 200


class RestaurantPizzaListResource(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"errors": ["No input provided"]}, 400

        price = data.get("price")
        restaurant_id = data.get("restaurant_id")
        pizza_id = data.get("pizza_id")

        errors = []

        if price is None:
            errors.append("Price is required")
        elif not isinstance(price, (int, float)) or not (1 <= price <= 30):
            errors.append("Price must be a number between 1 and 30")

        if not restaurant_id:
            errors.append("Restaurant ID is required")

        if not pizza_id:
            errors.append("Pizza ID is required")

        if errors:
            return {"errors": errors}, 400

        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)

        if not restaurant or not pizza:
            return {"errors": ["Restaurant or Pizza not found"]}, 404

        try:
            new_rp = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
            db.session.add(new_rp)
            db.session.commit()
            return pizza.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 500

# ------------------ Routes ------------------ #

api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaListResource, '/pizzas')
api.add_resource(RestaurantPizzaListResource, '/restaurant_pizzas')

# ------------------ Run App ------------------ #

if __name__ == '__main__':
    app.run(debug=True)
