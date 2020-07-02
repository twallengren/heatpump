# Author: Toren Wallengren

from solar_simulation import SolarSimulation
from components.solar_panel import SolarPanel
from components.cold_reservoir import ColdReservoir
from components.pump import Pump
from components.storage_tank import StorageTank
import matplotlib.pyplot as plt

# Calibrated so that the solar panel always has the minimum energy for a pumping cycle
# i.e. every cycle transfers heat from the cold reservoir to the hot reservoir
def get_smooth_simulation():
    return SolarSimulation(
        SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
        ColdReservoir(290), # Cold reservoir in thermal equilibrium with environment at 290K
        Pump(4, 10), # 4 Joule per cycle, 10 cycles per second
        StorageTank(300, 1) # Storage tank of 1 kg of water with initial temperature of 300K
    )

# Calibrated so that the solar panel must absorb energy for a few cycles before there is enough energy in the
# cold reservoir for efficient heat transfer (but still yields net positive energy gain)
def get_rough_simulation():
    return SolarSimulation(
        SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
        ColdReservoir(290),  # Cold reservoir in thermal equilibrium with environment at 290K
        Pump(100, 10),  # 100 Joule per cycle, 10 cycles per second
        StorageTank(300, 1)  # Storage tank of 1 kg of water with initial temperature of 300K
    )

# Calibrated so that the pump uses more energy than is gained by the solar panel, so there is net negative energy
def get_bad_simulation():
    return SolarSimulation(
        SolarPanel(4, 0.2),  # Area of 4 m^2, efficiency of 20%
        ColdReservoir(290),  # Cold reservoir in thermal equilibrium with environment at 290K
        Pump(200, 10),  # 200 Joule per cycle, 10 cycles per second
        StorageTank(300, 1)  # Storage tank of 1 kg of water with initial temperature of 300K
    )

def run_simulation(simulation, max_temp = 500, max_cycles = 10000):

    net_energy_kilojoules = [simulation.net_energy_joules / 1000]
    energy_harvested_kilojoules = [simulation.storage.energy_level_joules / 1000]
    storage_tank_temp_kelvin = [simulation.storage.temp_kelvin]
    coefficient_of_performance = [simulation.coefficient_of_performance]
    time = [0]
    idx = 1

    while (simulation.storage.temp_kelvin < max_temp) & (idx < max_cycles):
        simulation.iterate_cycle()
        time.append(idx / simulation.pump.cycles_per_second / 60)
        net_energy_kilojoules.append(simulation.net_energy_joules / 1000)
        energy_harvested_kilojoules.append(simulation.storage.energy_level_joules / 1000)
        storage_tank_temp_kelvin.append(simulation.storage.temp_kelvin)
        coefficient_of_performance.append(simulation.coefficient_of_performance)
        idx += 1

    return time, net_energy_kilojoules, energy_harvested_kilojoules, storage_tank_temp_kelvin, coefficient_of_performance

def plot_results(fignum, suptitle, time, net_energy_in_kj, energy_harvested_in_kj, storage_tank_temp, coefficient_of_performance):

    plt.figure(fignum)
    plt.subplot(221)
    plt.plot(time, net_energy_in_kj)
    plt.grid(True)
    plt.title("Net Energy Harvested")
    plt.ylabel("Energy [KJ]")
    plt.subplot(222)
    plt.plot(time, energy_harvested_in_kj)
    plt.grid(True)
    plt.title("Energy Delta in Storage Tank")
    plt.ylabel("Energy [KJ]")
    plt.subplot(223)
    plt.plot(time, storage_tank_temp)
    plt.grid(True)
    plt.title("Temperature of Storage Tank")
    plt.xlabel("Time [minutes]")
    plt.ylabel("Temperature [K]")
    plt.subplot(224)
    plt.plot(time, coefficient_of_performance)
    plt.grid(True)
    plt.title("Performance Coefficient")
    plt.xlabel("Time [minutes]")
    plt.ylabel("COP [unitless]")
    plt.suptitle(suptitle)

if __name__ == '__main__':

    time, net, harvested, temp, cop = run_simulation(get_smooth_simulation(), max_cycles=1000000)
    plot_results(1, "Optimized Pump (through steam transition)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_smooth_simulation())
    plot_results(2, "Optimized Pump (10000 cycles)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_smooth_simulation(), max_cycles=1000)
    plot_results(3, "Optimized Pump (1000 cycles)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_rough_simulation(), max_cycles=1000000)
    plot_results(4, "Functional Pump (through steam transition)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_rough_simulation())
    plot_results(5, "Functional Pump (10000 cycles)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_rough_simulation(), max_cycles = 1000)
    plot_results(6, "Functional Pump (1000 cycles)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_bad_simulation(), max_cycles=1000000)
    plot_results(7, "Bad Pump (through steam transition)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_bad_simulation())
    plot_results(8, "Bad Pump (10000 cycles)", time, net, harvested, temp, cop)

    time, net, harvested, temp, cop = run_simulation(get_bad_simulation(), max_cycles = 1000)
    plot_results(9, "Bad Pump (1000 cycles)", time, net, harvested, temp, cop)

    plt.show()