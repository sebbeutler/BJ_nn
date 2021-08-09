import numpy as np
from random import randint, random, choice
from enum import Enum
from datetime import datetime
from multipledispatch import dispatch
import math
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib


# TODO: 
# - Implement functions: (find: raise)
# - Implement tests for functions
# - Verify if we dont link nodes that dont exist

class Link:
    def __init__(self, src, to, weight=1.0, enabled=True) -> None:
        self.src = src
        self.to = to
        self.weight = weight
        self.enabled = enabled
    
    def copy(self):
        return Link(self.src, self.to, self.weight, self.enabled)
    
    def __str__(self) -> str:
        return "({}, {}): {}".format(self.src, self.to, self.weight)

class NodeType(Enum):
    """A type is attributed to each node for easier filtering and to differentiate hidden nodes later.
    """
    Input = 1
    Output = 2
    Hidden = 4

class Node:
    def tanh(x):
        return 2 / (1+math.exp(-2*x)) -1

    def leakyReLu(x):
        a = 0.001
        
        if x > 0.0:
            return x
        else:
            return x*a
    
    def __init__(self, id: int=0, type: NodeType=NodeType.Hidden, links=None):
        self.id = id # type: int
        self.type = type # type: NodeType
        self.links = links if links != None else [] # type: list[Link]
        self.fn = Node.leakyReLu # type: function(float)
        self.value = None # type: float
        self.buffer_value = None # type: float
        self.layer = None
        
    def getLinkFrom(self, src: int) -> Link:
        for link in self.links:
            if link.src == src:
                return link
        return None
    
    def activate(self):
        self.value = self.fn(self.buffer_value)
        
    def randomLink(self):
        if len(self.links)==0:
            return None
        return self.links[randint(0, len(self.links)-1)]

class Agent:
    def __init__(self):
        self.nodes = {} # type: dict[int, Node]
        self.fitness = 0.0 # type: float

    def addNode(self, node: Node):
        self.nodes[node.id] = node

    def addLink(self, link):
        if link.to not in self.nodes.keys():
            self.nodes[link.to] = Node(link.to)
        self.nodes[link.to].links.append(link.copy())
    
    def randomNode(self):
        return list(self.nodes.values())[randint(0, len(self.nodes.values())-1)]
    
    def clean(self):
        for node in self.nodes.values():
            node.value = None
            node.buffer_value = None
    
    def getLink(self, src, to):
        for link in self.nodes[to].links:
            if link.src == src and link.to == to:
                return link
        return None
        
class Specie:
    def __init__(self, id: int):
        self.agents = [] # type: list[Agent]
        self.fitness = 0.0 # type: float
        self.rep = None # type: Agent
    
    def addAgent(self, agent: Agent):
        if self.rep == None or agent.fitness >= self.rep.fitness:
            self.rep = agent
        self.agents.append(agent)

