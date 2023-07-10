import typing

class Height:

    CM_PER_INCH = 2.54

    def __init__(self):
        self.feet = None
        self.inches = None
        self.centimeters = None
        self.metric = False

    def set_english(self, feet: int = 0, inches: float = 0.0):
        if (feet < 0 or inches < 0) or (feet == 0 and inches == 0.0):
            raise ValueError("Height needs positive feet and/or inches values")
        elif (feet > 0) and inches > 0:
            if inches >= 12:
                raise ValueError("If feet supplied, inches must be < 12")
        self.metric = False
        # legal if one and only one is None, account for that here
        if feet is None:
            feet = 0
        if inches is None:
            inches = 0
        self.feet: int = feet
        self.inches: int = inches
        if feet == 0:
            self.feet = int(self.inches) // 12
            self.inches = self.inches - self.feet * 12
        self.centimeters: float = (12 * feet + inches) * Height.CM_PER_INCH

    def set_metric(self, centimeters: float = 0.0):
        if centimeters <= 0.0:
            raise ValueError("Need to supply positive value(s) for height")
        self.metric = True
        self.centimeters: float = centimeters
        self.inches: float = centimeters / Height.CM_PER_INCH
        self.feet: int = int(self.inches) // 12
        self.inches = self.inches - (self.feet * 12)

    def print(self):
        if self.centimeters is None:
            raise ValueError("Height value was never set")
        print(f"{self.feet}' {self.inches:.2f}\"", end="")
        print(f" or {self.centimeters:.2f} cm")
        print("Was spec'd as metric:", self.metric)


# test code
if __name__ == "__main__":
    height = Height()
    height.set_english(6, 0.5)
    height.print()
    print()

    height = Height()
    height.set_metric(193)
    height.print()
    print()

    failures = 0
    tests = 0
    height = Height()
    tests += 1

    try:
        height.print()
        print("*** Error #1, should have gotten ValueError")
        failures += 1
    except Exception as e:
        print("Expected exception: ",e)
    print()

    height = Height()
    tests += 1

    try:
        height.set_english(6)
        print("Got a good height as expected (6 ft?)")
        height.print()
    except Exception as e:
        print("***Error: unexpected exception: ", e)
        failures += 1

    print()
    tests += 1

    height = Height()
    try:
        height.set_english(0, 69.0)
        print("Got a good height as expected (5' 9\" ?)")
        height.print()
    except Exception as e:
        print("*** Error: unexpected exception: ", e)
        failures += 1

    print()
    tests += 1

    height = Height()
    try:
        height.set_english(5, 9)
        print("Got a good height as expected (5' 9\" ?)")
        height.print()
    except Exception as e:
        print("***Error: unexpected exception: ", e)
        failures += 1

    print()
    tests += 1

    height = Height()
    try:
        height.set_english(5, 12)
        print("*** Error Got a good height but should not have")
        height.print()
        failures += 1
    except Exception as e:
        print("Expected exception: ", e)

    print()
    height = Height()
    tests += 1

    try:
        height.print()
        print("***Error, should have gotten exception printing height with no value")
        failures += 1
    except Exception as e:
        print("Expected exception: ", e)

    print("\n\ntest failures:", failures, "out of", tests, "tests")
