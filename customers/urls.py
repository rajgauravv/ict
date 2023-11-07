from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerList, CustomerDetail

router = DefaultRouter()

urlpatterns = [
    path('', CustomerList.as_view(), name='customer_list'),
    path('<int:pk>/', CustomerDetail.as_view(), name='customer_detail'),
]

urlpatterns += router.urls
