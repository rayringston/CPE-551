"""
Authors: Andrea Antropow & Ray Ringston
Contact: aantrop1@stevens.edu & rringsto@stevens.edu
Filename: main.ipynb
"""
import numpy as np
import matplotlib.pyplot as plt
import pytest

# imports our classes lc_circuit and component
from lc_circuit import LCCircuit
from component import Component

def main():

    try:
        # prompts user to enter Inductance, Capacitance, Initial charge, Initial current, Simulatation time, and Time step. 
        print("Enter the following values: ")
        L = float(input("\tInductance (H): "))
        C = float(input("\tCapacitance (F): "))

        initialcharge = float(input("\tInitial charge (C): "))
        initialcurrent = float(input("\tInitial current (A): "))

        simTime = float(input("\tSimulation time (s): "))
        dt = float(input("\tTime step (s): "))

        # checks if inductance and capacitance are positive values. Raises an error if they are not. 
        if L <= 0 or C <= 0:
            raise ValueError("Inductance and capacitance must be positive.")
        # checks if simulation time and time step are positive values. Raises an error if they are not. 
        if dt <= 0 or simTime <= 0:
            raise ValueError("Time and time step must be positive.")

        # checks if Time step is smaller than the simulation time. Raises an error if it is not. 
        if dt > simTime:
            raise ValueError("Time step must be smaller than simulation time.")
            
    # Handles invalid numeric or circuit value inputs
    except ValueError as e:
        print(f"Input Error: {e}")
        return

    else:
        # Creates a baseline LC circuit object
        lc1 = LCCircuit(L, C)

        # sets initial conditons based on user input
        lc1.setInitialConditions(initialcharge, initialcurrent)

        # runs simulation and performs waveform analysis
        lc1.simulate(simTime, dt)
        lc1.analyze()

        # creates a NumPy array of time values for plotting
        time = np.arange(0, simTime, dt)

        # plots voltage and current for the baseline circuit
        plt.plot(time, lc1.voltages, label="Voltage (baseline)")
        plt.plot(time, lc1.currents, label="Current (baseline)")

        # labels for graph
        plt.xlabel("Time (s)")
        plt.ylabel("Value")
        plt.legend()
        plt.title("Baseline LC Circuit")
        plt.show()

        # initializes second circuit variable for later comparison.
        lc2 = None

        # asks user if they want to add parallel capacitor
        choice = input("\nAdd parallel capacitor and re-analyze? (Y/N): ").lower().strip()

        if choice == "y":
            # prompts user to enter the extra capacitor value
            extraC = float(input("\tExtra capacitance (F): "))

            # Creates capacitor component objects.
            c1 = Component("Capacitor", C)
            c2 = Component("Capacitor", extraC)

            # combines both capacitances in parallel
            newC = (c1 + c2).value

            # creates a modified LC circuit with the new capacitance.
            lc2 = LCCircuit(L, newC)

            # sets initial conditions
            lc2.setInitialConditions(initialcharge, initialcurrent)

            # simulates and analyzes the modified circuit.
            lc2.simulate(simTime, dt)
            lc2.analyze()

            # plots voltage and current for the modified circuit.
            plt.plot(time, lc2.voltages, label="Voltage (modified)")
            plt.plot(time, lc2.currents, label="Current (modified)")

            # labels for graph
            plt.xlabel("Time (s)")
            plt.ylabel("Value")
            plt.legend()
            plt.title("Modified LC Circuit")
            plt.show()

        # Asks user is they would like to export the data to excel
        saveChoice = input(f"\nWould you like to export the waveform data to Excel? \nThe expected length of the sheet will be {len(lc1)}: (Y/N): ").lower().strip()

        # if user enters yes or y then asks the user for filename. 
        if saveChoice == "yes" or saveChoice == "y":

            filename = input("Enter Excel filename: ")

            # if the user does not enter .xlsx at the end of the file name add it
            if not filename.endswith(".xlsx"):
                filename += ".xlsx"

            # exports baseline circuit data
            lc1.exportToExcel(filename.replace(".xlsx", "_baseline.xlsx"), simTime)

            # if user added second capacitor exports baseline circuit data
            if lc2 is not None:
                lc2.exportToExcel(filename.replace(".xlsx", "_modified.xlsx"), simTime)


# runs the program only when this file is executed directly
if __name__ == "__main__":
    main()
