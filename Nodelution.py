import numpy as np
from random import random, choice
from enum import Enum

class NodeType(Enum):
    Input = 1
    Output = 2
    Hidden = 4

class Node:
    def __init__(self, id=0, type=NodeType.Hidden, inputs={}, fn=lambda x: x):
        self.id = id
        self.type = type
        self.inputs = inputs
        self.disabled = []
        self.fn = fn
        
    def __getitem__(self, key):
        return self.inputs[key]
    
    def __setitem__(self, key, value):
        self.inputs[key] = value
    
    def __len__(self):
        return len(self.inputs)

class Agent:
    def __init__(self):
        self.nodes = {}
        
    def addNode(self, node):
        self.nodes[node.id] = node
    
    def __str__(self):
        string = ""
        for node in self.nodes.values():
            string += "{}: {}\n".format(node.id, ",".join(map(str,node.inputs)))
        return string
        

class Nodelution:
    def __init__(self):
        self.Agents = [] # List of Agent
        self.test = None
        self.InputList = [1,2,3]
        self.OutpuList = [4,5]
        self.NodeCount = 5

    def setup(self):
        agent = Agent()
        
        agent.addNode(Node(1, NodeType.Input))
        agent.addNode(Node(2, NodeType.Input))
        agent.addNode(Node(3, NodeType.Input))
        
        agent.addNode(Node(4, NodeType.Output, {1: 1, 2: 1, 3: 1}))
        agent.addNode(Node(5, NodeType.Output, {1: 1, 2: 1, 3: 1}))
        
        self.test = agent
    
    def getNodeWithLinks(self, agent, disabled=True):
        while True:
            node = choice(list(agent.nodes.values()))
            if len(node.inputs) > 0:
                if not disabled:
                    if len(node.inputs) == len(node.disabled):
                        continue
                break
        return node
    
    def mutateLinkAdd(self, agent, percent=1):
        if random() > percent:
            return
        
        node_id = choice([id for id in agent.nodes.keys() if id not in self.InputList])
        if len(agent.nodes[node_id]) >= len(agent.nodes.keys())-1:
            print("Can't add a link here mate.")
            return
        
        target_link = choice([id for id in agent.nodes.keys() if id not in list(agent.nodes[node_id].inputs.keys()) + [node_id]])
        
        agent.nodes[node_id][target_link] = 1.0
    
    def mutateLinkShift(self, agent, percent=1, shift=0.2):        
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        node[choice(list(node.inputs.keys()))] += random()*shift*2 -shift
        
    def mutateLinkRandom(self, agent, percent=1):        
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        node[choice(list(node.inputs.keys()))] = random()*2 -1
    
    def mutateLinkToggle(self, agent, percent=1):           
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent)

        
        link_id = choice(list(node.inputs.keys()))
        if link_id in node.disabled:
            node.disabled.remove(link_id)
        else:
            node.disabled.append(link_id)
    
    def mutateNodeAdd(self, agent, percent=1):
        if random() > percent:
            return
        
        node = self.getNodeWithLinks(agent, False)
        
        enabled_links = [link for link in node.inputs.keys() if link not in node.disabled]
        
        link_id = choice(enabled_links)
        node.disabled.append(link_id)
        
        self.NodeCount += 1
        
        agent.addNode(Node(self.NodeCount, NodeType.Hidden, {link_id : 1}))
        node[self.NodeCount] = node[link_id]
        

nn = Nodelution()
nn.setup()

for i in range(10000):
    nn.mutateNodeAdd(nn.test)
    nn.mutateLinkToggle(nn.test)
    nn.mutateLinkShift(nn.test)
    nn.mutateLinkRandom(nn.test)
    # nn.mutateLinkAdd(nn.test)

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