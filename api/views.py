import decimal
import traceback

from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

# local imports
from ice_cream_truck.models import BaseIceCreamTruckItemFields, FlavorType
from ice_cream_truck.serializers import BaseIceCreamTruckItemFieldsSerializer
from .serializers import FoodPurchaseSerializer
from customers.models import Customer, Purchase, Order


class BuyFoodView(generics.CreateAPIView):
    serializer_class = FoodPurchaseSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'customer_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'food_type': openapi.Schema(type=openapi.TYPE_STRING),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
                'flavor': openapi.Schema(type=openapi.TYPE_STRING),
                'name': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['customer_id', 'food_type', 'quantity', 'name', 'flavor'],
        ),
        responses={
            201: "Purchase successful. Enjoy!",
            200: "Purchase failed. Sorry!"
        },
    )
    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return: Enjoy/Sorry
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if serializer.instance:
            return Response({"message": "ENJOY!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "SORRY!"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """

        :param serializer:
        :return: True/False for serializer.instance
        """
        customer_id = serializer.validated_data['customer_id']
        food_type = serializer.validated_data['food_type']
        name = serializer.validated_data['name']
        quantity = serializer.validated_data['quantity']
        flavor = self.request.data.get('flavor', None)

        customer = Customer.objects.get(id=customer_id)

        food_item = BaseIceCreamTruckItemFields.objects.filter(food_type=food_type, name=name, flavors__name=flavor)

        if food_item.exists() and food_item[0].quantity >= quantity:
            food_item = food_item[0]
            total_price = food_item.price * quantity
            food_item.quantity -= quantity

            with transaction.atomic():
                order, created = Order.objects.select_for_update().get_or_create(
                    customer=customer,
                    total_amount=total_price
                )
                order.save()

                purchase = Purchase.objects.create(
                    customer=customer,
                    item=food_item,
                    flavor=food_item.flavors.first() if flavor else None,
                    quantity=quantity,
                    total_amount=total_price
                )

                order.purchases.add(purchase)
                order.save()

                food_item.save()

            serializer.instance = purchase
            return purchase
        else:
            print("Quantity not sufficient")
            traceback.print_exc()
            # set instance to None, If purchase is not successful.
            serializer.instance = None


class GetInventoryView(generics.ListAPIView):
    """
    Get Inventory details - Available stock
    """
    serializer_class = BaseIceCreamTruckItemFieldsSerializer
    queryset = BaseIceCreamTruckItemFields.objects.all().order_by('food_type')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        customers = Customer.objects.all()
        total_revenue = sum(decimal.Decimal(customer.total_spent1) for customer in customers)

        output_data_dict = {}
        for data in serializer.data:
            if data.get('food_type') in output_data_dict:
                output_data_dict[data.get('food_type')].append(data)
            else:
                output_data_dict[data.get('food_type')] = [data]
        flavors = [flavor[0] for flavor in FlavorType.FLAVOR_CHOICES]
        inventory_data = {
            "stock": output_data_dict,
            "total_revenue": total_revenue,
            "flavors": flavors
        }

        return Response(inventory_data, status=status.HTTP_200_OK)
