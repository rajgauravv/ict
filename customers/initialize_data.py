from django.contrib.auth.models import User
from .models import Customer, Purchase, Order, Review
from ice_cream_truck.models import BaseIceCreamTruckItemFields, Flavor


def load_customers_data():
    # Create a user for admin
    admin_user = User.objects.create_user(username="1234567890", password="Admin@123")
    admin_user.save()

    # Create a customer with admin user
    admin_customer = Customer(
        user=admin_user,
        first_name="Admin",
        last_name="User",
        email="admin@example.com",
        phone_number="1234567890",
        address="123 Admin Street"
    )
    admin_customer.save()

    # Create more customers
    customer1 = Customer(
        user=User.objects.create_user(username="9876543210", password="Customer@123"),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="9876543210",
        address="456 Elm Street"
    )
    customer1.save()

    customer2 = Customer(
        user=User.objects.create_user(username="5678901234", password="Customer@123"),
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        phone_number="5678901234",
        address="789 Oak Avenue"
    )
    customer2.save()

    # Create purchases for customers
    ice_cream = BaseIceCreamTruckItemFields.objects.create(
        name="Vanilla Ice Cream",
        price=2.0,
        quantity=10,
        food_type="ice_cream"
    )

    # Create purchases for customers
    purchase1 = Purchase(
        customer=customer1,
        item=ice_cream,
        flavor=Flavor.objects.create(food_item=ice_cream, name="Chocolate"),
        quantity=3,
        total_amount=6.0
    )
    purchase1.save()

    purchase2 = Purchase(
        customer=customer2,
        item=ice_cream,
        flavor=Flavor.objects.create(food_item=ice_cream, name="Strawberry"),
        quantity=2,
        total_amount=4.0
    )
    purchase2.save()

    # Create orders for customers
    order1 = Order(
        customer=customer1,
        total_amount=10.0
    )
    order1.save()
    order1.purchases.add(purchase1)

    order2 = Order(
        customer=customer2,
        total_amount=4.0
    )
    order2.save()
    order2.purchases.add(purchase2)

    # Create reviews for customers
    review1 = Review(
        customer=customer1,
        food_item=ice_cream,
        rating=5,
        comment="Great ice cream!"
    )
    review1.save()

    review2 = Review(
        customer=customer2,
        food_item=ice_cream,
        rating=4,
        comment="Good, but could be better."
    )
    review2.save()


if __name__ == "__main__":
    load_customers_data()
