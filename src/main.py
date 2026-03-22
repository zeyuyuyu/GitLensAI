import asyncio
import random

class Agent:
    def __init__(self, id):
        self.id = id
        self.proposals = []
        self.votes = {}
        self.balance = 100

    async def propose(self, proposal):
        self.proposals.append(proposal)
        await asyncio.gather(*[agent.vote(proposal, self) for agent in agents if agent.id != self.id])

    async def vote(self, proposal, proposer):
        if proposal not in self.votes:
            self.votes[proposal] = random.choice([True, False])
            self.balance -= 10 if self.votes[proposal] else 0
            proposer.balance += 10 if self.votes[proposal] else 0

class Swarm:
    def __init__(self, num_agents):
        self.agents = [Agent(i) for i in range(num_agents)]

    async def run(self):
        while True:
            await asyncio.gather(*[agent.propose(f'Proposal {len(agent.proposals)}') for agent in self.agents])
            await asyncio.sleep(1)

if __name__ == '__main__':
    swarm = Swarm(10)
    asyncio.run(swarm.run())
