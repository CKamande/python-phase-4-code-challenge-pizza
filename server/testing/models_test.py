import pytest
from faker import Faker
from server.models import db, Restaurant, Pizza, RestaurantPizza
from server import create_app

@pytest.fixture(scope='module')
def test_app():
    app = create_app({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.mark.usefixtures("test_app")
class TestRestaurantPizza:
    '''Tests for RestaurantPizza model validation'''

    def test_price_between_1_and_30(self):
        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address='Main St')
        db.session.add_all([pizza, restaurant])
        db.session.commit()

        rp1 = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=1)
        rp2 = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=30)
        db.session.add_all([rp1, rp2])
        db.session.commit()

        assert rp1.price == 1
        assert rp2.price == 30

    def test_price_too_low(self):
        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address='Main St')
        db.session.add_all([pizza, restaurant])
        db.session.commit()

        with pytest.raises(ValueError):
            rp = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=0)
            db.session.add(rp)
            db.session.commit()

    def test_price_too_high(self):
        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address='Main St')
        db.session.add_all([pizza, restaurant])
        db.session.commit()

        with pytest.raises(ValueError):
            rp = RestaurantPizza(restaurant_id=restaurant.id, pizza_id=pizza.id, price=31)
            db.session.add(rp)
            db.session.commit()
