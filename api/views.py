from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FoodPurchaseSerializer, InventorySerializer
from ice_cream_truck.models import IceCream, ShavedIce, SnackBar
from customers.models import Customer


class BuyFoodView(APIView):
    """
    API endpoint to purchase a specific food item from the ice cream truck.

    Example POST data:
    {
        "customer_id": 1,
        "food_type": "ice_cream",
        "food_id": 1,
        "quantity": 2
    }
    """
    def post(self, request, format=None):
        serializer = FoodPurchaseSerializer(data=request.data)
        try:
            if serializer.is_valid():
                customer_id = serializer.validated_data['customer_id']
                food_type = serializer.validated_data['food_type']
                food_id = serializer.validated_data['food_id']
                quantity = serializer.validated_data['quantity']

                customer = Customer.objects.get(id=customer_id)

                if food_type == "ice_cream":
                    food_item = IceCream.objects.get(id=food_id)
                elif food_type == "shaved_ice":
                    food_item = ShavedIce.objects.get(id=food_id)
                elif food_type == "snack_bar":
                    food_item = SnackBar.objects.get(id=food_id)
                else:
                    return Response({"error": "Invalid food type"}, status=status.HTTP_400_BAD_REQUEST)

                if food_item.quantity >= quantity:
                    total_price = food_item.price * quantity
                    food_item.quantity -= quantity
                    food_item.save()

                    customer.total_spent += total_price
                    customer.save()

                    return Response({"message": "ENJOY!"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"message": "SORRY!"}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_400_BAD_REQUEST)
        except (IceCream.DoesNotExist, ShavedIce.DoesNotExist, SnackBar.DoesNotExist):
            return Response({"error": "Food item not found"}, status=status.HTTP_400_BAD_REQUEST)


class GetInventoryView(APIView):
    """
    API endpoint to get the current inventory of the ice cream truck.
    """
    def get(self, request, format=None):
        try:
            ice_creams = IceCream.objects.all()
            shaved_ice = ShavedIce.objects.all()
            snack_bars = SnackBar.objects.all()

            ice_cream_data = InventorySerializer(ice_creams, many=True).data
            shaved_ice_data = InventorySerializer(shaved_ice, many=True).data
            snack_bar_data = InventorySerializer(snack_bars, many=True).data

            total_revenue = Customer.objects.aggregate(total_revenue=Sum('total_spent'))['total_revenue'] or 0
            inventory_data = {
                "stock": {
                    "ice_cream": ice_cream_data,
                    "shaved_ice": shaved_ice_data,
                    "snack_bars": snack_bar_data
                },
                "total_revenue": total_revenue
            }
            return Response(inventory_data, status=status.HTTP_200_OK)
        except (IceCream.DoesNotExist, ShavedIce.DoesNotExist, SnackBar.DoesNotExist):
            return Response({"error": "Food items not found"}, status=status.HTTP_400_BAD_REQUEST)