from nn.Agent import Agent

class Specie:
    def __init__(self, id: int):
        self.agents = [] # type: list[Agent]
        self.fitness = 0.0 # type: float
        self.rep = None # type: Agent
    
    def addAgent(self, agent: Agent):
        if self.rep == None or agent.fitness >= self.rep.fitness:
            self.rep = agent
        self.agents.append(agent)