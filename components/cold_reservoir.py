# Author: Toren Wallengren

from components.constants import freezing_temp

class ColdReservoir:

    def __init__(self, temperature):

        if temperature <= freezing_temp:
            raise ValueError("Cold reservoir temperature must be greater than 273.1 K.")

        self.temp = temperature