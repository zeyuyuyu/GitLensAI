import numpy as np
from typing import List, Tuple

class SwarmAggregator:
    def __init__(self, swarm_size: int, dim: int):
        self.swarm_size = swarm_size
        self.dim = dim
        self.positions = np.random.rand(swarm_size, dim)
        self.velocities = np.zeros((swarm_size, dim))
        self.best_positions = np.copy(self.positions)
        self.best_fitness = np.zeros(swarm_size)
        self.global_best_position = np.copy(self.positions[0])
        self.global_best_fitness = self.best_fitness[0]

    def update_position(self, fitness_function) -> None:
        c1, c2 = 2, 2
        w = 0.5
        for i in range(self.swarm_size):
            r1, r2 = np.random.rand(2)
            self.velocities[i] = w * self.velocities[i] + c1 * r1 * (self.best_positions[i] - self.positions[i]) + c2 * r2 * (self.global_best_position - self.positions[i])
            self.positions[i] += self.velocities[i]
            fitness = fitness_function(self.positions[i])
            if fitness < self.best_fitness[i]:
                self.best_positions[i] = self.positions[i]
                self.best_fitness[i] = fitness
            if fitness < self.global_best_fitness:
                self.global_best_position = self.positions[i]
                self.global_best_fitness = fitness

    def optimize(self, fitness_function, max_iterations: int) -> Tuple[np.ndarray, float]:
        for _ in range(max_iterations):
            self.update_position(fitness_function)
        return self.global_best_position, self.global_best_fitness
