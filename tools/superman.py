class Superman:
    def __init__(self, name="Clark Kent"):
        self.name = name
        self.powers = ["flight", "super strength", "x-ray vision", "heat vision"]
        self.weakness = "kryptonite"
        self.is_flying = False

    def fly(self):
        self.is_flying = True
        return f"{self.name} is now flying!"

    def use_power(self, power):
        if power in self.powers:
            return f"{self.name} uses {power}!"
        return f"{self.name} doesn't have that power."

    def land(self):
        if self.is_flying:
            self.is_flying = False
            return f"{self.name} has landed."
        return f"{self.name} is already on the ground."