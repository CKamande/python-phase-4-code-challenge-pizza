from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
import os

from models import db, Restaurant, Pizza, RestaurantPizza  # ✅ import from models.py

# Setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///pizza.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # ✅ bind db instance to app
migrate = Migrate(app, db)
api = Api(app)

# Resources
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

        db.session.delete(restaurant)
        db.session.commit()
        return '', 204


class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict() for p in pizzas], 200


class RestaurantPizzaListResource(Resource):
    def post(self):
        data = request.get_json()
        price = data.get("price")
        restaurant_id = data.get("restaurant_id")
        pizza_id = data.get("pizza_id")

        # Validate price
        if price is None or not (1 <= price <= 30):
            return {"errors": ["Price must be between 1 and 30"]}, 400

        restaurant = Restaurant.query.get(restaurant_id)
        pizza = Pizza.query.get(pizza_id)
        if not restaurant or not pizza:
            return {"errors": ["Restaurant or Pizza not found"]}, 400

        try:
            new_rp = RestaurantPizza(price=price, restaurant=restaurant, pizza=pizza)
            db.session.add(new_rp)
            db.session.commit()
            return pizza.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400

# Register endpoints
api.add_resource(RestaurantListResource, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaListResource, '/pizzas')
api.add_resource(RestaurantPizzaListResource, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(debug=True)
