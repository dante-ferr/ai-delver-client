from typing import TYPE_CHECKING
from .simulation import Simulation


class SimulationController:
    def __init__(self):
        self.all_simulations: list[Simulation] = []
        self.current_simulation: Simulation = Simulation()

    def start_new_simulation(self):
        self.current_simulation = Simulation()


simulation_controller = SimulationController()
