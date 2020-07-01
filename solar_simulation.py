# Author: Toren Wallengren

from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank

class SolarSimulation:
    """
    Simulation of heat pump from a cold reservoir at temperature Tc to a hot reservoir at temperature Th.

    Qc is the energy absorbed by the cold reservoir from the solar panel, W is the work done by the pump, and Qh is the
    energy deposited into the hot reservoir.

    The 'coefficient of performance' is the ratio of benefit over cost, which in this case is Qh/W. We note that
    multiplying the coefficient of performance by the work done by the pump yields the heat deposited.

    The first law of thermodynamics tells us Qc + W = Qh, or W = Qh - Qc so that the coefficient of performance can be
    rewritten as Qh/(Qh-Qc) or 1/(1-Qc/Qh).

    The second law of thermodynamics tells us the entropy increase of the hot reservoir must be greater than or equal to
    the entropy decrease of the cold reservoir, or Qh/Th >= Qc/Tc so Tc/Th >= Qc/Qh. So we have 1-Qc/Qh >= 1-Tc/Th, so
    1/(1-Qc/Qh) <= 1/(1-Tc/Th) = Tc/(Th - Tc) which is a theoretical upper bound on the coefficient of performance.

    In this simulation, we assume heat is efficiently extracted from the cold reservoir such that its temperature Tc
    remains constant. We also assume that the pump does the same amount of work W on each cycle. The hot reservoir will
    increase in temperature as heat is pumped into it, so we assume it is a 200kg tank of water and use the known
    specific heat capacity of water to compute the temperature increase during each cycle.

    We assume the pump is operating at the theoretical upper efficiency bound. So for each iteration, we multiply the
    work done by the pump by the coefficient of performance to find the energy deposited into the hot reservoir. Then we
    update the temperature of the hot reservoir which forces us to recompute the coefficient of performance before the
    next cycle.
    """

    def __init__(self):

        self.panel = SolarPanel(1, 0.2) # Area of 1 m^2, efficiency of 20%
        self.coldres = ColdReservoir(290) # Cold reservoir in thermal equilibrium with environment at 290K
        self.pump = Pump(100) # 100 Joules per cycle
        self.storage = StorageTank(300, 50) # Storage tank of 200 kg of water with initial temperature of 300K
        self.coefficient_of_performance = self.coldres.temp/(self.storage.temp - self.coldres.temp)

    def iterate_cycle(self):
        """

        :return: returns the time required for the solar panel in the system to harvest the energy for the current cycle
        """

        energy_into_storage = self.coefficient_of_performance*self.pump.energy_per_cycle
        self.storage.deposit_energy(energy_into_storage)
        self.coefficient_of_performance = self.coldres.temp/(self.storage.temp - self.coldres.temp)