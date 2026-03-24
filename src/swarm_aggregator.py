import numpy as np

class SwarmAggregator:
    def __init__(self, num_agents, dim):
        self.num_agents = num_agents
        self.dim = dim
        self.positions = np.zeros((num_agents, dim))
        self.velocities = np.zeros((num_agents, dim))
        self.accelerations = np.zeros((num_agents, dim))
        self.social_weights = np.ones((num_agents, num_agents)) / (num_agents - 1)
        self.inertia_weight = 0.5
        self.cognitive_weight = 1.0
        self.social_weight = 1.0

    def update(self, local_bests, global_best):
        for i in range(self.num_agents):
            cognitive_component = self.cognitive_weight * (local_bests[i] - self.positions[i])
            social_component = self.social_weight * np.sum(self.social_weights[i] * (global_best - self.positions[i]))
            self.accelerations[i] = self.inertia_weight * self.accelerations[i] + cognitive_component + social_component
            self.velocities[i] += self.accelerations[i]
            self.positions[i] += self.velocities[i]

    def get_positions(self):
        return self.positions

    def get_global_best(self):
        return np.max(self.positions, axis=0)
