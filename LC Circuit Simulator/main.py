import math
import numpy as np
import matplotlib.pyplot as plt

from lc_circuit import LCCircuit


def main():

    try:
        L = float(input("Enter inductance (H): "))
        C = float(input("Enter capacitance (F): "))
        initialcharge = float(input("Enter initial charge (C): "))
        initialcurrent = float(input("Enter initial current (A): "))
        simTime = float(input("Enter simulation time (s): "))
        dt = float(input("Enter time step (s): "))

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
        lc = LCCircuit(L, C)

        lc.setInitialConditions(initialcharge, initialcurrent)

        lc.simulate(simTime, dt)

        lc.analyze()

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

            if not filename.endswith(".xlsx"):
                filename += ".xlsx"

            lc.exportToExcel(filename, simTime)


if __name__ == "__main__":
    main()
