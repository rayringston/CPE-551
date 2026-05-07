"""
Authors: Andrea Antropow & Ray Ringston
Contact: aantrop1@stevens.edu & rringsto@stevens.edu
Filename: component.py
Description:    The component class is used to store the necessary values for the components in the LCCircuit class. 
                The LCCircuit class is composed of two Component instances, a capacitor and an inductor.
                Using a separate class allows far easier separation of the functions of both classes.
"""

class Component:
    """
    The component class is how the data for each component in a LC is stored. A component will either be an Inductor or Capacitor, and will store it's value, charge, and current.
    The addition operator and the string method were both added for use in other modules.
    """
    def __init__(self, name, value):
        """
        The __init__ method for the Component class simply initializes the attributes of the instance, based on input parameters.
        """
        self.name = name
        self.value = value
        self.current = 0
        self.charge = 0

    def __str__(self):
        """
        The __str__ method is primarly used for developers and debugging. 
        Based on which components is stored, it will prints it's type and it's value with the appropriate units.
        """
        if self.name == "Capacitor":
            return f"{self.name}: {self.value} F"
        elif self.name == "Inductor":
            return f"{self.name}: {self.value} H"
        else:
            return "Unknown component."
    
    def __add__(self, other):
        """
        The addition operator was overloaded to simulate adding additional components to the existing circuit.
        During the simulation, the user is prompted to test the effects of adding an additional capacitor, and overloading is used to update the values.
        """
        if not isinstance(other, Component):
            return NotImplemented

        if self.name != other.name:
            raise ValueError("Cannot combine different component types")

        return Component(self.name, self.value + other.value)
