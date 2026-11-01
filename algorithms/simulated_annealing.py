"""
algorithms/simulated_annealing.py
Stochastic optimization governed by a temperature schedule.
"""

import math
from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors
import random

class SimulatedAnnealingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.initial_temp: float = self.params.get("initial_temp", 100.0)
        self.cooling_rate: float = self.params.get("cooling_rate", 0.995)
        self.min_temp: float = self.params.get("min_temp", 1e-3)
        self.max_iterations: int = self.params.get("max_iterations", 2000)
        self.patience=  self.params.get("patience", 300)
        self.min_improvement = self.params.get("min_improvement", 0.1)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Simulated Annealing optimization.

        Guidelines:
        - Start from a high temperature where worse moves are accepted with significant probability.
        - Lower temperature over iterations according to a cooling schedule.
        - Downhill moves (improvements) must always be accepted.
        - Uphill moves (worse costs) should be accepted probabilistically according to temperature.
        - Record objective values throughout the run in self.history.

        Prohibited:
        - Ignoring the temperature parameter or turning this into pure hill climbing.
        """
        # TODO: Implement Simulated Annealing
        
        state = self.problem.generate_initial_state()
        current_cost = self.problem.evaluate(state)

        best_state=state
        best_cost=current_cost
        self.history=[best_cost]

        temp=self.initial_temp
        no_improvement_count = 0
        last_best_cost = best_cost

        for iteration in range(self.max_iterations):
            
            neighbors = get_neighbors(state, self.problem)
            if len(neighbors) ==0:
                break

            neighbor_candidate=random.choice(neighbors)
            next_cost=self.problem.evaluate(neighbor_candidate)

            if next_cost < current_cost:
                state=neighbor_candidate
                current_cost=next_cost

            elif temp > self.min_temp:
                
                delta_E = next_cost - current_cost
                probability = math.exp(-delta_E / temp)

                if random.random() < probability :
                    state=neighbor_candidate
                    current_cost=next_cost

            if current_cost < best_cost:
                best_state = state
                best_cost = current_cost

            if last_best_cost - best_cost >= self.min_improvement:
                last_best_cost = best_cost
                no_improvement_count = 0
            else:
                no_improvement_count += 1

            self.history.append(best_cost)

            if no_improvement_count >= self.patience:
                break

            temp=temp * self.cooling_rate

        return (best_state, best_cost)


       
