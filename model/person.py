from model.height import Height
from model.location import Location
# from string import capwords


class Person:

    # attrs: height, weight, age, Location (object)

    KG_PER_LB = 0.453592

    def __init__(self, age: float, weight: float, used_metric: bool = False):
        if (age is None or age <= 0) or (weight is None or weight <= 0):
            print(age, weight, used_metric)
            raise ValueError("Both age and height must be supplied and > 0")
        self.age: float = age
        self.used_metric = used_metric
        if not used_metric:
            self.weight_lb: float = weight
            self.weight_kg: float = weight * Person.KG_PER_LB
        else:
            self.weight_kg: float = weight
            self.weight_lb: float = weight / Person.KG_PER_LB
        self.height: Height = None
        self.location: Location = None

    def calc_calories_needed(self: float) -> float:
        if self.height is None:
            raise ValueError("Missing person's height")
        if self.location is None:
            raise ValueError("Missing person's location")
        # this formula is done with metric measurements
        temp_list = self.location.get_temperature()
        if not temp_list[1]:
            raise ValueError("Location could not be found, please try another one or a different spelling")
        return int(10 * self.weight_kg + 6.5 * self.height.centimeters
                          + 5 - temp_list[0])



# test
if __name__ == "__main__":
    me = Person(69, 215, False)
    me.height = Height()
    me.height.set_english(6, 0.5)
    print(f"weight: {me.weight_lb} lb, {me.weight_kg:.1f} kg, used metric: {me.used_metric}")
    print(f"height: {me.height.feet}'' {me.height.inches}\"; {me.height.centimeters} cm\n\n")
    for loc in ["nanuet", "new city", "new york", "atlanta", "xyzzy"]:
        # print(f"capwords: {capwords(loc)}")
        me.location = Location(loc, "usa")
        here =  me.location
        print(f"{here.city_pretty}, {here.country_pretty}:")
        print(f"\t{here.get_temperature(True):.1f}{Location.DEG_C}, or {here.get_temperature(False):.1f}{Location.DEG_F}")
        try:
            print(f"Calories needed: {me.calc_calories_needed():.1f}")
        except ValueError as ve:
            print(ve)
        print()
