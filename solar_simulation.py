# Author: Toren Wallengren

from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank

class SolarSimulation:

    def __init__(self, timestep):

        self.panel = SolarPanel(1, 0.2) # Area of 1 m^2, efficiency of 20%
        self.coldres = ColdReservoir(290) # Cold reservoir in thermal equilibrium with environment at 290K
        self.pump = Pump(1) # 1 Joule per cycle
        self.storage = StorageTank(291, 1) # Storage tank with initial temperature of 291K
        self.timestep = timestep
        self.coefficient_of_performance = 1/(self.storage.temp/self.coldres.temp - 1)

    def iterate_cycle(self):

        energy_into_storage = self.coefficient_of_performance*self.pump.energy_per_cycle
        self.storage.deposit_energy(energy_into_storage)
        self.coefficient_of_performance = 1 / (self.storage.temp / self.coldres.temp - 1)