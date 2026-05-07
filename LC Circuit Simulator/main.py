import numpy as np
import matplotlib.pyplot as plt
import pytest

from lc_circuit import LCCircuit
from component import Component

def main():

    try:
        print("Enter the following values: ")
        L = float(input("\tInductance (H): "))
        C = float(input("\tCapacitance (F): "))

        initialcharge = float(input("\tInitial charge (C): "))
        initialcurrent = float(input("\tInitial current (A): "))

        simTime = float(input("\tSimulation time (s): "))
        dt = float(input("\tTime step (s): "))

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
        lc1 = LCCircuit(L, C)

        lc1.setInitialConditions(initialcharge, initialcurrent)

        lc1.simulate(simTime, dt)
        lc1.analyze()

        time = np.arange(0, simTime, dt)

        plt.plot(time, lc1.voltages, label="Voltage (baseline)")
        plt.plot(time, lc1.currents, label="Current (baseline)")

        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.legend()
        plt.title("Baseline LC Circuit")
        plt.show()

        lc2 = None

        choice = input("\nAdd parallel capacitor and re-analyze? (Y/N): ").lower().strip()

        if choice == "y":
            extraC = float(input("\tExtra capacitance (F): "))

            c1 = Component("Capacitor", C)
            c2 = Component("Capacitor", extraC)

            newC = (c1 + c2).value

            lc2 = LCCircuit(L, newC)

            lc2.setInitialConditions(initialcharge, initialcurrent)

            lc2.simulate(simTime, dt)
            lc2.analyze()

            plt.plot(time, lc2.voltages, label="Voltage (modified)")
            plt.plot(time, lc2.currents, label="Current (modified)")

            plt.xlabel("Time (s)")
            plt.ylabel("Value")
            plt.legend()
            plt.title("Modified LC Circuit")
            plt.show()

        saveChoice = input(f"\nWould you like to export the waveform data to Excel? \nThe expected length of the sheet will be {len(lc1)}: (Y/N): ").lower().strip()

        if saveChoice == "yes" or saveChoice == "y":

            filename = input("Enter Excel filename: ")

            if not filename.endswith(".xlsx"):
                filename += ".xlsx"

            lc1.exportToExcel(filename.replace(".xlsx", "_baseline.xlsx"), simTime)

            if lc2 is not None:
                lc2.exportToExcel(filename.replace(".xlsx", "_modified.xlsx"), simTime)


if __name__ == "__main__":
    main()
