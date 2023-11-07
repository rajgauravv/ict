from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from customers.models import Customer
from ice_cream_truck.models import IceCream, SnackBar


class BuyFoodAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test_user",password="test_user_password"
        )

        # Create a customer
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Test Customer",
            email="test@example.com",
            phone_number="1234567890",
            address="Test Address",
        )

        # Create an ice cream
        self.ice_cream = IceCream.objects.create(
            name="Vanilla Ice Cream",
            price=2.0,
            quantity=10,
        )

        # Create a snack bar
        self.snack_bar = SnackBar.objects.create(
            name="Chocolate Bar",
            price=1.5,
            quantity=5,
        )

    def test_buy_ice_cream(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "ice_cream",
            "food_id": self.ice_cream.id,
            "quantity": 3,
        }

        response = self.client.post('/ice_cream_truck/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'],"ENJOY!")

        # Check if the ice cream quantity has decreased
        self.ice_cream.refresh_from_db()
        self.assertEqual(self.ice_cream.quantity, 7)
        self.assertEqual(response.json()['message'],"ENJOY!")

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_spent, 6.0)
        self.assertEqual(response.json()['message'],"ENJOY!")

    def test_buy_snack_bar_insufficient_stock(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "snack_bar",
            "food_id": self.snack_bar.id,
            "quantity": 10,
        }

        response = self.client.post('/ice_cream_truck/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['message'],"SORRY!")
        # Check if the snack bar quantity remains the same
        self.snack_bar.refresh_from_db()
        self.assertEqual(self.snack_bar.quantity, 5)
        self.assertEqual(response.json()['message'],"SORRY!")

    def test_get_inventory(self):
        response = self.client.get('/ice_cream_truck/get_inventory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(len(data['ice_creams']), 1)
        self.assertEqual(len(data['snack_bars']), 1)

    def test_buy_food_invalid_food_type(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "invalid_food",
            "food_id": self.ice_cream.id,
            "quantity": 2,
        }

        response = self.client.post('/ice_cream_truck/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
