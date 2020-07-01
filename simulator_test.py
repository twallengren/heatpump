# Author: Toren Wallengren

from solar_simulation import SolarSimulation
import matplotlib.pyplot as plt

simulation = SolarSimulation()

net_energy = [simulation.net_energy]
energy_absorbed = [simulation.panel.total_energy_absorbed]
energy_harvested = [simulation.storage.energy_level]
storage_tank_temp = [simulation.storage.temp]
coefficient_of_performance = [simulation.coefficient_of_performance]
count = [0]

for idx in range(1,1000000):
    simulation.iterate_cycle()
    count.append(idx)
    net_energy.append(simulation.net_energy)
    energy_absorbed.append(simulation.panel.total_energy_absorbed)
    energy_harvested.append(simulation.storage.energy_level)
    storage_tank_temp.append(simulation.storage.temp)
    coefficient_of_performance.append(simulation.coefficient_of_performance)

net_energy_in_kj = [e/1000 for e in net_energy]
energy_absorbed_in_kj = [e/1000 for e in energy_absorbed]
energy_harvested_in_kj = [e/1000 for e in energy_harvested]
plt.subplot(141)
plt.plot(count, net_energy_in_kj)
plt.grid(True)
plt.title("Net Energy of System")
plt.xlabel("Number of Cycles")
plt.ylabel("Energy [KJ]")
plt.subplot(142)
plt.plot(count, energy_harvested_in_kj)
plt.grid(True)
plt.title("Energy in Storage Tank")
plt.xlabel("Number of Cycles")
plt.ylabel("Energy [KJ]")
plt.subplot(143)
plt.plot(count, storage_tank_temp)
plt.grid(True)
plt.title("Temperature of Storage Tank")
plt.xlabel("Number of Cycles")
plt.ylabel("Temperature [K]")
plt.subplot(144)
plt.plot(count, coefficient_of_performance)
plt.grid(True)
plt.title("Performance Coefficient")
plt.xlabel("Number of Cycles")
plt.ylabel("COP [unitless]")
plt.show()