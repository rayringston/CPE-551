"""
Authors: Andrea Antropow & Ray Ringston
Contact: aantrop1@stevens.edu & rringsto@stevens.edu
Filename: lc_circuit.py
Description:    The LCCircuit class contains the primary simulation functionality of this project. The class 
                contains 2 instances of the Component class, used to store voltage and current values much easier. 
                The LCCircuit will then use a specified time step and simulation length to run a physics simulation 
                of this circuit, saving the results. Additional methods are including to perform analysis and 
                measurements, and to save the generated wave form to an Excel file. 
"""


import numpy as np
import pandas as pd
from component import Component
import math

class LCCircuit:
    """
    This is primary class used for simulation. Important methods include the simulation execution, and the analysis of the results.
    """
    
    def __init__(self, L, C):
        """
        The LCCircuit initialization takes two parameters, L and C for the inductance and capacitance respectively.
        Two instances of the Component class are created to represent these two components.
        """
        self.inductor = Component("Inductor", L)
        self.capacitor = Component("Capacitor", C)

    def __str__(self):
        """
        Simple string overloading to print out both components.
        """
        return f"{self.inductor}\n{self.capacitor}"

    def __len__(self):
        """
        The length operator has a very specific use. After simulation has been performed, the resulting dataset will contain a large number of rows. 
        Before this is potentially saved to an Excel file, the program will print the 'length' of the LCCircuit, showing how many rows will be saved.
        """
        if hasattr(self, "simTime") and hasattr(self, "timestep"): # hasattr will return True if the listed attributes are defined for this instance
            return int(self.simTime / self.timestep)
        else: 
            return 0

    def exportToExcel(self, filename, simTime):
        """
        exportToExcel takes two input parameters, the file_name to be saved and the simulation time.
        It will attempt to save the simulated dataset to an Excel file. Listed columns are Time (s), Voltage (V), and Current (A).
        Exception handling is necessary to ensure proper file management.
        """
        try:
            time = np.arange(0, simTime, self.timestep)

            minimumLength = min(len(time), len(self.voltages), len(self.currents)) # ensures all columns are the same length

            data = pd.DataFrame({
                "Time (s)": time[:minimumLength],
                "Voltage (V)": self.voltages[:minimumLength],
                "Current (A)": self.currents[:minimumLength]
            })

            data.to_excel(filename, index=False)

            print(f"Waveform data successfully exported to {filename}.")

        except PermissionError:
            print("Error: Cannot write to the file because it is open.")

        except FileNotFoundError:
            print("Error: Invalid file path.")

        except ValueError:
            print("Error: Invalid filename or data.")

        except Exception as e:
            print(f"Export Error: {e}")

    def setInitialConditions(self, initialCharge, initialCurrent=0):
        """
        This method simply defines the intial values for the sub-components in the LCCircuit class.
        """
        self.capacitor.charge = initialCharge
        self.inductor.current = initialCurrent

    def addParallelCapacitor(self, extraC):
        """
        Uses an operator overloading of the Component class to add another capacitor in parallel to the simulated circuit.
        """
        c1 = Component("Capacitor", self.capacitor.value)
        c2 = Component("Capacitor", extraC)
        self.capacitor = c1 + c2

    def stepTime(self, dt):
        """
        Steps time forward by a specified timestep. The current flowing through the inductor depends on the voltage across the capacitor, 
        and the voltage across the capacitor depends on the charge flowing into it. The mathematical equations governing this behavoir are shown below.
        """
        # dI / dt = -Q / (L * C)
        # dI = (-Q * dt) / (L * C)
        
        dI = -self.capacitor.charge / (self.inductor.value * self.capacitor.value) * dt
        self.inductor.current += dI

        # dQ = I * dt
        
        self.capacitor.charge += self.inductor.current * dt

    def simulate(self, simTime, dt):
        """
        The simulate method takes the total simulation time and time step as parameters. It performs a simulation using Eulerian discretization, 
        a technique to replace a continuous process with a finite number of small steps in time. It iterates over these steps throughout the simulation duration, saving measurements for each step.
        """
        
        self.timestep = dt
        self.simTime = simTime
        steps = int(simTime / dt)

        self.voltages = np.zeros(steps)
        self.currents = np.zeros(steps)

        for step in range(steps):
            self.voltages[step] = self.capacitor.charge / self.capacitor.value
            self.currents[step] = self.inductor.current

            self.stepTime(dt)

    def analyze(self):
        """
        The analyze method goes through the generated waveform and calculates how often it crosses over 0. Using this, it can determine the period of the wave, and then it's frequency.
        """
        signs = np.sign(self.voltages)

        # the following lines use zero crossings to determine the frequency of the wave
        # the zeroCrossings list will contain a 1 whenever an element has a different sign then the next element
        
        zeroCrossings = signs[:-1] * signs[1:] < 0

        # using this list, we create a list showing only the indexes where a crossing occured

        crossingIndices = []
        for i, change in enumerate(zeroCrossings):
            if change:
                crossingIndices.append(i)

        # then we calculate the distance between neighbors to determine the period of each index
        
        periods = []
        for i in range(2, len(crossingIndices)):
            period = (crossingIndices[i] - crossingIndices[i - 2]) * self.timestep
            periods.append(period)

        # finally, we take the average of these periods and, calculate the frequency
        
        if periods:
            averagePeriod = sum(periods) / len(periods)
            frequency = 1 / averagePeriod

            theoreticalFrequency = 1 / (2 * math.pi * math.sqrt(self.inductor.value * self.capacitor.value))

            print(f"Simulated Resonant Frequency: {frequency} Hz")
            print(f"Theoretical Resonant Frequency: {theoreticalFrequency} Hz")
            print(f"Percent Error: {(frequency - theoreticalFrequency) / theoreticalFrequency * 100}")

            return frequency

        else:
            print("No oscillations detected.")
            return None
