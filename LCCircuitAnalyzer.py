import math
import numpy as np
import pandas as pd

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

    def exportToExcel(self, filename, simTime):
        try:
            time = np.arange(0, simTime, self.timestep)

            # Make sure all arrays are the same size
            minimumLength = min(len(time), len(self.voltages), len(self.currents))

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
        self.capacitor.charge = initialCharge
        self.inductor.current = initialCurrent
    
    def stepTime(self, dt):
        dI = -self.capacitor.charge / (self.inductor.value * self.capacitor.value) * dt
        self.inductor.current += dI
        self.capacitor.charge += self.inductor.current * dt

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
        signs = np.sign(self.voltages)
        zeroCrossings = signs[:-1] * signs[1:] < 0

        crossingIndices = []

        for i, change in enumerate(zeroCrossings):
            if change:
                crossingIndices.append(i)

        periods = []

        # Every two crossings = one full period
        for i in range(2, len(crossingIndices)):
            period = (crossingIndices[i] - crossingIndices[i - 2]) * self.timestep
            periods.append(period)

        if periods:
            averagePeriod = sum(periods) / len(periods)
            frequency = 1 / averagePeriod

            theoreticalFrequency = 1 / (2 * np.pi * np.sqrt(
                self.inductor.value * self.capacitor.value
            ))

            print(f"Simulated resonant frequency: {frequency} Hz")
            print(f"Theoretical resonant frequency: {theoreticalFrequency} Hz")

            return frequency

        else:
            print("No oscillations detected.")
            return None

def main():             
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

    except ValueError as e:
        print(f"Input Error: {e}")
        return

    else:
        # Create and run circuit
        lc = LCCircuit(L, C)
        lc.setInitialConditions(initialcharge, initialcurrent)
        lc.simulate(simTime, dt)
        lc.analyze()
        # Graph
        import matplotlib.pyplot as plt
        time = np.arange(0, simTime, dt)
        plt.plot(time, lc.voltages, label="Voltage (V)")
        plt.plot(time, lc.currents, label="Current (A)")

        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.legend()

        plt.show()

        saveChoice = input("Would you like to export the waveform data to Excel? (Y/N): ").lower().strip()

        if saveChoice == "yes" or saveChoice == "y":
            filename = input("Enter Excel filename: ")

            # Automatically add extension if user forgets
            if not filename.endswith(".xlsx"):
                filename += ".xlsx"

            lc.exportToExcel(filename, simTime)

if __name__ == "__main__":
    main()
