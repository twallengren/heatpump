# Author: Toren Wallengren

class StorageTank:

    energy_level = 0

    def __init__(self, temperature, heat_capacity):

        self.temp = temperature
        self.heatcap = heat_capacity

    def deposit_energy(self, energy):

        self.energy_level += energy
        self.temp = (energy + self.heatcap*self.temp)/self.heatcap