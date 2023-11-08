from rest_framework import serializers
from .models import *


class FlavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flavor
        fields = '__all__'


class BaseIceCreamTruckItemFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseIceCreamTruckItemFields
        fields = '__all__'

