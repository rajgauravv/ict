from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# local imports
from customers.models import Customer
from ice_cream_truck.models import BaseIceCreamTruckItemFields, Flavor


class BuyFoodAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="test_user",
            password="test_user_password"
        )

        # create a customer
        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Test Customer",
            email="test@example.com",
            phone_number="1234567891",
            address="Test Address",
        )

        # creating an ice cream object
        self.ice_cream = BaseIceCreamTruckItemFields.objects.create(
            name="Vanilla Ice Cream",
            price=2.0,
            quantity=10,
            food_type="ice_cream"
        )

        # creatin a snack bar object
        self.snack_bar = BaseIceCreamTruckItemFields.objects.create(
            name="Chocolate Bar",
            price=1.5,
            quantity=5,
            food_type="snack_bar"
        )

        self.flavors = Flavor.objects.create(food_item= self.ice_cream, name="Chocolate")
        self.flavors = Flavor.objects.create(food_item= self.snack_bar, name="Pistachio")

    def test_buy_ice_cream(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "ice_cream",
            "name": "Vanilla Ice Cream",
            "quantity": 3,
            "flavor": "Chocolate"
        }

        response = self.client.post('/api/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], "ENJOY!")

        # Refreshing db to check if the ice cream quantity has decreased
        self.ice_cream.refresh_from_db()
        self.assertEqual(self.ice_cream.quantity, 7)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_spent, 6.0)

    def test_buy_snack_bar_insufficient_stock(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "snack_bar",
            "name": "Chocolate Bar",
            "quantity": 10,
            "flavor": "Pistachio"
        }

        response = self.client.post('/api/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], "SORRY!")

        # Refreshing db to check if the snack bar quantity remains the same
        self.snack_bar.refresh_from_db()
        self.assertEqual(self.snack_bar.quantity, 5)

    def test_get_inventory(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "ice_cream",
            "name": "Vanilla Ice Cream",
            "quantity": 3,
            "flavor": "Chocolate"
        }
        self.client.post('/api/buy_food/', data, format='json')

        response = self.client.get('/api/get_inventory/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data['stock']

        # Entry for the presence of different food types
        self.assertIn('ice_cream', data)
        self.assertIn('snack_bar', data)

        ice_cream_data = data['ice_cream']
        self.assertEqual(len(ice_cream_data), 1)

        first_ice_cream = ice_cream_data[0]
        self.assertEqual(first_ice_cream['name'], "Vanilla Ice Cream")
        self.assertEqual(first_ice_cream['description'], None)
        self.assertEqual(float(first_ice_cream['price']), 2.0)
        self.assertEqual(first_ice_cream['quantity'], 7)
        self.assertEqual(first_ice_cream['food_type'], "ice_cream")

        total_revenue = response.data['total_revenue']
        self.assertEqual(float(total_revenue), 6.0)

    def test_buy_food_invalid_food_type(self):
        data = {
            "customer_id": self.customer.id,
            "food_type": "invalid_food",
            "name": "Invalid Food",
            "quantity": 2,
            "flavor": "Strawberry"
        }

        response = self.client.post('/api/buy_food/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
