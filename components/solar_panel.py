# Author: Toren Wallengren

class SolarPanel:
    """
    Represents an individual solar panel with known area & efficiency
    """

    solar_constant = 1370 # watts/meter^2
    total_energy_harvested = 0 # joules

    def __init__(self, area, efficiency):

        if area <= 0:
            raise ValueError("Solar panel area must be positive.")
        if (efficiency <= 0) | (efficiency > 1):
            raise ValueError("Solar panel efficiency must be positive and less than 1.")

        self.area = area
        self.efficiency = efficiency

    def get_time_for_energy(self, energy):
        return energy/(self.solar_constant*self.area*self.efficiency)