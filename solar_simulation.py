# Author: Toren Wallengren

from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank

class SolarSimulation:

    def __init__(self):

        self.panel = SolarPanel(1, 0.2) # Area of 1 m^2, efficiency of 20%
        self.coldres = ColdReservoir(290) # Cold reservoir in thermal equilibrium with environment at 290K
        self.pump = Pump(100) # 1 Joule per cycle
        self.storage = StorageTank(300, 837200) # Storage tank of 200 kg of water with initial temperature of 291K
        self.coefficient_of_performance = 1/(self.storage.temp/self.coldres.temp - 1)

    def iterate_cycle(self):

        energy_into_storage = self.coefficient_of_performance*self.pump.energy_per_cycle
        self.storage.deposit_energy(energy_into_storage)
        self.coefficient_of_performance = 1 / (self.storage.temp / self.coldres.temp - 1)
        heat_from_panel = energy_into_storage - self.pump.energy_per_cycle
        cycle_time = self.panel.get_time_for_energy(heat_from_panel)
        return cycle_time