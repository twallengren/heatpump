# Author: Toren Wallengren

from components.constants import freezing_temp

class ColdReservoir:

    def __init__(self, temperature):

        if temperature <= freezing_temp:
            raise ValueError(f'Cold reservoir temperature must be greater than {freezing_temp} K.')

        self.temp = temperature