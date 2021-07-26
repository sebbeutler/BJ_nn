import numpy as np
from random import random, choice
from enum import Enum
from datetime import datetime
from multipledispatch import dispatch

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
    """Represent a single Node of a network.

    Attributes:
        id: Unique identifier (int).
        type: cf. Nodetype.
        inputs: Collection of all the parent nodes and the weight of their link to this node.
                Form: {node_id: weight_value, ...}
        disabled: List of existing links that are toggled off (wont be processed on evaluation of the agent).
        fn: Activation function.
    
    Methodes:
        __getitem__, __setitem__, __len__: Shortcut to self.inputs.
                                           Node[i] / len(Node) will act like Node.inputs[i] / len(Node.inputs).
    """
    def __init__(self, id: int=0, type: NodeType=NodeType.Hidden, links=[], fn=lambda x: x):
        self.id = id # type: int
        self.type = type # type: NodeType
        self.links = links
        self.fn = fn # type: function(float)
        
    def getLinkFrom(self, src):
        for link in self.links:
            if link.src == src:
                return link
        return None

class Agent:
    """Represent an individual of the population.
    

    Attributes:
        nodes: Collection of the Nodes forming the network.
            For easier usage, use Agent.addNode(Node) to add a Node to the agent.
            Form: {node_id: Node, ...}
    
    Methods:
        addNode: Add a node to the nodes collection and use the node.id as index for the dictionnary.
    """
    def __init__(self):
        self.nodes = {} # type: dict[int, Node]
        self.active_links = []
        self.inactive_links = []
        
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
        self.nodes[link.to].links.append(link)
    
    @dispatch(int, int, weight=float, enabled=bool)
    def addLink(self, src, to, weight=1.0, enabled=True):
        self.addLink(Link(src, to, weight, enabled))
        

class Nodelution:
    def __init__(self, settings):
        self.agents = [] # type: list[Agent]
        self.inputList = [i for i in range(1, settings["Input"]+1)] # type: list[int]
        self.outputList = [i for i in range(len(self.inputList)+1, len(self.inputList)+1+settings["Output"])] # type: list[int]
        self.nodeCount = len(self.inputList) + len(self.outputList) # type: int

    def setup(self):
        pass
    
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
    
    def mutateLinkShift(self, agent: Agent, percent=1, shift=0.2) -> None:        
        if random() > percent:
            return
        
        choice(agent.active_links).weight += random()*shift*2 -shift
        
    def mutateLinkRandom(self, agent: Agent, percent=1) -> None:        
        if random() > percent:
            return
        
        choice(agent.active_links).weight = random()*2 -1
    
    def mutateLinkToggle(self, agent: Agent, percent=1) -> None:           
        if random() > percent:
            return
        
        link = choice(agent.active_links + agent.inactive_links)
        link.enabled = not link.enabled

        if link.enabled:
            agent.inactive_links.remove(link)
            agent.active_links.append(link)
        else:
            agent.active_links.remove(link)
            agent.inactive_links.append(link)
    
    def mutateNodeAdd(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
    def mutateNodePop(self, agent: Agent, percent=1) -> None:
        raise Exception("Not implemented func.")
    
    def mutateNodeToggle(self, agent, percent=1) -> None:
        raise Exception("Not implemented func.")

    def distance(self, agent1, agent2) -> float:
        raise Exception("Not implemented func.")

    def progenerate(self, agent1, agent2) -> Agent:
        raise Exception("Not implemented func.")

    def evolve(self, max_gen=1):
        
        self.initializePopulation()
        self.scoreFitness()
        
        for i in range(1, max_gen+1):
            self.speciatePopulation()

            self.adjustFitness()

            self.killAgents()

            self.produceNextGen()

            self.mutatePopulation()
            
            self.scoreFitness()

            print("{} gen={} fit={} pop={}".format(datetime.now().strftime("[%H:%M:%S]"), i, 0, len(self.agents)))

    def initializePopulation(self) -> None:
        print("Generating Initial Population")
    
    def scoreFitness(self) -> None:
        print("Computing Fitness For All Agents")

    def speciatePopulation(self) -> None:
        print("Speciating Population")
    
    def adjustFitness(self) -> None:
        print("Adjusting fitness")

    def killAgents(self) -> None:
        print("Kill weak agents")
    
    def produceNextGen(self) -> None:
        print("Produce new generation")
    
    def mutatePopulation(self) -> None:
        print("Apply mutations")

DefaultSettings = {
        "Input": 3,
        "Output": 2,
        "Generations": 1
    }

if __name__ == '__main__':
    nn = Nodelution(DefaultSettings)
    # nn.evolve(100)

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