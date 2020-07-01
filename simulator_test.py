# Author: Toren Wallengren

from solar_simulation import SolarSimulation
import matplotlib.pyplot as plt

simulation = SolarSimulation()

energy_harvested = [simulation.storage.energy_level]
storage_tank_temp = [simulation.storage.temp]
coefficient_of_performance = [simulation.coefficient_of_performance]
count = [0]

for idx in range(1,1000000):
    simulation.iterate_cycle()
    count.append(idx)
    energy_harvested.append(simulation.storage.energy_level)
    storage_tank_temp.append(simulation.storage.temp)
    coefficient_of_performance.append(simulation.coefficient_of_performance)

energy_in_kj = [e/1000 for e in energy_harvested]
plt.subplot(131)
plt.plot(count, energy_in_kj)
plt.grid(True)
plt.title("Energy in Storage Tank")
plt.subplot(132)
plt.plot(count, storage_tank_temp)
plt.grid(True)
plt.title("Temperature of Storage Tank")
plt.subplot(133)
plt.plot(count, coefficient_of_performance)
plt.grid(True)
plt.title("Performance Coefficient")
plt.show()