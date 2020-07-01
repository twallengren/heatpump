# Author: Toren Wallengren

class StorageTank:

    energy_level = 0

    def __init__(self, initial_temperature, kilos_of_water):

        self.temp = initial_temperature
        self.heatcap = 4186*kilos_of_water # specific heat of water is 4186 joule/kg

    def deposit_energy(self, energy):

        self.energy_level += energy
        self.temp = (energy + self.heatcap*self.temp)/self.heatcap