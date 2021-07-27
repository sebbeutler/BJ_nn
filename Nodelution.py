import numpy as np
from random import random, choice
from enum import Enum
from datetime import datetime
from multipledispatch import dispatch
from itertools import zip_longest
import math
from cluster import KMeansClustering

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

class NodeType(Enum):
    """A type is attributed to each node for easier filtering and to differentiate hidden nodes later.
    """
    Input = 1
    Output = 2
    Hidden = 4

class Node:
    def __init__(self, id: int=0, type: NodeType=NodeType.Hidden, links=None, fn=lambda x: 2 / (1+math.exp(-2*x)) -1):
        self.id = id # type: int
        self.type = type # type: NodeType
        self.links = links if links != None else [] # type: list[Link]
        self.fn = fn # type: function(float)
        self.value = None # type: float
        self.buffer_value = None # type: float
        
    def getLinkFrom(self, src: int) -> Link:
        for link in self.links:
            if link.src == src:
                return link
        return None
    
    def activate(self):
        self.value = self.fn(self.buffer_value)

class Agent:
    def __init__(self):
        self.nodes = {} # type: dict[int, Node]
        self.active_links = [] # type: list[Link]
        self.inactive_links = [] # type: list[Link]
        self.fitness = 0.0 # type: float
        
    def addNode(self, node: Node):
        self.nodes[node.id] = node
        for link in node.links:
            if link.enabled:
                self.active_links.append(link)
            else:
                self.inactive_links.append(link)

    @dispatch(Link)
    def addLink(self, link):
        if link.enabled:
            self.active_links.append(link)
        else:
            self.inactive_links.append(link)
        if link.to not in self.nodes.keys():
            self.nodes[link.to] = Node(link.to)
        self.nodes[link.to].links.append(link)
    
    @dispatch(int, int, weight=float, enabled=bool)
    def addLink(self, src, to, weight=1.0, enabled=True):
        self.addLink(Link(src, to, weight, enabled))
    
    def toggleLink(self, link: Link):
        link.enabled = not link.enabled
        if link.enabled:
            self.inactive_links.remove(link)
            self.active_links.append(link)
        else:
            self.active_links.remove(link)
            self.inactive_links.append(link)
        
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
        
    def reset(self):
        self.__init__(self.settings)
    
    def mutateLinkAdd(self, agent: Agent, percent=1):
        if random() > percent:
            return
        
        node_id = choice([id for id in agent.nodes if id not in self.inputList])
        if len(agent.nodes[node_id].links) >= len(agent.nodes)-1:
            print("Can't add a link here mate.")
            return
        
        # All nodes except inputs and the node that own the links
        target_nodes = []
        for target_id in agent.nodes:
            if target_id != node_id and agent.nodes[node_id].getLinkFrom(target_id) == None:
                target_nodes.append(target_id)

        target_link = choice(target_nodes)
        
        agent.addLink(target_link, node_id)

        return (node_id, target_link)
    
    # TODO: don't shift >-1 / <1
    def mutateLinkShift(self, agent: Agent, percent=1, shift=0.2) -> None:
        if random() > percent or len(agent.active_links) == 0:
            return
        
        choice(agent.active_links).weight += random()*shift*2 -shift
    
    def mutateLinkRandom(self, agent: Agent, percent=1) -> None:
        if random() > percent or len(agent.active_links) == 0:
            return
        
        choice(agent.active_links).weight = random()*2 -1
    
    def mutateLinkToggle(self, agent: Agent, percent=1) -> None:
        if random() > percent or len(agent.active_links) == 0:
            return
        
        link = choice(agent.active_links + agent.inactive_links)
        
        agent.toggleLink(link)
    
    def mutateNodeAdd(self, agent: Agent, percent=1) -> None:
        if random() > percent or len(agent.active_links) == 0:
            return
        
        link = choice(agent.active_links)
        
        agent.toggleLink(link)
        
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
        
        links1 = [(link.src, link.to) for link in agent1.active_links + agent1.inactive_links]
        links2 = [(link.src, link.to) for link in agent2.active_links + agent2.inactive_links]
        
        for link in links1:
            if link in links2:
                matching_links += 1
                weight_diff += abs(agent1.nodes[link[1]].getLinkFrom(link[0]).weight - agent2.nodes[link[1]].getLinkFrom(link[0]).weight) 
         
        
        for node in agent1.nodes.values():
            if node.id in [n.id for n in agent2.nodes.values()]:
                matching_nodes += 1
        
        try:
            weight_diff /= matching_links
        except ZeroDivisionError:
            weight_diff = 0.0
        
        disjoint_links = len(agent1.active_links + agent1.inactive_links) + len(agent2.active_links + agent2.inactive_links) - 2 * matching_links
        total_links = matching_links + disjoint_links
        
        disjoint_nodes = len(agent1.nodes.values()) + len(agent2.nodes.values()) - 2 * matching_nodes
        total_nodes = matching_nodes + disjoint_nodes
        
        if total_links == 0:
            total_links = 1
        
        return disjoint_links * c1 / total_links + weight_diff * c2 + disjoint_nodes * c3 / total_nodes

    def progenerate(self, agent1: Agent, agent2: Agent) -> Agent:
        child = Agent()
        
        for link in agent1.active_links + agent2.active_links + agent1.inactive_links + agent2.inactive_links:
            if link.to in child.nodes.keys() and child.nodes[link.to].getLinkFrom(link.src) != None:
                child.nodes[link.to].getLinkFrom(link.src).weight = (child.nodes[link.to].getLinkFrom(link.src).weight + link.weight) / 2
            else:
                child.addLink(Link(link.src, link.to, link.weight, link.enabled))
                
        for node in list(agent1.nodes.values()) + list(agent2.nodes.values()):
            if node.id not in child.nodes and len(node.links) == 0:
                child.addNode(Node(node.id))
        
        return child

    def evolve(self, max_gen=1):
        
        self.initializePopulation()
        
        for i in range(1, max_gen+1):
            self.speciatePopulation()

            self.killAgents()

            self.produceNextGen()

            self.mutatePopulation()
            
            self.scoreFitness()

            print("{} gen={} fit={} pop={}".format(datetime.now().strftime("[%H:%M:%S]"), i, self.maxFitness, len(self.agents)))

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
                    agent.addLink(i,o)
        return agent
        
    def evalAgent(self, agent: Agent, input_data: list[float]) -> list[float]:
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
        print("Computing Fitness For All Agents")

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
        
        selected_species = []
        for i in range(self.settings["Species"]):
            selected_species.append(self.species[i])
        
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
            

DefaultSettings = {
        "Input": 2,
        "Output": 1,
        "Generations": 1,
        "Population_Size": 50,
        "Species": 8,
        "Distance_Treshold": 0.0,
        
        "mLinkAdd": 0.01,
        "mLinkRandom": 0.01,
        "mLinkShift": 0.01,
        "mLinkToggle": 0.01,
        "mNodeAdd": 0.01,
    }

if __name__ == '__main__':
    nn = Nodelution(DefaultSettings)
    nn.evolve(100)
    ()

# print([node.disabled for node in nn.test.nodes.values()])
# print(nn.test)

# import itertools
# import matplotlib.pyplot as plt
# import networkx as nx
# from networkx.drawing.nx_agraph import graphviz_layout

# G = nx.DiGraph()

# G.add_node(1, layer=0)
# G.add_node(2, layer=0)
# G.add_node(3, layer=0)
# G.add_node(4, layer=1)
# G.add_node(5, layer=1)

# for node in nn.test.nodes.values():
#     G.add_node(node.id)
#     for link in node.inputs.keys():
#         G.add_edge(link, node.id)

# pos = nx.multipartite_layout(G, subset_key="layer")

# nx.draw(G, pos, with_labels=True)
# plt.show()