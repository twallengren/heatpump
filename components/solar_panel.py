# Author: Toren Wallengren

from components.constants import *

class SolarPanel:
    """
    Represents an individual solar panel with known area & efficiency
    """

    total_energy_absorbed = 0 # joules

    def __init__(self, area, efficiency):

        if area <= 0:
            raise ValueError("Solar panel area must be positive.")
        if (efficiency <= 0) | (efficiency > 1):
            raise ValueError("Solar panel efficiency must be positive and less than 1.")

        self.area = area
        self.efficiency = efficiency

    def elapse_time(self, time_step):
        energy_increment = solar_constant * self.area * self.efficiency * time_step
        self.total_energy_absorbed += energy_increment
        return energy_increment

    def get_time_for_energy(self, energy):
        return energy/(solar_constant * self.area * self.efficiency)

    def remove_energy(self, energy):
        self.total_energy_absorbed -= energy