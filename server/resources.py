from flask import request
from flask_restful import Resource
from .models import db, Restaurant, RestaurantPizza, Pizza


class RestaurantListResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        return [r.to_dict(only=("id", "name", "address")) for r in restaurants], 200


class RestaurantByIDResource(Resource):
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404

        return restaurant.to_dict(
            rules=("-restaurant_pizzas.restaurant", "-restaurant_pizzas.pizza.restaurant_pizzas")
        ), 200

    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {"error": "Restaurant not found"}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return {}, 204


class PizzaListResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        return [p.to_dict() for p in pizzas], 200


class RestaurantPizzaCreateResource(Resource):
    def post(self):
        data = request.get_json()

        try:
            rp = RestaurantPizza(
                price=data["price"],
                restaurant_id=data["restaurant_id"],
                pizza_id=data["pizza_id"]
            )
            db.session.add(rp)
            db.session.commit()

            return rp.pizza.to_dict(
                rules=("-restaurant_pizzas",)
            ), 201

        except Exception as e:
            db.session.rollback()
            return {"errors": [str(e)]}, 400
