import unittest
from server.app import create_app
from server.models import db, Restaurant, Pizza, RestaurantPizza

class AppTestCase(unittest.TestCase):
    def setUp(self):
        # Create the Flask test app with config
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
            'SQLALCHEMY_TRACK_MODIFICATIONS': False
        })
        self.client = self.app.test_client()

        # Setup database in the app context
        with self.app.app_context():
            db.create_all()

            # Seed test data
            r1 = Restaurant(name="Pizza Palace", address="123 Main St")
            r2 = Restaurant(name="Slice Haven", address="456 Elm St")
            p1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
            p2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")
            db.session.add_all([r1, r2, p1, p2])
            db.session.commit()

            rp1 = RestaurantPizza(price=15, restaurant_id=r1.id, pizza_id=p1.id)
            db.session.add(rp1)
            db.session.commit()

    def tearDown(self):
        # Clean up database
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_all_restaurants(self):
        res = self.client.get('/restaurants')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()), 2)

    def test_get_single_restaurant_success(self):
        with self.app.app_context():
            restaurant = Restaurant.query.first()
        res = self.client.get(f'/restaurants/{restaurant.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIn('name', res.get_json())

    def test_get_single_restaurant_not_found(self):
        res = self.client.get('/restaurants/999')
        self.assertEqual(res.status_code, 404)
        self.assertIn('error', res.get_json())

    def test_delete_restaurant_success(self):
        with self.app.app_context():
            restaurant = Restaurant.query.first()
        res = self.client.delete(f'/restaurants/{restaurant.id}')
        self.assertEqual(res.status_code, 204)

    def test_delete_restaurant_not_found(self):
        res = self.client.delete('/restaurants/999')
        self.assertEqual(res.status_code, 404)

    def test_get_all_pizzas(self):
        res = self.client.get('/pizzas')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()), 2)

    def test_create_restaurant_pizza_success(self):
        with self.app.app_context():
            restaurant = Restaurant.query.first()
            pizza = Pizza.query.first()

        payload = {
            "price": 10,
            "restaurant_id": restaurant.id,
            "pizza_id": pizza.id
        }
        res = self.client.post('/restaurant_pizzas', json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['name'], pizza.name)

    def test_create_restaurant_pizza_price_invalid(self):
        with self.app.app_context():
            restaurant = Restaurant.query.first()
            pizza = Pizza.query.first()

        payload = {
            "price": 100,  # invalid price > 30
            "restaurant_id": restaurant.id,
            "pizza_id": pizza.id
        }
        res = self.client.post('/restaurant_pizzas', json=payload)
        self.assertIn(res.status_code, (400, 422))  # Accept either depending on validation
        self.assertIn('error', res.get_json())
