"""
algorithms/beam_search.py
Local Beam Search maintaining K parallel candidate states.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors


class LocalBeamSearchSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.beam_width: int = self.params.get("beam_width", 5)
        self.max_iterations: int = self.params.get("max_iterations", 150)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Local Beam Search.

        Guidelines:
        - Maintain a set of `beam_width` parallel configurations.
        - In each iteration, generate neighbors from all active states in the beam.
        - Pool and rank all generated successors collectively, then retain the top `beam_width` states.
        - Halt when the beam ceases to improve or reaches max_iterations.
        - Record the best cost of the population at each step in self.history.

        Encouraged:
        - Ensuring diversity across states in the beam to prevent collapse into a single redundant path.

        Prohibited:
        - Treating this as K independent, non-communicating searches.
        """


        beam_states=[]
        for _ in range(self.beam_width):
            state=self.problem.generate_initial_state()
            cost=self.problem.evaluate(state)

            beam_states.append((state,cost))

        beam_states.sort(key=lambda n:n[1])
        best_state=beam_states[0][0]
        best_cost=beam_states[0][1]

        self.history=[best_cost]

        for _ in range(self.max_iterations):

            neighbors=[]
            for state,cost in beam_states:
                neighbor=get_neighbors(state,self.problem)

                for neigh in neighbor:
                    neighbor_cost=self.problem.evaluate(neigh)
                    neighbors.append((neigh,neighbor_cost))

            if neighbors:
                neighbors.sort(key=lambda n:n[1])
                beam_states=neighbors[:self.beam_width]

                best_state_cuurent=beam_states[0][0]
                best_cost_current=beam_states[0][1]

                self.history.append(best_cost_current)

                if best_cost_current<best_cost :

                    best_state=best_state_cuurent
                    best_cost=best_cost_current
                    self.history.append(best_cost)

                else:
                    break
            else:
                break

        return best_state, best_cost
