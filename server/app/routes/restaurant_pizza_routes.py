from flask import Blueprint, request, jsonify
from server.models import db, RestaurantPizza, Pizza

restaurant_pizza_bp = Blueprint('restaurant_pizza_bp', __name__)

@restaurant_pizza_bp.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        price = data.get("price")
        restaurant_id = data.get("restaurant_id")
        pizza_id = data.get("pizza_id")

        if price is None or not (1 <= price <= 30):
            return jsonify({"error": "Price must be between 1 and 30"}), 400

        new_rp = RestaurantPizza(price=price, restaurant_id=restaurant_id, pizza_id=pizza_id)
        db.session.add(new_rp)
        db.session.commit()

        return jsonify(new_rp.pizza.to_dict()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
