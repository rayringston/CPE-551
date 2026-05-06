# CPE-551

#_LC Circuit Simulator_

## Group Members

Ray Ringston - rringsto@stevens.edu - 20014983

Andrea Antropow: aantrop1@stevens.edu - 20010216

## Project Description

### Overview
### Dependencies
The following Python libraries are required:  
- `math` (built-in)  
- `numpy`  
- `matplotlib`

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
   pip install numpy matplotlib

3. Navigate to the folder containing the program files.

4. Run the program using:
  - `main.py`

5. When prompted, enter the required inputs:
  - Inductance (H)  
  - Capacitance (F)  
  - Initial Charge (C)  
  - Initial Current (A)  
  - Simulation Time (s)  
  - Time Step (s)
  
6. After entering inputs:
  - The program will display the calculated resonant frequency in the terminal  
  - A graph will appear showing voltage and current versus time
  - You will be prompted to save the output waveform to a .xlsx file

7. Close the graph window to end the program.
   
## Contributions
Ray Ringston
- Implemented core classes (`Component`, `LCCircuit`)  
- Developed simulation logic and time-stepping method  
- Implemented waveform analysis and frequency calculation
  
Andrea Antropow
- Assisted with system modeling and circuit theory
- Handled user input and validation
- Contributed to testing and debugging 
