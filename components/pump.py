# Author: Toren Wallengren

class Pump:

    def __init__(self, energy_per_cycle, cycles_per_second):

        if energy_per_cycle <= 0:
            raise ValueError("Pump energy per cycle must be positive.")
        if cycles_per_second <= 0:
            raise ValueError("Pump cycles per second must be positive.")

        self.energy_per_cycle = energy_per_cycle
        self.cycles_per_second = cycles_per_second