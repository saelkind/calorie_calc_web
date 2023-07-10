

class Person:

    # attrs: height, weight, age, Locale (object)

    def __init__(self, age: float, weight: float):
        if (age is None or age <= 0) or (weight is None or weight <= 0):
            raise ValueError("Both age and height must be supplies and > 0")
        self.age: float = age
        self.weight: float = weight
        self.height = None
        self.locale = None

    def calculate_calories(self):
        if self.height is None:
            raise ValueError("Missing person's height")
        if self.locale is None:
            raise ValueError("Missing person's locale")
        pass
