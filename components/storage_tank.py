# Author: Toren Wallengren

class StorageTank:
    """
    Represents tank of water to store heat energy.
    """

    energy_level = 0
    freezing_temp = 273.1 # kelvin
    boiling_temp = 373.1 # kelvin
    specific_heat_liquid = 4186 # joule/kg
    specific_heat_gas = 1996 # joule/kg
    heat_of_vap = 2260000 # joule/kg
    vap_heat_added = 0 # joule

    def __init__(self, initial_temperature, kilos_of_water):

        # check for acceptable method parameters
        if initial_temperature <= self.freezing_temp:
            raise ValueError("Initial temperature of storage tank must be greater than 273.1 K.")
        if kilos_of_water <= 0:
            raise ValueError("Amount of water in storage tank must be positive.")

        # determine state of system
        if initial_temperature < self.boiling_temp:
            self.state = "liquid"
            self.heatcap = self.specific_heat_liquid * kilos_of_water
        elif initial_temperature == self.boiling_temp:
            self.state = "vaporizing"
            self.heatcap = self.heat_of_vap * kilos_of_water
        else:
            self.state = "gas"
            self.heatcap = self.specific_heat_gas * kilos_of_water

        # set remaining instance variables
        self.temp = initial_temperature
        self.kilos = kilos_of_water

    def deposit_energy(self, energy):

        self.energy_level += energy

        if (self.state == "liquid") | (self.state == "gas"):
            self.temp = (energy + self.heatcap*self.temp)/self.heatcap
            if self.temp >= self.boiling_temp:
                self.state = "vaporizing"
                self.heatcap = self.heat_of_vap * self.kilos
        else:
            self.vap_heat_added += energy
            if self.vap_heat_added >= self.heatcap:
                self.state = "gas"
                self.heatcap = self.specific_heat_gas * self.kilos