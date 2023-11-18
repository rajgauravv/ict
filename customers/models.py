import decimal
import traceback
from decimal import Decimal, InvalidOperation

from django.db import models
from django.contrib.auth.models import User

from ice_cream_truck.models import BaseIceCreamTruckItemFields, Flavor


class Customer(models.Model):
    """
    To keep track of all customers and total spent
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=False, blank=True, null=True)
    phone_number = models.CharField(max_length=15, unique=True)
    address = models.TextField(blank=True, null=True)

    @property
    def total_spent1(self):
        """
        Calculate the total amount spent by the customer, we can use it later for promotions/discounts.
        """
        print("case in total spent1")
        return self.orders.aggregate(total=models.Sum('total_amount'))['total'] or 0.0

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(BaseIceCreamTruckItemFields, on_delete=models.CASCADE)
    flavor = models.ForeignKey(Flavor, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    discount = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        # Calculate total amount based on item price and quantity
        decimal_number = Decimal(self.item.price)
        self.total_amount = (float(decimal_number) * float(self.quantity)) * ((100-self.discount)/100)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.first_name} purchased {self.quantity} - {self.item.name}(s) on {self.purchase_date}"


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    purchases = models.ManyToManyField(Purchase)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.total_amount = sum(purchase.total_amount for purchase in self.purchases.all())
        super().save(update_fields=['total_amount'])

    def __str__(self):
        return f"Order for {self.customer.first_name} on {self.order_date}"


class Review(models.Model):
    """
    Represents a customer review for an ice cream item.
    """
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    food_item = models.ForeignKey(BaseIceCreamTruckItemFields, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} for {self.food_item}"


class Promotion(models.Model):
    """
    Discounts/promotions offers
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name


class Payment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.amount} by {self.customer} on {self.timestamp}"


class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        (None, 'None'),
        ('standard', 'Standard'),
        ('premium', 'Premium')
    ]

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.customer}'s {self.get_membership_type_display()} Membership"
