# Author: Toren Wallengren

from components.constants import freezing_temp_kelvin

class ColdReservoir:
    """
    Represents the cold reservoir that absorbs energy directly from the solar panel. We assume the temperature of this
    reservoir remains constant throughout the simulation.
    """

    def __init__(self, temp_kelvin):

        if temp_kelvin <= freezing_temp_kelvin:
            raise ValueError(f'Cold reservoir temperature_kelvin must be greater than {freezing_temp_kelvin} K.')

        self.temp_kelvin = temp_kelvin