from django.db.models import Sum
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ice_cream_truck.models import BaseIceCreamTruckItemFields
from ice_cream_truck.serializers import BaseIceCreamTruckItemFieldsSerializer
from .serializers import FoodPurchaseSerializer
from customers.models import Customer


class BuyFoodView(APIView):
    """
    API endpoint to purchase a specific food item from the ice cream truck.

    Example POST data:
    {
        "customer_id": 1,
        "food_type": "ice_cream",
        "quantity": 2
    }
    """
    def post(self, request, format=None):
        serializer = FoodPurchaseSerializer(data=request.data)
        try:
            if serializer.is_valid():
                customer_id = serializer.validated_data['customer_id']
                food_type = serializer.validated_data['food_type']
                name = serializer.validated_data['name']
                quantity = serializer.validated_data['quantity']

                customer = Customer.objects.get(id=customer_id)

                food_item = BaseIceCreamTruckItemFields.objects.filter(food_type=food_type, name=name)

                if food_item.count() > 0 and food_item[0].quantity >= quantity:
                    food_item = food_item[0]
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
        except BaseIceCreamTruckItemFields.DoesNotExist:
            return Response({"error": "Food item not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Food item not found"}, status=status.HTTP_400_BAD_REQUEST)


class GetInventoryView(APIView):
    """
    API endpoint to get the current inventory of the ice cream truck.
    """
    def get(self, request, format=None):
        try:
            queryset = BaseIceCreamTruckItemFields.objects.all().order_by('food_type')
            serializer = BaseIceCreamTruckItemFieldsSerializer(instance=queryset, many=True)
            output_data = serializer.data
            total_revenue = Customer.objects.aggregate(total_revenue=Sum('total_spent'))['total_revenue'] or 0
            output_data_dict = {}
            for data in output_data:
                print(data)
                if data.get('food_type') in output_data_dict:
                    output_data_dict[data.get('food_type')].append(data)
                else:
                    output_data_dict[data.get('food_type')] = [data]
            inventory_data = {
                "stock": output_data_dict,
                "total_revenue": total_revenue
            }
            return Response(inventory_data, status=status.HTTP_200_OK)
        except BaseIceCreamTruckItemFields.DoesNotExist:
            return Response({"error": "Food items not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return Response({"error": "Food item not found"}, status=status.HTTP_400_BAD_REQUEST)