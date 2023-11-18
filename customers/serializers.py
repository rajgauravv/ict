from rest_framework import serializers
from .models import Customer, Purchase


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('user', 'first_name', 'last_name', 'email', 'phone_number', 'address')


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'