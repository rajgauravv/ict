from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import IceCream, ShavedIce, SnackBar
from .serializers import IceCreamSerializer, ShavedIceSerializer, SnackBarSerializer


class IceCreamViewSet(viewsets.ModelViewSet):
    queryset = IceCream.objects.all()
    serializer_class = IceCreamSerializer


class ShavedIceViewSet(viewsets.ModelViewSet):
    queryset = ShavedIce.objects.all()
    serializer_class = ShavedIceSerializer


class SnackBarViewSet(viewsets.ModelViewSet):
    queryset = SnackBar.objects.all()
    serializer_class = SnackBarSerializer
