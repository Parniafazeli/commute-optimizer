"""
algorithms/hill_climbing.py
Hill Climbing search with sideways move limits and random restarts.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors
import random

class HillClimbingSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.max_sideways: int = self.params.get("max_sideways", 100)
        self.max_restarts: int = self.params.get("max_restarts", 5)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Hill Climbing optimization.

        Guidelines:
        - Search through the neighborhood greedily for candidates that minimize total travel time.
        - Handle flat local maxima / shoulders by allowing up to `max_sideways` non-improving steps.
        - Apply up to `max_restarts` to explore different starting basins.
        - Track the best objective cost seen at each major step in self.history.

        Prohibited:
        - Looping indefinitely on flat plateaus.
        """
        best_state=self.problem.generate_initial_state()
       
        best_cost=self.problem.evaluate(best_state)
       
        self.history = [best_cost]

        for restart in range(self.max_restarts + 1):
            state=self.problem.generate_initial_state()

            if restart>0:
                neighbors = get_neighbors(state, self.problem)
                if len(neighbors)>0:
                    state = random.choice(neighbors)

            current_cost = self.problem.evaluate(state)
            if current_cost < best_cost:
                best_state = state
                best_cost = current_cost

            self.history.append(best_cost)
            sideaway=0
            while True:

                best_neighbor=None
                minimum_cost=float('inf')
                neighbors=get_neighbors(state,self.problem)

                for neighbor in neighbors:
                    cost=self.problem.evaluate(neighbor)

                    if cost < minimum_cost:
                        minimum_cost=cost
                        best_neighbor=neighbor
                        

                if best_neighbor is  None:
                    break

                if minimum_cost<current_cost:
                    state=best_neighbor
                    current_cost=minimum_cost
                    sideaway=0
                elif minimum_cost==current_cost:
                    if sideaway < self.max_sideways:
                        sideaway+=1
                        state=best_neighbor
                    else:
                        break
                else:
                    break

                if current_cost < best_cost:
                    best_state = state
                    best_cost = current_cost

                    self.history.append(best_cost)
        return (best_state,best_cost)



