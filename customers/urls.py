from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CustomerList, CustomerDetail, PurchaseList, PurchaseDetail

router = DefaultRouter()

urlpatterns = [
    path('', CustomerList.as_view(), name='customer_list'),
    path('<int:pk>/', CustomerDetail.as_view(), name='customer_detail'),
    path('purchases/', PurchaseList.as_view(), name='purchase_list'),
    path('purchases/<int:pk>/', PurchaseDetail.as_view(), name='purchase_detail'),
]

urlpatterns += router.urls
