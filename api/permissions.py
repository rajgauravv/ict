from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from functools import wraps

# Local
from api.utils import get_customer_object_or_none


def is_customer_owner(view_func):
    """
    Custom permission decorator to check if the user is the owner of the customer record.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        customer = get_customer_object_or_none(kwargs.get('customer_id'))
        if customer and customer.user == request.user:
            return view_func(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    return _wrapped_view


def is_admin_user_or_read_only(view_func):
    """
    Custom permission decorator to allow read-only access to non-admin users, and full access to admin users.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.method in permissions.SAFE_METHODS:
            return view_func(request, *args, **kwargs)

        if request.user and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    return _wrapped_view
