from django.db import models

# Create your models here.


class BaseIceCreamTruckItemFields(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField()

    class Meta:
        abstract = True


class IceCream(BaseIceCreamTruckItemFields):

    def __str__(self):
        return self.name


class IceCreamFlavor(models.Model):
    """
    To manage different ice creams with flavors, currently we have
    Chocolate, Pistachio, Strawberry and Mint.
    """
    ice_cream = models.ForeignKey(IceCream, on_delete=models.CASCADE, related_name='flavors')
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ShavedIce(BaseIceCreamTruckItemFields):

    def __str__(self):
        return self.name


class SnackBar(BaseIceCreamTruckItemFields):

    def __str__(self):
        return self.name
