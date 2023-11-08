from django.test import TestCase
from .models import BaseIceCreamTruckItemFields, Flavor
from decimal import Decimal


class BaseIceCreamTruckItemFieldsTestCase(TestCase):
    def setUp(self):
        BaseIceCreamTruckItemFields.objects.create(
            name="Chocolate Ice Cream",
            description="Delicious chocolate ice cream",
            price=Decimal('3.99'),  # Use Decimal to match the model
            quantity=10,
            food_type="ice_cream"
        )

    def test_base_item_creation(self):
        item = BaseIceCreamTruckItemFields.objects.get(name="Chocolate Ice Cream")
        self.assertEqual(item.name, "Chocolate Ice Cream")
        self.assertEqual(item.description, "Delicious chocolate ice cream")
        self.assertEqual(item.price, Decimal('3.99'))  # Use Decimal to match the model
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.food_type, "ice_cream")


class FlavorTestCase(TestCase):
    def setUp(self):
        base_item = BaseIceCreamTruckItemFields.objects.create(
            name="Pistachio Ice Cream",
            price=4.99,
            quantity=15,
            food_type="ice_cream"
        )
        Flavor.objects.create(food_item=base_item, name="Pistachio")

    def test_flavor_creation(self):
        base_item = BaseIceCreamTruckItemFields.objects.get(name="Pistachio Ice Cream")
        flavor = Flavor.objects.get(name="Pistachio")
        self.assertEqual(flavor.food_item, base_item)
        self.assertEqual(flavor.name, "Pistachio")
