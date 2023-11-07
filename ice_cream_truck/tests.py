import json

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import IceCream, ShavedIce, SnackBar
from .serializers import IceCreamSerializer, ShavedIceSerializer, SnackBarSerializer


class IceCreamViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.ice_cream_data = {'name': 'Vanilla Ice Cream', 'price': 2.50, 'quantity': 10}
        self.ice_cream = IceCream.objects.create(**self.ice_cream_data)

    def test_list_ice_creams(self):
        response = self.client.get('/ice_cream_truck/ice_creams/')
        ice_creams = IceCream.objects.all()
        serializer = IceCreamSerializer(ice_creams, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_ice_cream(self):
        new_ice_cream_data = {'name': 'Chocolate Ice Cream', 'price': 3.00, 'quantity': 20}
        response = self.client.post('/ice_cream_truck/ice_creams/', new_ice_cream_data, format='json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(IceCream.objects.count(), 2)

    def test_update_ice_cream(self):
        updated_data = {'name': 'Vanilla Ice Cream Updated', 'price': 2.75, 'quantity': 5}
        response = self.client.put(f'/ice_cream_truck/ice_creams/{self.ice_cream.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ice_cream.refresh_from_db()
        self.assertEqual(self.ice_cream.name, 'Vanilla Ice Cream Updated')

    def test_delete_ice_cream(self):
        response = self.client.delete(f'/ice_cream_truck/ice_creams/{self.ice_cream.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(IceCream.objects.count(), 0)


class ShavedIceViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.shaved_ice_data = {'name':'Shaved ice sample 1','price':12.50,'quantity':15}
        self.shaved_ice = ShavedIce.objects.create(**self.shaved_ice_data)

    def test_list_shaved_ice_data(self):
        response = self.client.get('/ice_cream_truck/shaved_ice/')
        shaved_ice = ShavedIce.objects.all()
        serializer = ShavedIceSerializer(shaved_ice, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_shave_ice_data(self):
        shaved_ice_data_new_sample = {'name':'Shaved ice sample 2','price': 07.17,'quantity':10}
        response = self.client.post('/ice_cream_truck/shaved_ice/',shaved_ice_data_new_sample, format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(len(ShavedIce.objects.all()),2)

    def test_update_shave_ice_data(self):
        update_data = {'name':'Shaved ice sample 3','price': 17.17,'quantity':15}
        response = self.client.put('/ice_cream_truck/shaved_ice/{}/'.format(self.shaved_ice.id), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.shaved_ice.refresh_from_db()
        self.assertEqual(self.shaved_ice.name,'Shaved ice sample 3')

    def test_delete_shaved_ice_data(self):
        response = self.client.delete('/ice_cream_truck/shaved_ice/{}/'.format(self.shaved_ice.id))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(ShavedIce.objects.count(),0)


class SnackBarViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.snack_bar_data = {'name': 'Choco Crunch Bar', 'price': '1.75', 'quantity': 30}
        self.snack_bar = SnackBar.objects.create(**self.snack_bar_data)

    def test_list_snack_bar(self):
        response = self.client.get('/ice_cream_truck/snack_bars/')
        snack_bar = SnackBar.objects.all()
        serializer = SnackBarSerializer(snack_bar,many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_create_snack_bar(self):
        snack_bar_new_sample = {'name': 'Choco Crunch Bar sample 2', 'price': 1.75, 'quantity': 30}
        response = self.client.post('/ice_cream_truck/snack_bars/',snack_bar_new_sample,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(SnackBar.objects.count(),2)

    def test_update_snack_bar(self):
        update_data = {'name': 'Choco Crunch Bar - sample 2 updated', 'price': 2.75, 'quantity': 25}
        response = self.client.put('/ice_cream_truck/snack_bars/{}/'.format(self.snack_bar.id),update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.snack_bar.refresh_from_db()
        self.assertEqual(self.snack_bar.name, 'Choco Crunch Bar - sample 2 updated')

    def test_delete_snack_bar(self):
        response = self.client.delete('/ice_cream_truck/snack_bars/{}/'.format(self.snack_bar.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(SnackBar.objects.count(), 0)
