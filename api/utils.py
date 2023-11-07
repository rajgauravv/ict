from customers.models import Customer


def get_customer_object_or_none(customer_id):
    try:
        return Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None