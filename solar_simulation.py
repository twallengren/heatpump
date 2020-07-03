# Author: Toren Wallengren

from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank

class SolarSimulation:
    """
    Simulation of heat pump from a cold reservoir at temperature Tc to a hot reservoir at temperature Th.

    Qc is the energy absorbed by the cold reservoir from the solar panel (and the energy extracted out of the cold
    reservoir by the pump), W is the work done by the pump, and Qh is the energy deposited into the hot reservoir.

    The 'coefficient of performance' is the ratio of benefit over cost, which in this case is Qh/W. We note that
    multiplying the coefficient of performance by the work done by the pump yields the amount of heat deposited into
    the hot reservoir.

    The first law of thermodynamics tells us Qc + W = Qh, or W = Qh - Qc so that the coefficient of performance can be
    rewritten as Qh/(Qh-Qc) or 1/(1-Qc/Qh).

    The second law of thermodynamics tells us the entropy increase of the hot reservoir must be greater than or equal to
    the entropy decrease of the cold reservoir, or Qh/Th >= Qc/Tc so Tc/Th >= Qc/Qh. So we have 1-Qc/Qh >= 1-Tc/Th, so
    1/(1-Qc/Qh) <= 1/(1-Tc/Th) = Th/(Th - Tc) which is a theoretical upper bound on the coefficient of performance.

    In this simulation, we assume heat is efficiently extracted from the cold reservoir such that its temperature Tc
    remains constant. We also assume that the pump does the same amount of work W on each cycle. The hot reservoir will
    increase in temperature as heat is pumped into it, so we assume it is a tank of water and use the known values for
    specific heat of liquid, heat of vaporization, and specific heat of gas to handle temperature/phase changes (this
    simulation only covers liquid => gas).

    We assume the pump is operating at the theoretical upper efficiency bound. So for each iteration, we multiply the
    work done by the pump by the coefficient of performance to find the energy deposited into the hot reservoir. Then we
    update the temperature of the hot reservoir which forces us to recompute the coefficient of performance before the
    next cycle.

    Since the pump uses a fixed amount of energy each cycle and we use that to compute what *should* be deposited into
    the hot reservoir, we can use the first law to say the cold reservoir must have Qc = Qh - W energy available for
    the pump to transfer heat on a given cycle. Whether or not the energy is available depends on how quickly the solar
    panel is able to absorb energy.

    All calculations are in kilograms, meters, seconds, & kelvin (so energy is in joules).

    SolarPanel (solar_panel.py) - tracks how much solar energy has been absorbed to determine whether heat transfer
                                    occurs on a given cycle.

    ColdReservoir (cold_reservoir.py) - tracks temperature (kelvin) of cold reservoir.

    Pump (pump.py) - represents energy consumption specs of pump that moves heat from cold to hot reservoir.

    StorageTank (storage_tank.py) - tracks temperature (kelvin) and heat energy added (joules) to tank of water which
                                    may undergo a liquid => gas phase transformation.
    """

    net_energy_joules = 0

    def __init__(self, solar_panel, cold_reservoir, pump, storage_tank):

        if not isinstance(solar_panel, SolarPanel):
            raise TypeError("solar_panel should be an instance of SolarPanel")
        if not isinstance(cold_reservoir, ColdReservoir):
            raise TypeError("cold_reservoir should be an instance of ColdReservoir")
        if not isinstance(pump, Pump):
            raise TypeError("pump should be an instance of Pump")
        if not isinstance(storage_tank, StorageTank):
            raise TypeError("storage_tank should be an instance of StorageTank")

        self.panel = solar_panel
        self.cold_reservoir = cold_reservoir
        self.pump = pump
        self.storage = storage_tank
        self.coefficient_of_performance = storage_tank.temp_kelvin/(storage_tank.temp_kelvin - cold_reservoir.temp_kelvin)
        self.time_elapsed_seconds = 1 / self.pump.cycles_per_second

    def iterate_cycle(self):

        # solar panel builds energy over each cycle
        self.panel.elapse_time_seconds(self.time_elapsed_seconds)

        # pump operates every cycle even if no heat transfer occurs
        self.net_energy_joules -= self.pump.energy_per_cycle_joules

        # theoretical energy that should be pumped into the hot reservoir
        energy_into_storage_joules = self.coefficient_of_performance*self.pump.energy_per_cycle_joules

        # energy required from panel to pump energy into the hot reservoir
        energy_required_from_panel_joules = energy_into_storage_joules - self.pump.energy_per_cycle_joules

        # cycle only transfers heat if the panel has absorbed the minimum required energy
        if self.panel.total_energy_absorbed_joules > energy_required_from_panel_joules:

            # drain energy from panel
            self.panel.remove_energy_joules(energy_required_from_panel_joules)

            # never needed to explicitly model energy passing through cold reservoir/pump

            # add resulting energy to storage
            self.storage.deposit_energy_joules(energy_into_storage_joules)

            # update COP because storage tank temperature is now slightly larger
            self.coefficient_of_performance = self.storage.temp_kelvin/(self.storage.temp_kelvin - self.cold_reservoir.temp_kelvin)

            # track net change in energy
            self.net_energy_joules += energy_into_storage_joules