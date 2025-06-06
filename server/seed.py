from server.app import app
from server.models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")
    try:
        for rp in RestaurantPizza.query.all():
            db.session.delete(rp)
        for r in Restaurant.query.all():
            db.session.delete(r)
        for p in Pizza.query.all():
            db.session.delete(p)
        db.session.commit()

        print("Creating pizzas...")
        pizza1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
        pizza2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")
        db.session.add_all([pizza1, pizza2])
        db.session.commit()

        print("Creating restaurants...")
        rest1 = Restaurant(name="Pizza Palace", address="123 Main St")
        rest2 = Restaurant(name="Cheesy Bites", address="456 Side St")
        db.session.add_all([rest1, rest2])
        db.session.commit()

        print("Linking pizzas to restaurants...")
        rp1 = RestaurantPizza(price=10, restaurant=rest1, pizza=pizza1)
        rp2 = RestaurantPizza(price=15, restaurant=rest1, pizza=pizza2)
        rp3 = RestaurantPizza(price=12, restaurant=rest2, pizza=pizza1)
        db.session.add_all([rp1, rp2, rp3])
        db.session.commit()

        print("Seeding complete.")

    except Exception as e:
        db.session.rollback()
        print(f"Error seeding database: {e}")