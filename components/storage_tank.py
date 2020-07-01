# Author: Toren Wallengren

from components.constants import *

class StorageTank:
    """
    Represents tank of water to store heat energy.
    """

    energy_level = 0 # joules
    vap_heat_added = 0 # joules

    def __init__(self, initial_temperature, kilos_of_water):

        # check for acceptable method parameters
        if initial_temperature <= freezing_temp:
            raise ValueError(f'Initial temperature of storage tank must be greater than {freezing_temp} K.')
        if kilos_of_water <= 0:
            raise ValueError("Amount of water in storage tank must be positive.")

        # determine state of system
        if initial_temperature < boiling_temp:
            self.state = LIQUID
            self.heatcap = specific_heat_liquid * kilos_of_water
        elif initial_temperature == boiling_temp:
            self.state = VAPORIZING
            self.heatcap = heat_of_vap * kilos_of_water
        else:
            self.state = GAS
            self.heatcap = specific_heat_gas * kilos_of_water

        # set remaining instance variables
        self.temp = initial_temperature
        self.kilos = kilos_of_water

    def deposit_energy(self, energy):

        self.energy_level += energy

        if (self.state == LIQUID) | (self.state == GAS):
            self.temp = (energy + self.heatcap * self.temp) / self.heatcap
            if self.temp >= boiling_temp:
                self.temp = boiling_temp
                self.state = VAPORIZING
                self.heatcap = heat_of_vap * self.kilos
        else:
            self.vap_heat_added += energy
            if self.vap_heat_added >= self.heatcap:
                self.state = GAS
                self.heatcap = specific_heat_gas * self.kilos