class Nodelution:
    def __init__(self, settings):
        self.settings = settings
        self.agents = [] # type: list[Agent]
        self.inputList = [i for i in range(1, settings["Input"]+1)] # type: list[int]
        self.outputList = [i for i in range(len(self.inputList)+1, len(self.inputList)+1+settings["Output"])] # type: list[int]
        self.nodeCount = len(self.inputList) + len(self.outputList) # type: int
        self.link_history = {} # type: dict[tuple, int]
        self.species = [] # type: list[Specie]
        self.maxFitness = 0.0 # type: float
        self.topAgent = None # type: Agent
        
    def reset(self):
        self.__init__(self.settings)
    
    def mutateLinkAdd(self, agent: Agent, percent=1):
        if random() > percent:
            return
        
        node_id = choice([id for id in agent.nodes if id not in self.inputList])
        if len(agent.nodes[node_id].links) >= len(agent.nodes)-1:
            return
        
        # All nodes except inputs and the node that own the links
        target_nodes = []
        for target_id in agent.nodes:
            if target_id != node_id and agent.nodes[node_id].getLinkFrom(target_id) == None:
                target_nodes.append(target_id)

        target_link = choice(target_nodes)
        
        agent.nodes[node_id].links.append(Link(target_link, node_id))

        return (node_id, target_link)
    
    # TODO: don't shift >-1 / <1
    def mutateLinkShift(self, agent: Agent, percent=1, shift=0.2) -> None:
        if random() > percent:
            return
        
        link = agent.randomNode().randomLink()
        if link == None:
            return
        link.weight += min(max(random()/shift*2 -shift, 0),1)
    
    def mutateLinkRandom(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        link = agent.randomNode().randomLink()
        if link == None:
            return
        link.weight = random()
    
    def mutateLinkToggle(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
        link = agent.randomNode().randomLink()
        if link == None:
            return
        link.weight = not link.enabled
    
    def mutateNodeAdd(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
        link = agent.randomNode().randomLink()
        
        if link == None or link.enabled == False:
            return
        
        link.enabled = False
        
        def quick_inc(obj, name):
            setattr(obj, name, getattr(obj, name)+1)
            return getattr(obj, name)
        
        node_id = self.link_history[(link.src, link.to)] if (link.src, link.to) in self.link_history else quick_inc(self, 'nodeCount')
        
        if (link.src, link.to) not in self.link_history:
            self.link_history[(link.src, link.to)] = node_id
        
        agent.addNode(Node(node_id))
        agent.addLink(Link(link.src, node_id, 1.0))
        agent.addLink(Link(node_id, link.to, link.weight))        
        
    def mutateNodePop(self, agent: Agent, percent=1) -> None:
        raise Exception("Not implemented func.")
    
    def mutateNodeToggle(self, agent, percent=1) -> None:
        raise Exception("Not implemented func.")

    def distance(self, agent1: Agent, agent2: Agent, c1=1.0, c2=1.0, c3=1.0) -> float:
        matching_nodes = 0
        
        matching_links = 0
        
        weight_diff = 0.0
         
        
        for node in agent1.nodes.values():
            if node.id in [n.id for n in agent2.nodes.values()]:
                matching_nodes += 1
                for link in node.links:
                    if agent2.nodes[link.to].getLinkFrom(link.src) != None:
                        matching_links += 1
                        weight_diff += abs(link.weight - agent2.getLink(link.src, link.to).weight)
                        
        
        try:
            weight_diff /= matching_links
        except ZeroDivisionError:
            weight_diff = 0.0
        
        link_count1 = 0
        for n in agent1.nodes.values():
            link_count1 += len(n.links)
            
        link_count2 = 0
        for n in agent2.nodes.values():
            link_count2 += len(n.links)   
        
        disjoint_links = link_count1 + link_count2 - 2 * matching_links
        total_links = matching_links + disjoint_links
        
        disjoint_nodes = len(agent1.nodes.values()) + len(agent2.nodes.values()) - 2 * matching_nodes
        total_nodes = matching_nodes + disjoint_nodes
        
        if total_links == 0:
            total_links = 1
        
        return disjoint_links * c1 / total_links + weight_diff * c2 + disjoint_nodes * c3 / total_nodes

    def progenerate(self, agent1: Agent, agent2: Agent) -> Agent:
        child = Agent()
        
        links = []
        for agent in [agent1, agent2]:
            for node in agent.nodes.values():
                for link in node.links:
                    links.append(link)
        
        for link in links:
            if link.to in child.nodes.keys() and child.nodes[link.to].getLinkFrom(link.src) != None:
                child.nodes[link.to].getLinkFrom(link.src).weight = (child.nodes[link.to].getLinkFrom(link.src).weight + link.weight) / 2
            else:
                child.addLink(Link(link.src, link.to, link.weight, link.enabled))
                
        for node in list(agent1.nodes.values()) + list(agent2.nodes.values()):
            if node.id not in child.nodes and len(node.links) == 0:
                child.addNode(Node(node.id, node.type))
        
        return child

    def evolve(self, max_gen=1):
        
        self.initializePopulation()
        
        for i in range(1, max_gen+1):
            self.speciatePopulation()

            self.killAgents()

            self.produceNextGen()

            self.mutatePopulation()
            
            self.scoreFitness()

            print("{} gen={} fit={} pop={} sp={}".format(datetime.now().strftime("[%H:%M:%S]"), i, self.maxFitness, len(self.agents), len(self.species)))

    def initializePopulation(self) -> None:
        for i in range(self.settings["Population_Size"]):
            self.agents.append(self.createAgent())
        
        self.mutatePopulation()
    
    def createAgent(self, empty=False) -> Agent:
        agent = Agent()
        for n in self.inputList:
            agent.addNode(Node(n, NodeType.Input))
        for n in self.outputList:
            agent.addNode(Node(n, NodeType.Output))
        if not empty:
            for i in self.inputList:
                for o in self.outputList:
                    agent.addLink(Link(i,o, random()*2-1))
        return agent
        
    def evalAgent(self, agent: Agent, input_data: list[float]) -> list[float]:
        agent.clean()
        for i in range(len(self.inputList)):
            agent.nodes[self.inputList[i]].value = input_data[i]
        
        for i in range(200):
            node: Node        
            for node in agent.nodes.values():
                node.buffer_value = 0
                for link in node.links:
                    if link.enabled:
                        if agent.nodes[link.src].value == None:
                            continue
                        node.buffer_value += agent.nodes[link.src].value * link.weight
            
            for node in agent.nodes.values():
                if node.type == NodeType.Input:
                    continue
                node.activate()
                
        return [agent.nodes[n].value for n in self.outputList]

    def scoreFitness(self) -> None:
        for agent in self.agents:
            agent.fitness = self.fitnessEval(agent)
            
            if agent.fitness > self.maxFitness:
                self.maxFitness = agent.fitness
                self.topAgent = agent
            
    def fitnessEval(self, agent):
        fitness = 0.0
        sucess = True
        
        output =  self.evalAgent(agent, [0,0])[0]
        sucess &= output <= 0.5
        fitness += 1.0 - output**2
        
        output =  self.evalAgent(agent, [1.0,1.0])[0]
        sucess &= output <= 0.5
        fitness += 1.0 - output**2
        
        output =  self.evalAgent(agent, [0,1.0])[0]
        sucess &= output > 0.5
        fitness += 1.0 - (1.0 - output)**2
        
        output =  self.evalAgent(agent, [1.0,0])[0]
        sucess &= output > 0.5
        fitness += 1.0 - (1.0 - output)**2
        
        if sucess:
            fitness += 10
        
        return fitness
                

    def speciatePopulation(self) -> None:
        self.species = []
        self.species.append(Specie(0))
        self.species[0].addAgent(self.agents[0])
        
        for agent in self.agents[1:]:
            found_specie = False
            for specie in self.species:
                if self.distance(agent, specie.rep) < self.settings["Distance_Treshold"]:
                    specie.addAgent(agent)
                    found_specie = True
            if not found_specie:
                self.species.append(Specie(len(self.species)))
                self.species[-1].addAgent(agent)
    
        for specie in self.species:
            for agent in specie.agents:
                agent.fitness /= len(specie.agents)
                specie.fitness += agent.fitness
                

    def killAgents(self) -> None:
        self.species.sort(key=lambda x: -x.fitness)
        
        selected_species = self.species[:self.settings["Species"]]
        
        for specie in selected_species:
            specie.agents.sort(key=lambda x: -x.fitness)
            specie.agents = specie.agents[:int(len(specie.agents)/2)+1]
        
        self.species = selected_species
    
    def produceNextGen(self) -> None:
        total_fitness = 0
        for specie in self.species:
            if specie.fitness == 0.0:
                specie.fitness = 1.0
            total_fitness += specie.fitness
        
        next_gen = []
        
        for specie in self.species:
            for i in range(int(specie.fitness / total_fitness * self.settings["Population_Size"])):
                next_gen.append(self.progenerate(choice(specie.agents), choice(specie.agents)))
        
        if len(next_gen) < self.settings["Population_Size"]:
            for i in range(self.settings["Population_Size"] - len(next_gen)):
                next_gen.append(self.progenerate(choice(self.species[0].agents), choice(self.species[0].agents)))
        
        self.agents = next_gen

    # TODO: multiple mutations per agent
    def mutatePopulation(self) -> None:
        for agent in self.agents:
            self.mutateLinkAdd(agent, self.settings["mLinkAdd"])
            self.mutateLinkRandom(agent, self.settings["mLinkRandom"])
            self.mutateLinkShift(agent, self.settings["mLinkShift"])
            self.mutateLinkToggle(agent, self.settings["mLinkToggle"])
            self.mutateNodeAdd(agent, self.settings["mNodeAdd"])

def plot_agent(agent):
    G = nx.DiGraph()
    
    def rec_layer(agent, nodes, layer_id):
        next_nodes = set()
        for node in nodes:
            node.layer = layer_id
            for link in node.links:
                if node.layer != None:
                    next_nodes.add(agent.nodes[link.src])
        if len(next_nodes) == 0:
            return
        rec_layer(agent, next_nodes, layer_id-1)
    
    rec_layer(agent, [agent.nodes[id] for id in nn.outputList], 100)

    first_layer = 100
    for node in agent.nodes.values():
        if node.layer < first_layer:
            first_layer = node.layer
    
    for node in agent.nodes.values():
        if node.type == NodeType.Input:
            node.layer = first_layer - 1
        elif node.type == NodeType.Output:
            node.layer = 100
    
    for node in agent.nodes.values():
        G.add_node(node.id, layer=node.layer)
    
    for link in agent.active_links:
        G.add_edge(link.src, link.to)

    pos = nx.multipartite_layout(G, subset_key="layer")

    nx.draw(G, pos, with_labels=True)
    
    plt.get_current_fig_manager().window.SetPosition((1200, 200))
    plt.show()
    plt.pause(0.001)

DefaultSettings = {
        "Input": 2,
        "Output": 1,
        "Generations": 1,
        "Population_Size": 200,
        "Species": 15,
        "Distance_Treshold": 0.7,
        
        "mLinkRandom": 0.988,
        "mLinkShift": 0.0988,
        "mLinkAdd": 0.01,
        "mLinkToggle": 0.001,
        "mNodeAdd": 0.01,
    }

def graph_mutations(agent):
    matplotlib.use("wx")
    plt.ion()
    plt.show()
    
    plot_agent(agent)
    
    while True:
        print("1: LinkAdd | 2: LinkRandom | 3: LinkShift | 4: LinkToggle | 5: NodeAdd | 0:exit")
        x = int(input("choice:"))
        plt.close()
        
        if x == 1:
            nn.mutateLinkAdd(agent)
        elif x == 2:
            nn.mutateLinkRandom(agent)
        elif x == 3:
            nn.mutateLinkShift(agent)
        elif x == 4:
            nn.mutateLinkToggle(agent)
        elif x == 5:
            nn.mutateNodeAdd(agent)
        elif x == 0:
            break
        
        plot_agent(agent)

if __name__ == '__main__':    
    nn = Nodelution(DefaultSettings)
    
    nn.evolve(100)
    
    nn.fitnessEval(nn.topAgent)
    
    print(nn.evalAgent(nn.topAgent, [0,0])[0]) # 0
    print(nn.evalAgent(nn.topAgent, [1,1])[0]) # 0
    
    print(nn.evalAgent(nn.topAgent, [1,0])[0]) # 1
    print(nn.evalAgent(nn.topAgent, [0,1])[0]) # 1
    
    # agent = nn.createAgent()
    # graph_mutations(agent)
    