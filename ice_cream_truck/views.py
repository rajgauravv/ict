from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import BaseIceCreamTruckItemFields
from .serializers import BaseIceCreamTruckItemFieldsSerializer


class BaseIceCreamTruckViewSet(viewsets.ModelViewSet):
    queryset = BaseIceCreamTruckItemFields.objects.all()
    serializer_class = BaseIceCreamTruckItemFieldsSerializer
