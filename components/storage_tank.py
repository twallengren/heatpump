# Author: Toren Wallengren

from components.constants import *

class StorageTank:
    """
    Represents tank of water to store heat energy.
    """

    energy_level_joules = 0
    vap_heat_added_joules = 0

    def __init__(self, initial_temp_kelvin, kilograms_of_water):

        # check for acceptable method parameters
        if initial_temp_kelvin <= freezing_temp_kelvin:
            raise ValueError(f'Initial temperature of storage tank must be greater than {freezing_temp_kelvin} K.')
        if kilograms_of_water <= 0:
            raise ValueError("Amount of water in storage tank must be greater than 0.")

        # determine state of system
        if initial_temp_kelvin < boiling_temp_kelvin:
            self.state = LIQUID
            self.heat_capacity = specific_heat_liquid_water * kilograms_of_water
        elif initial_temp_kelvin == boiling_temp_kelvin:
            self.state = VAPORIZING
            self.heat_capacity = heat_of_vap_water * kilograms_of_water
        else:
            self.state = GAS
            self.heat_capacity = specific_heat_gas_water * kilograms_of_water

        # set remaining instance variables
        self.temp_kelvin = initial_temp_kelvin
        self.kilograms_of_water = kilograms_of_water

    def deposit_energy_joules(self, energy_joules):

        # track total energy added
        self.energy_level_joules += energy_joules

        # liquid and gas phases update temperature using the same equation (w/ different heat capacity)
        if (self.state == LIQUID) | (self.state == GAS):

            # increase temperature based on dQ = m*C*(Tf - T0)
            self.temp_kelvin = (energy_joules + self.heat_capacity * self.temp_kelvin) / self.heat_capacity

            # check for liquid => gas phase transition
            if (self.temp_kelvin >= boiling_temp_kelvin) & (self.state == LIQUID):
                self.temp_kelvin = boiling_temp_kelvin
                self.state = VAPORIZING
                self.heat_capacity = heat_of_vap_water * self.kilograms_of_water

        # water in tank is in the process of vaporizing
        else:

            # stays in this state (at a constant temperature) until enough energy has been added
            # we track how much energy has been added while in this state with self.vap_heat_added_joules
            # the amount of energy that needs to be added before transitioning to gas is stored in self.heat_capacity
            self.vap_heat_added_joules += energy_joules
            if self.vap_heat_added_joules >= self.heat_capacity:
                self.state = GAS
                self.heat_capacity = specific_heat_gas_water * self.kilograms_of_water