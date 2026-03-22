import random
import time
import uuid

class SwarmAgent:
    def __init__(self, id):
        self.id = id
        self.state = {
            'position': [random.uniform(-10, 10), random.uniform(-10, 10)],
            'velocity': [random.uniform(-1, 1), random.uniform(-1, 1)],
            'goal': [random.uniform(-10, 10), random.uniform(-10, 10)],
            'neighbors': []
        }

    def update(self):
        # Update position based on velocity
        self.state['position'][0] += self.state['velocity'][0]
        self.state['position'][1] += self.state['velocity'][1]

        # Adjust velocity based on goal and neighbor positions
        for neighbor in self.state['neighbors']:
            dx = neighbor['position'][0] - self.state['position'][0]
            dy = neighbor['position'][1] - self.state['position'][1]
            distance = (dx**2 + dy**2)**0.5
            self.state['velocity'][0] += dx / distance
            self.state['velocity'][1] += dy / distance
        self.state['velocity'][0] += (self.state['goal'][0] - self.state['position'][0]) * 0.1
        self.state['velocity'][1] += (self.state['goal'][1] - self.state['position'][1]) * 0.1

        # Apply friction
        self.state['velocity'][0] *= 0.95
        self.state['velocity'][1] *= 0.95

class SwarmCoordinator:
    def __init__(self, num_agents):
        self.agents = [SwarmAgent(str(uuid.uuid4())) for _ in range(num_agents)]

    def run(self, steps):
        for _ in range(steps):
            # Update agent positions and velocities
            for agent in self.agents:
                agent.update()

            # Update agent neighbor lists
            for agent in self.agents:
                agent.state['neighbors'] = [other.state for other in self.agents if other.id != agent.id and ((other.state['position'][0] - agent.state['position'][0])**2 + (other.state['position'][1] - agent.state['position'][1])**2)**0.5 < 2]

            time.sleep(0.1)

if __name__ == '__main__':
    coordinator = SwarmCoordinator(50)
    coordinator.run(100)
