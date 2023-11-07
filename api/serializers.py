from rest_framework import serializers


class FoodPurchaseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    food_type = serializers.CharField()
    food_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_food_type(self, value):
        valid_food_types = ["ice_cream", "shaved_ice", "snack_bar"]
        if value not in valid_food_types:
            raise serializers.ValidationError("Invalid food type")
        return value


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.IntegerField()
