import numpy as np
from collections import deque

class SwarmAggregator:
    def __init__(self, num_agents, buffer_size=100):
        self.num_agents = num_agents
        self.buffer_size = buffer_size
        self.agent_buffers = [deque(maxlen=buffer_size) for _ in range(num_agents)]
        self.global_buffer = deque(maxlen=buffer_size)

    def add_data(self, agent_id, data):
        self.agent_buffers[agent_id].append(data)
        self.global_buffer.append(data)

    def aggregate(self):
        agent_means = [np.mean(buf) for buf in self.agent_buffers]
        global_mean = np.mean(self.global_buffer)

        # Apply swarm intelligence-based weighting
        weights = self._swarm_weights(agent_means, global_mean)
        aggregated_data = np.average(self.global_buffer, weights=weights)
        return aggregated_data

    def _swarm_weights(self, agent_means, global_mean):
        weights = []
        for mean in agent_means:
            if mean > global_mean:
                weights.append(1 + abs(mean - global_mean) / global_mean)
            else:
                weights.append(1 - abs(mean - global_mean) / global_mean)
        return weights / sum(weights)
