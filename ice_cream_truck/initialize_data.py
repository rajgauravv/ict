from .models import IceCream, IceCreamFlavor, ShavedIce, SnackBar


def load_ice_cream_data():
    # Create Ice Cream
    vanilla_ice_cream = IceCream(name="Vanilla Ice Cream", description="Classic vanilla flavor", price=2.50, quantity=10)
    vanilla_ice_cream.save()

    # Create Ice Cream Flavors
    vanilla_flavor = IceCreamFlavor(ice_cream=vanilla_ice_cream, name="Vanilla")
    vanilla_flavor.save()


def load_shaved_ice_data():
    # Create Shaved Ice items
    shaved_ice = ShavedIce(name="Shaved Ice", description="Refreshing shaved ice", price=3.00, quantity=20)
    shaved_ice.save()


def load_snack_bar_data():
    # Create Snack Bar items
    snack_bar = SnackBar(name="Snack Bar", description="Delicious snacks", price=1.50, quantity=15)
    snack_bar.save()


if __name__ == "__main__":
    load_ice_cream_data()
    load_shaved_ice_data()
    load_snack_bar_data()
