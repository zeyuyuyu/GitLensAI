import numpy as np

class SwarmAggregator:
    def __init__(self, num_agents, data_dim):
        self.num_agents = num_agents
        self.data_dim = data_dim
        self.agents = [Agent(data_dim) for _ in range(num_agents)]
        self.global_best = np.zeros(data_dim)
        self.global_best_score = float('-inf')

    def aggregate(self, data_samples):
        for agent in self.agents:
            agent.update(data_samples)
            score = agent.evaluate()
            if score > self.global_best_score:
                self.global_best = agent.position.copy()
                self.global_best_score = score
        return self.global_best

class Agent:
    def __init__(self, data_dim):
        self.position = np.random.uniform(-1, 1, size=data_dim)
        self.velocity = np.zeros(data_dim)
        self.personal_best = self.position.copy()
        self.personal_best_score = float('-inf')

    def update(self, data_samples):
        c1 = 2
        c2 = 2
        w = 0.5

        for sample in data_samples:
            score = self.evaluate_sample(sample)
            if score > self.personal_best_score:
                self.personal_best = sample.copy()
                self.personal_best_score = score

            self.velocity = w * self.velocity + c1 * np.random.uniform(0, 1, size=self.data_dim) * (self.personal_best - self.position) + \
                           c2 * np.random.uniform(0, 1, size=self.data_dim) * (global_best - self.position)
            self.position += self.velocity

    def evaluate(self):
        return self.personal_best_score

    def evaluate_sample(self, sample):
        # Implement your own evaluation function here
        return np.linalg.norm(sample)