import numpy as np
from lc_circuit import LCCircuit

def test_theoretical_frequency_matches_order():
    """
    This test case measures the accuracy of the simulation prediction. 
    Using the formula for resonant frequnecy, this test will only pass if the simulation is within 1% error.
    """

    L = 0.5
    C = 0.5

    lc = LCCircuit(L, C)
    lc.setInitialConditions(1.0, 0.0)
    lc.simulate(5.0, 0.001)

    sim_freq = lc.analyze()
    theory = 1 / (2 * np.pi * np.sqrt(L * C))

    assert sim_freq is not None
    assert abs(sim_freq - theory) / theory < 0.01 # percent error < 1%
