from .models import BaseIceCreamTruckItemFields, Flavor


def load_ice_cream_data():
    vanilla_ice_cream = BaseIceCreamTruckItemFields(name="Vanilla and Chocolate Cream", description="Classic vanilla flavor", price=2.50, quantity=50, food_type='ice_cream')
    vanilla_ice_cream.save()

    vanilla_flavor = Flavor(food_item=vanilla_ice_cream, name="Chocolate")
    vanilla_flavor.save()

    vanilla_ice_cream2 = BaseIceCreamTruckItemFields(name="Strawberry Cream", description="Strawberry flavor", price=2.50, quantity=20, food_type='ice_cream')
    vanilla_ice_cream2.save()

    vanilla_flavor = Flavor(food_item=vanilla_ice_cream2, name="Strawberry")
    vanilla_flavor.save()


def load_shaved_ice_data():
    shaved_ice = BaseIceCreamTruckItemFields(name="Shaved Ice", description="Refreshing shaved ice", price=3.00, quantity=30, food_type='shaved_ice')
    shaved_ice.save()

    shaved_ice_flavor = Flavor(food_item=shaved_ice, name="Mint")
    shaved_ice_flavor.save()


def load_snack_bar_data():
    snack_bar = BaseIceCreamTruckItemFields(name="Snack Bar", description="Delicious snacks", price=1.50, quantity=35, food_type='snack_bar')
    snack_bar.save()

    snack_bar_flavor = Flavor(food_item=snack_bar, name="Pistachio")
    snack_bar_flavor.save()


if __name__ == "__main__":
    load_ice_cream_data()
    load_shaved_ice_data()
    load_snack_bar_data()
