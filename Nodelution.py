import numpy as np
from random import random, choice
from enum import Enum
from datetime import datetime

# TODO: 
# - Implement functions: (find: raise)
# - Implement tests for functions

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
    def __init__(self, id=0, type=NodeType.Hidden, inputs={}, fn=lambda x: x):
        self.id = id # type: int
        self.type = type # type: NodeType
        self.inputs = inputs # type: dict[int, float] # node_id: weight_value
        self.disabled = [] # type: list[int]
        self.fn = fn
        
    def __getitem__(self, key):
        return self.inputs[key]
    
    def __setitem__(self, key, value):
        self.inputs[key] = value
    
    def __len__(self):
        return len(self.inputs)

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
        
    def addNode(self, node):
        self.nodes[node.id] = node
    
    def __str__(self):
        string = ""
        for node in self.nodes.values():
            string += "{}: {}\n".format(node.id, ",".join(map(str,node.inputs)))
        return string
        

class Nodelution:
    def __init__(self, settings):
        self.agents = [] # type: list[Agent]
        self.test = None
        self.inputList = [i for i in range(1, settings["Input"]+1)] # type: list[int]
        self.outputList = [i for i in range(len(self.inputList)+1, len(self.inputList)+1+settings["Output"])] # type: list[int]
        self.nodeCount = len(self.inputList) + len(self.outputList) # type: int

    def setup(self):
        agent = Agent()
        
        agent.addNode(Node(1, NodeType.Input))
        agent.addNode(Node(2, NodeType.Input))
        agent.addNode(Node(3, NodeType.Input))
        
        agent.addNode(Node(4, NodeType.Output, {1: 1, 2: 1, 3: 1}))
        agent.addNode(Node(5, NodeType.Output, {1: 1, 2: 1, 3: 1}))
        
        self.test = agent
    
    # FIXME: Possible infinite loop stuck, could use some optimization as well. 
    def getNodeWithLinks(self, agent, disabled=True) -> Node:
        """Fetch randomly a node in an agent that has 1 or more links.
        If the disabled flag is set to True, the node has to have active links (not all disabled).

        Args:
            agent (Agent): Agent to select the node from.
            disabled (bool, optional): If True the node selected has to have at least 1 link enabled. Defaults to True.

        Returns:
            Node: The randomly selected node
        """
        while True:
            node = choice(list(agent.nodes.values()))
            if len(node.inputs) > 0:
                if not disabled:
                    if len(node.inputs) == len(node.disabled):
                        continue
                break
        return node
    
    def mutateLinkAdd(self, agent, percent=1) -> None:
        if random() > percent:
            return
        
        node_id = choice([id for id in agent.nodes if id not in self.InputList])
        if len(agent.nodes[node_id]) >= len(agent.nodes)-1:
            print("Can't add a link here mate.")
            return
        
        # All nodes except inputs and the node that own the links
        target_nodes = [id for id in agent.nodes if id not in list(agent.nodes[node_id].inputs) + [node_id]]

        target_link = choice(target_nodes)
        
        agent.nodes[node_id][target_link] = 1.0
    
    def mutateLinkShift(self, agent, percent=1, shift=0.2) -> None:        
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        node[choice(list(node.inputs))] += random()*shift*2 -shift
        
    def mutateLinkRandom(self, agent, percent=1) -> None:        
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        node[choice(list(node.inputs))] = random()*2 -1
    
    def mutateLinkToggle(self, agent, percent=1) -> None:           
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent)

        
        link_id = choice(list(node.inputs.keys()))
        if link_id in node.disabled:
            node.disabled.remove(link_id)
        else:
            node.disabled.append(link_id)
    
    def mutateNodeAdd(self, agent, percent=1) -> None:
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        enabled_links = [link for link in node.inputs if link not in node.disabled]
        
        link_id = choice(enabled_links)
        node.disabled.append(link_id)
        
        self.NodeCount += 1
        
        agent.addNode(Node(self.NodeCount, NodeType.Hidden, {link_id : 1}))
        node[self.NodeCount] = node[link_id]
    
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
    nn.setup()
    nn.evolve(100)

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