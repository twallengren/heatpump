# Author: Toren Wallengren

from solar_simulation import SolarSimulation
from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank
import matplotlib.pyplot as plt

# Calibrated so that the solar panel always has the minimum energy for a pumping cycle
# i.e. every cycle transfers heat from the cold reservoir to the hot reservoir
smooth_simulation = SolarSimulation(
    SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
    ColdReservoir(290), # Cold reservoir in thermal equilibrium with environment at 290K
    Pump(3, 10), # 3 Joule per cycle, 10 cycles per second
    StorageTank(300, 1) # Storage tank of 1 kg of water with initial temperature of 300K
)

# Calibrated so that the solar panel must absorb energy for a few cycles before there is enough energy in the
# cold reservoir for efficient heat transfer (but still yields net positive energy gain)
rough_simulation = SolarSimulation(
    SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
    ColdReservoir(290), # Cold reservoir in thermal equilibrium with environment at 290K
    Pump(100, 10), # 100 Joule per cycle, 10 cycles per second
    StorageTank(300, 1) # Storage tank of 1 kg of water with initial temperature of 300K
)

# Calibrated so that the pump uses more energy than is gained by the solar panel, so there is net negative energy
bad_simulation = SolarSimulation(
    SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
    ColdReservoir(290), # Cold reservoir in thermal equilibrium with environment at 290K
    Pump(150, 10), # 150 Joule per cycle, 10 cycles per second
    StorageTank(300, 1) # Storage tank of 1 kg of water with initial temperature of 300K
)

def run_simulation(simulation, max_temp = 400, max_cycles = 1000):

    net_energy = [simulation.net_energy]
    energy_harvested = [simulation.storage.energy_level]
    storage_tank_temp = [simulation.storage.temp]
    coefficient_of_performance = [simulation.coefficient_of_performance]
    count = [0]
    idx = 1

    while (simulation.storage.temp < max_temp) & (idx < max_cycles):
        simulation.iterate_cycle()
        count.append(idx)
        net_energy.append(simulation.net_energy)
        energy_harvested.append(simulation.storage.energy_level)
        storage_tank_temp.append(simulation.storage.temp)
        coefficient_of_performance.append(simulation.coefficient_of_performance)
        idx += 1

    net_energy_in_kj = [e / 1000 for e in net_energy]
    energy_harvested_in_kj = [e / 1000 for e in energy_harvested]

    return simulation, count, net_energy_in_kj, energy_harvested_in_kj, storage_tank_temp, coefficient_of_performance

def plot_results(fignum, suptitle, count, net_energy_in_kj, energy_harvested_in_kj, storage_tank_temp, coefficient_of_performance):

    plt.figure(fignum)
    plt.subplot(221)
    plt.plot(count, net_energy_in_kj)
    plt.grid(True)
    plt.title("Net Energy Harvested")
    plt.ylabel("Energy [KJ]")
    plt.subplot(222)
    plt.plot(count, energy_harvested_in_kj)
    plt.grid(True)
    plt.title("Energy Delta in Storage Tank")
    plt.ylabel("Energy [KJ]")
    plt.subplot(223)
    plt.plot(count, storage_tank_temp)
    plt.grid(True)
    plt.title("Temperature of Storage Tank")
    plt.xlabel("Number of Cycles")
    plt.ylabel("Temperature [K]")
    plt.subplot(224)
    plt.plot(count, coefficient_of_performance)
    plt.grid(True)
    plt.title("Performance Coefficient")
    plt.xlabel("Number of Cycles")
    plt.ylabel("COP [unitless]")
    plt.suptitle(suptitle)

if __name__ == '__main__':

    smooth_simulation, count, net, harvested, temp, cop = run_simulation(smooth_simulation)
    plot_results(1, "Optimized Pump", count, net, harvested, temp, cop)

    rough_simulation, count, net, harvested, temp, cop = run_simulation(rough_simulation)
    plot_results(2, "Functional Pump", count, net, harvested, temp, cop)

    bad_simulation, count, net, harvested, temp, cop = run_simulation(bad_simulation)
    plot_results(3, "Bad Pump", count, net, harvested, temp, cop)

    plt.show()