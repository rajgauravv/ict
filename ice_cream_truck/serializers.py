from rest_framework import serializers
from .models import IceCream, ShavedIce, SnackBar


class IceCreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = IceCream
        fields = '__all__'


class ShavedIceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShavedIce
        fields = '__all__'


class SnackBarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SnackBar
        fields = '__all__'
