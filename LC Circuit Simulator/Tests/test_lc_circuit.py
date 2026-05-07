import numpy as np
from lc_circuit import LCCircuit

def test_simulation_runs():
    """
    Test Simulation Runs
    This test ensures that a simulation will generate a waveform during simulation
    """
    lc = LCCircuit(0.5, 0.5)
    lc.setInitialConditions(1.0, 0.0)
    lc.simulate(1.0, 0.001)

    assert len(lc.voltages) > 0
    assert len(lc.currents) > 0


def test_frequency_reasonable():
    """
    This test ensures that the simulation analysis, the outputted frequency is within a reasonable range, defined and greater than 0.
    """
    lc = LCCircuit(0.5, 0.5)
    lc.setInitialConditions(1.0, 0.0)
    lc.simulate(5.0, 0.001)

    freq = lc.analyze()

    assert freq is not None
    assert freq > 0
    assert freq < 10
