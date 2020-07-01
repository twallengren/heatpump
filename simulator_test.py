# Author: Toren Wallengren

from solar_simulation import SolarSimulation
from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank
import matplotlib.pyplot as plt

simulation = SolarSimulation(
    SolarPanel(1, 0.2),  # Area of 1 m^2, efficiency of 20%
    ColdReservoir(290), # Cold reservoir in thermal equilibrium with environment at 290K
    Pump(1, 10), # 1 Joule per cycle, 10 cycles per second
    StorageTank(300, 5) # Storage tank of 5 kg of water with initial temperature of 300K
)

net_energy = [simulation.net_energy]
energy_absorbed = [simulation.panel.total_energy_absorbed]
energy_harvested = [simulation.storage.energy_level]
storage_tank_temp = [simulation.storage.temp]
coefficient_of_performance = [simulation.coefficient_of_performance]
count = [0]
idx = 1

while (simulation.storage.temp < 400) & (idx < 10000000):
    simulation.iterate_cycle()
    count.append(idx)
    net_energy.append(simulation.net_energy)
    energy_absorbed.append(simulation.panel.total_energy_absorbed)
    energy_harvested.append(simulation.storage.energy_level)
    storage_tank_temp.append(simulation.storage.temp)
    coefficient_of_performance.append(simulation.coefficient_of_performance)
    idx += 1

net_energy_in_kj = [e/1000 for e in net_energy]
energy_absorbed_in_kj = [e/1000 for e in energy_absorbed]
energy_harvested_in_kj = [e/1000 for e in energy_harvested]
plt.subplot(141)
plt.plot(count, net_energy_in_kj)
plt.grid(True)
plt.title("Net Energy Harvested")
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