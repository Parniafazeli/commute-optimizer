"""
algorithms/genetic_algorithm.py
Population-based optimization using selection, recombination, and mutation.
"""

from typing import Tuple
from algorithms.base import LocalSearchSolver
from core.state import State
from core.problem import CommuteProblem
from algorithms.operators import get_neighbors, crossover
import random


class GeneticAlgorithmSolver(LocalSearchSolver):
    def __init__(self, problem: CommuteProblem, **kwargs):
        super().__init__(problem, **kwargs)
        self.population_size: int = self.params.get("population_size", 30)
        self.generations: int = self.params.get("generations", 100)
        self.crossover_rate: float = self.params.get("crossover_rate", 0.8)
        self.mutation_rate: float = self.params.get("mutation_rate", 0.2)
        self.elitism: int = self.params.get("elitism", 2)

    def solve(self) -> Tuple[State, float]:
        """
        Executes Genetic Algorithm optimization.

        Guidelines:
        - Initialize a population of valid candidate solutions.
        - Design a fitness metric suitable for minimizing commute travel time (lower cost -> higher fitness).
        - Use selection operators (such as tournament or roulette selection) to pick parents.
        - Pair parents to produce offspring via `crossover()`, and apply stochastic mutation.
        - Preserve the top candidates across generations if using elitism.
        - Track best population performance per generation in self.history.

        Encouraged:
        - Experimenting with population size, selection pressure, and operator rates to balance exploration vs. exploitation.
        """
        # TODO: Implement Genetic Algorithm

        population=[]

        for _ in range(self.population_size):
            state=self.problem.generate_initial_state()
            cost=self.problem.evaluate(state)
            population.append((state,cost))


        population.sort(key=lambda p:p[1])
        best_state=population[0][0]
        best_cost=population[0][1]

        self.history=[best_cost]

        for _ in range(self.generations):

            new_population=[]
            

            for i in range(min(self.elitism,self.population_size)):
                new_population.append(population[i])

            while len(new_population) < self.population_size:

                parent1=self.roulette_selection(population)
                parent2=self.roulette_selection(population)

                random_crossover=random.random()
                if random_crossover < self.crossover_rate :
                    child=crossover(parent1[0],parent2[0],self.problem)
                else:
                    child=parent1[0]

                ranodm_mutation=random.random()
                if ranodm_mutation < self.mutation_rate :
                    neighbors=get_neighbors(child,self.problem)
                    if neighbors:
                        child=random.choice(neighbors)


                child_cost=self.problem.evaluate(child)
                new_population.append((child,child_cost))

            population=new_population
            population.sort(key=lambda p:p[1])

            if population[0][1] < best_cost :
                best_state=population[0][0]
                best_cost=population[0][1]

            self.history.append(best_cost)
        return best_state, best_cost


    
    def roulette_selection(self,population):

        fitnesses=[]

        for state,cost in population:
            fitness=1/(cost + 1e-10)
            fitnesses.append(fitness)

        Total_fitness=sum(fitnesses)
        probilites=[]
        
        for f in fitnesses:
            probilites.append(f/Total_fitness)

        r=random.random()
        cumulative_prob = 0

        for i in range(len(population)):
            cumulative_prob+=probilites[i]

            if r <= cumulative_prob :
                return population[i]

        return population[-1]