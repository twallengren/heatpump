# Author: Toren Wallengren

from solar_simulation import SolarSimulation
import matplotlib.pyplot as plt

simulation = SolarSimulation()

time = [0]
energy_harvested = [simulation.storage.energy_level]
storage_tank_temp = [simulation.storage.temp]
coefficient_of_performance = [simulation.coefficient_of_performance]
count = [0]

for idx in range(1,100000):
    cycle_time = simulation.iterate_cycle()
    time.append(time[idx-1] + cycle_time)
    count.append(idx)
    energy_harvested.append(simulation.storage.energy_level)
    storage_tank_temp.append(simulation.storage.temp)
    coefficient_of_performance.append(simulation.coefficient_of_performance)

time_in_hours = [t/3600 for t in time]
energy_in_kj = [e/1000 for e in energy_harvested]
plt.subplot(231)
plt.plot(time_in_hours, energy_in_kj)
plt.subplot(232)
plt.plot(time_in_hours, storage_tank_temp)
plt.subplot(233)
plt.plot(time_in_hours, coefficient_of_performance)
plt.subplot(234)
plt.plot(count, energy_in_kj)
plt.subplot(235)
plt.plot(count, storage_tank_temp)
plt.subplot(236)
plt.plot(count, coefficient_of_performance)
plt.show()