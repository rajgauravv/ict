from django.contrib.auth.models import User
from .models import Customer


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
        address="123 Admin Street",
        total_spent=0.0
    )
    admin_customer.save()

    # Create more customers
    customer1 = Customer(
        user=User.objects.create_user(username="9876543210", password="Customer@123"),
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        phone_number="9876543210",
        address="456 Elm Street",
        total_spent=50.0
    )
    customer1.save()

    customer2 = Customer(
        user=User.objects.create_user(username="5678901234", password="Customer@123"),
        first_name="Jane",
        last_name="Smith",
        email="jane@example.com",
        phone_number="5678901234",
        address="789 Oak Avenue",
        total_spent=75.0
    )
    customer2.save()


if __name__ == "__main__":
    load_customers_data()
