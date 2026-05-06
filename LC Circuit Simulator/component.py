class Component:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.current = 0
        self.charge = 0

    def __str__(self):
        if self.name == "Capacitor":
            return f"{self.name}: {self.value} F"
        elif self.name == "Inductor":
            return f"{self.name}: {self.value} H"
        else:
            return "Unknown component."
