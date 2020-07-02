# Author: Toren Wallengren

from components.constants import *

class SolarPanel:
    """
    Represents an individual solar panel with known area_sq_meters & efficiency.
    """

    total_energy_absorbed_joules = 0 # joules

    def __init__(self, area_sq_meters, efficiency):

        if area_sq_meters <= 0:
            raise ValueError("Solar panel area_sq_meters must be greater than 0.")
        if (efficiency <= 0.0) | (efficiency > 1.0):
            raise ValueError("Solar panel efficiency must be greater than 0 and less than or equal to 1.")

        self.area_sq_meters = area_sq_meters
        self.efficiency = efficiency

    def elapse_time_seconds(self, time_step):
        energy_increment_joules = solar_constant * self.area_sq_meters * self.efficiency * time_step
        self.total_energy_absorbed_joules += energy_increment_joules

    def remove_energy_joules(self, energy_joules):
        self.total_energy_absorbed_joules -= energy_joules