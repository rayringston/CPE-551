# CPE-551

# _LC Circuit Simulator_

## Group Members

Ray Ringston - rringsto@stevens.edu - 20014983

Andrea Antropow: aantrop1@stevens.edu - 20010216

## Project Description

### Overview

An LC circuit, is a circuit consisting of a capacitor and an inductor, sometimes called an LC tank. The capacitor and inductor both store and release energy, and when placed together in parallel they continuously pass energy between them. These are oscillations, and the frequnecy of this oscillation for a given LC tank is called it's resonant frequency. This frequency depends solely on the capacitance and inductance of the tank, and can be calculated using this formula:

# $`f_R = \frac{1}{2\pi\sqrt{LC}}`$

The purpose of this project is not just to calculate the resonant frequency and generate the corresponding waveform. This uses the basic physical principles of inductors and capacitors to experimentally determine this frequency. We will use Euler discretization to simulate many short timesteps rather than model a continuous process. 

### Dependencies
The following Python libraries are required:  
- `math` (built-in)  
- `numpy`  
- `matplotlib`
- `pandas`

### File Structure
For this projects, the functions were split into 2 modules, `component.py` and `lc_circuit.py`, and the main file, `main.py`.

`component.py`:
- Handles initialization of components
- Distinguishes the different components in the LC Circuit

`lc_circuit.py`:
- Uses the Component class to model an LC tank
- Executes the simulation
- Perform various analysis and file handling methods
- Visualizes the results using matplotlib

`main.py`
- Handles user input for parameters
- Performs exception handling and input validation
- Controls the execution of previous modules

## Instructions to Run Program
1. Make sure Python 3 is installed on your system.

2. Install required libraries by running the following command in your terminal:
   ```bash
   pip install numpy matplotlib pandas
   ```

3. Navigate to the folder containing the program files.

4. Run the program using:

```bash
python main.py
```
5. When prompted, enter the required inputs:
     - Inductance (H)  
     - Capacitance (F)  
     - Initial Charge (C)  
     - Initial Current (A)  
     - Simulation Time (s)  
     - Time Step (s)
  
6. After entering inputs:
     - The program will display the calculated resonant frequency in the terminal
     - It will also print the theoretical value, and the simulations percent error  
     - A graph will appear showing voltage and current versus time

7. Close the graph window to continue
8. When prompted, choose to rerun the simulation after adding an additional capacitor
      - If accepted, the additional simulation will run
      - The frequency and percent of this simulation will be printed
      - Again, the current and voltage waveforms are displayed in a plot

9. Finally, you will be prompted to save these waveforms to Excel files
      - The user will again be prompted to enter a filename, where the simulation results will be saved
      - If the additional run is chosen, the two files will instead be saved as `{filename}_baseline.xlsx` `{filename}_modified.xlsx`
## Contributions
Ray Ringston
   - Implemented core classes (`Component`, `LCCircuit`)  
   - Developed simulation logic and time-stepping method  
   - Implemented waveform analysis and frequency calculation
  
Andrea Antropow
   - Assisted with system modeling and circuit theory
   - Implemented `main.py`
   - Handled user input and validation
   - Contributed to testing and debugging 
