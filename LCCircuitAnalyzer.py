import math
import numpy as np

class Component:
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.current = 0
        self.charge = 0

    def __str__(self): # print the component with units
        if self.name == "Capacitor":
            return f"{self.name}: {self.value} F"
        elif self.name == "Inductor":
            return f"{self.name}: {self.value} H"
        else:
            return "Unknown component."
    
class LCCircuit:
    def __init__(self, L, C):
        self.inductor = Component("Inductor", L)
        self.capacitor = Component("Capacitor", C)
    def __str__(self):
        return f"{self.inductor}\n{self.capacitor}"


    def setInitialConditions(self, intitialCharge, initialCurrent=0):
        self.capacitor.charge = initialCharge
        self.inductor.current = initialCurrent
    
    def stepTime(self, dt):
        #dI = -q/LC * dt
        dI = -self.capacitor.charge / (self.inductor.value * self.capacitor.value) * dt
        #dq = I * dt
        dq = self.inductor.current * dt

        self.inductor.current += dI
        self.capacitor.charge += dq

    def simulate(self, simTime, dt):
        self.timestep = dt
        steps = int(simTime / dt)

        self.voltages = np.zeros(steps)
        self.currents = np.zeros(steps)

        for step in range(steps):
            self.voltages[step] = self.capacitor.charge / self.capacitor.value
            self.currents[step] = self.inductor.current

            self.stepTime(dt)
    
    def analyze(self):
        # this list is True at any index where the voltage changes sign
        signs = np.sign(self.voltages)
        zeroCrossings = signs[:-1] * signs[1:] < 0

        lastChange = 0
        midWave = False
        periods = []
        for i, change in enumerate(zeroCrossings):
            if change:
                if midWave:
                    periods.append((i - lastChange) * self.timestep)
                    lastChange = i
                    midWave = False
                else:
                    midWave = True
        
        if periods:
            averagePeriod = sum(periods) / len(periods)
            frequency = 1 / averagePeriod
            print(f"Resonant frequency: {frequency} Hz")
            return frequency
        
        else:
            print("No oscillations detected.")
            return None
                    
try:
    # Get user input
    L = float(input("Enter inductance (H): "))
    C = float(input("Enter capacitance (F): "))
    initialcharge = float(input("Enter initial charge (C): "))
    initialcurrent = float(input("Enter initial current (A): "))
    simTime = float(input("Enter simulation time (s): "))
    dt = float(input("Enter time step (s): "))

    # Validation
    if L <= 0 or C <= 0:
        raise ValueError("Inductance and capacitance must be positive.")
    if dt <= 0 or simTime <= 0:
        raise ValueError("Time and timestep must be positive.")
    if dt > simTime:
        raise ValueError("Timestep must be smaller than simulation time.")

    # Create and run circuit
    lc = LCCircuit(L, C)
    lc.setInitialConditions(initialcharge, initialcurrent)
    lc.simulate(simTime, dt)
    lc.analyze()

except ValueError as e:
    print(f"Input Error: {e}")

import matplotlib.pyplot as plt
time = np.arange(0, initialcharge, initialcurrent)
plt.plot(time, lc.voltages, label="Voltage (V)")
plt.plot(time, lc.currents, label="Current (A)")

plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.legend()

plt.show()
