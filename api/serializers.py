from rest_framework import serializers


class FoodPurchaseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    food_type = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.IntegerField()
