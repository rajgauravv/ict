from django.db import models


# Create your models here.
class FoodType:
    FOOD_CHOICES = (
        ('ice_cream', 'ice_cream'),
        ('shaved_ice', 'shaved_ice'),
        ('snack_bar', 'snack_bar')
    )


class BaseIceCreamTruckItemFields(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()
    food_type = models.CharField(
        max_length=10,
        choices=FoodType.FOOD_CHOICES,
        default='ice_cream'
    )

    def __str__(self):
        return self.get_food_type_display()


class Flavor(models.Model):
    """
    To manage different ice creams with flavors, currently we have
    Chocolate, Pistachio, Strawberry and Mint.
    """
    food_item = models.ForeignKey(BaseIceCreamTruckItemFields, on_delete=models.CASCADE, related_name='flavors')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
