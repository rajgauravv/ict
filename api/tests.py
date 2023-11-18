from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

# local imports
from customers.models import Customer, Purchase, Order, Review, Payment, Membership, Promotion
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

        self.flavors = Flavor.objects.create(food_item=self.ice_cream, name="Chocolate")
        self.flavors = Flavor.objects.create(food_item=self.snack_bar, name="Pistachio")

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

        # self.customer.refresh_from_db()
        # self.assertEqual(float(self.orders.total_spent), 6.0)

        # Refreshing customer to check if an order and purchase were created
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.orders.count(), 1)
        self.assertEqual(self.customer.orders.first().purchases.count(), 1)

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

    def test_purchase_model(self):
        purchase = Purchase.objects.create(
            customer=self.customer,
            item=self.ice_cream,
            flavor=self.flavors,
            quantity=2,
            total_amount=4.0
        )

        self.assertEqual(str(purchase),
                         f"{self.customer.first_name} purchased 2 - {self.ice_cream.name}(s) on {purchase.purchase_date}")

    def test_order_model(self):
        purchase = Purchase.objects.create(
            customer=self.customer,
            item=self.ice_cream,
            flavor=self.flavors,
            quantity=2,
            total_amount=4.0
        )

        order = Order.objects.create(
            customer=self.customer,
            total_amount=4.0
        )

        order.purchases.add(purchase)

        self.assertEqual(str(order), f"Order for {self.customer.first_name} on {order.order_date}")

    def test_review_model(self):
        review = Review.objects.create(
            customer=self.customer,
            food_item=self.ice_cream,
            rating=4,
            comment="Delicious!"
        )

        self.assertEqual(str(review), f"Review by {self.customer} for {self.ice_cream}")

    def test_total_spent_calculation(self):
        purchase = Purchase.objects.create(
            customer=self.customer,
            item=self.ice_cream,
            flavor=self.flavors,
            quantity=2,
            total_amount=4.0
        )

        order = Order.objects.create(
            customer=self.customer,
            total_amount=4.0
        )

        order.purchases.add(purchase)
        order.save()
        # refresh the customer
        self.customer.refresh_from_db()
        print("==>",self.customer.first_name)
        print("==>",self.customer.total_spent1)

        # check if total_spent1 is updated
        self.assertEqual(float(self.customer.total_spent1), 4.0)

    def test_total_spent_calculation_with_multiple_orders(self):
        purchase_1 = Purchase.objects.create(
            customer=self.customer,
            item=self.ice_cream,
            flavor=self.flavors,
            quantity=2,
            total_amount=4.0
        )

        purchase_2 = Purchase.objects.create(
            customer=self.customer,
            item=self.snack_bar,
            flavor=self.flavors,
            quantity=3,
            total_amount=4.5
        )

        order_1 = Order.objects.create(
            customer=self.customer,
            total_amount=4.0
        )

        order_2 = Order.objects.create(
            customer=self.customer,
            total_amount=4.5
        )

        # add the purchases to the orders
        order_1.purchases.add(purchase_1)
        order_2.purchases.add(purchase_2)
        order_1.save()
        order_2.save()

        self.customer.refresh_from_db()

        # total_spent1 is updated
        self.assertEqual(float(self.customer.total_spent1), 8.5)

    def test_total_spent_calculation_with_promotion(self):
        promotion = Promotion.objects.create(
            name="Discount on Ice Cream",
            description="Get 20% off on Vanilla Ice Cream",
            discount_percentage=20.0,
            start_date="2023-01-01T00:00:00Z",
            end_date="2023-01-31T23:59:59Z"
        )

        # Create a purchase with the promotion
        purchase = Purchase.objects.create(
            customer=self.customer,
            item=self.ice_cream,
            quantity=3,
            total_amount=4.8,  # Original price: 2.0 * 3 = 6.0, Discounted price: 6.0 * 0.8 = 4.8
            discount=20
        )

        # Create an order and add the purchase
        order = Order.objects.create(
            customer=self.customer,
            total_amount=4.8
        )
        order.purchases.add(purchase)
        order.save()

        # Refresh the customer to update total_spent1
        self.customer.refresh_from_db()

        # Check if total_spent1 reflects the discounted amount
        self.assertEqual(float(self.customer.total_spent1), 4.8)


class PaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_user_password"
        )

        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Test Customer",
            email="test@example.com",
            phone_number="1234567891",
            address="Test Address",
        )

    def test_payment_creation(self):
        payment = Payment.objects.create(
            customer=self.customer,
            amount=10.0,
            payment_method="Credit Card"
        )

        self.assertEqual(str(payment), f"Payment of 10.0 by {self.customer} on {payment.timestamp}")


class MembershipModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_user",
            password="test_user_password"
        )

        self.customer = Customer.objects.create(
            user=self.user,
            first_name="Test Customer",
            email="test@example.com",
            phone_number="1234567891",
            address="Test Address",
        )

    def test_membership_creation(self):
        membership = Membership.objects.create(
            customer=self.customer,
            membership_type="standard",
            start_date="2023-01-01T00:00:00Z",
            end_date="2024-01-01T00:00:00Z"
        )

        self.assertEqual(str(membership), f"{self.customer}'s Standard Membership")