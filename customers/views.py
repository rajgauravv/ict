from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
from django.http import JsonResponse


class CustomerList(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        customer_data = {
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name', ''),
            'email': request.data.get('email', ''),
            'phone_number': request.data.get('phone_number'),
            'address': request.data.get('address', ''),
        }
        try:
            # Create a new User
            user_data = {
                'username': request.data.get('phone_number'),
                'password': request.data.get('phone_number'),
                # Add other user-related fields if needed
            }

            # Use a database transaction to ensure data consistency
            with transaction.atomic():
                user, created = User.objects.get_or_create(username=user_data['username'])
                if not created:
                    customer = Customer.objects.filter(user_id=user.id).last()
                    return Response({"message": "User with this phone number already exists.",
                                    "customer_id": customer.id},
                                    status=status.HTTP_200_OK)

                user.set_password(user_data['password'])
                user.save()

                customer_data = {
                    'first_name': request.data.get('first_name'),
                    'last_name': request.data.get('last_name', ''),
                    'email': request.data.get('email', ''),
                    'phone_number': request.data.get('phone_number'),
                    'address': request.data.get('address'),
                    'user': user.id  # Associate the customer with the newly created user
                }

                serializer = CustomerSerializer(data=customer_data)
                if serializer.is_valid():
                    customer = serializer.save()
                    response_data = {
                        "message": "Customer created successfully",
                        "customer_id": customer.id  # Return the user's ID in the response
                    }
                    return JsonResponse(response_data, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(str(e))
            return JsonResponse({"message": "Error creating customer"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomerDetail(APIView):
    def get_object(self, pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return None

    def get(self, request, pk):
        customer = self.get_object(pk)
        if customer is not None:
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        customer = self.get_object(pk)
        if customer is not None:
            serializer = CustomerSerializer(customer, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        customer = self.get_object(pk)
        if customer is not None:
            customer.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
