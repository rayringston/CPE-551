import numpy as np
import pandas as pd
from component import Component


class LCCircuit:
    def __init__(self, L, C):
        self.inductor = Component("Inductor", L)
        self.capacitor = Component("Capacitor", C)

    def __str__(self):
        return f"{self.inductor}\n{self.capacitor}"

    def __len__(self):
        if hasattr(self, "simTime") and hasattr(self, "timestep"):
            return int(self.simTime / self.timestep)
        else: 
            return 0

    def exportToExcel(self, filename, simTime):
        try:
            time = np.arange(0, simTime, self.timestep)

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

    def addParallelCapacitor(self, extraC):
        c1 = Component("Capacitor", self.capacitor.value)
        c2 = Component("Capacitor", extraC)
        self.capacitor = c1 + c2

    def stepTime(self, dt):
        dI = -self.capacitor.charge / (self.inductor.value * self.capacitor.value) * dt
        self.inductor.current += dI
        self.capacitor.charge += self.inductor.current * dt

    def simulate(self, simTime, dt):
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
        signs = np.sign(self.voltages)
        zeroCrossings = signs[:-1] * signs[1:] < 0

        crossingIndices = []

        for i, change in enumerate(zeroCrossings):
            if change:
                crossingIndices.append(i)

        periods = []

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
