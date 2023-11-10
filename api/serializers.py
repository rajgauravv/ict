from rest_framework import serializers

# local imports
from ice_cream_truck.models import Flavor


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = ['name']


class FoodPurchaseSerializer(serializers.Serializer):
    customer_id = serializers.IntegerField()
    food_type = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    flavors = FlavorSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data


class InventorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=5, decimal_places=2)
    quantity = serializers.IntegerField()


