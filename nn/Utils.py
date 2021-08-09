from nn.Agent import Agent
from nn.Gene import Gene
from nn.Node import Node

from random import choice, random
import json
import numpy as np

import matplotlib.pyplot as plt
import networkx as nx

def distance(agent1: Agent, agent2: Agent, c1=1.0, c2=1.0, c3=0.8) -> float:
    matching = 0
    disjoint = 0
    excess = 0
    weight_diff = 0.0
    N = 0
    
    max1 = max(agent1.genes)
    max2 = max(agent2.genes)
    
    for i in range(max(max1, max2).id+1):
        g = Gene(i, None, None)
        if g in agent1.genes and g in agent2.genes:
            matching += 1
            weight_diff += abs(agent1.getGene(i).weight - agent2.getGene(i).weight)
        elif g in agent1.genes:
            if i > max2.id:
                excess += 1
            else:
                disjoint += 1
        elif g in agent2.genes:
            if i > max1.id:
                excess += 1
            else:
                disjoint += 1
    weight_diff /= matching
    N = matching + disjoint + excess
    
    x = excess * c1 / N + disjoint * c2 / N + c3 * weight_diff
    return x

# TODO: inherit weight
def progenerate(agent1: Agent, agent2: Agent) -> Agent:
    child = Agent()
    
    max1 = max(agent1.genes)
    max2 = max(agent2.genes)
    
    if agent1.fitness == agent2.fitness:
        alpha = None
    elif agent1.fitness > agent2.fitness:
        alpha = agent1
    else:
        alpha = agent2
    
    for i in range(max(max1, max2).id+1):
        g = Gene(i, None, None)
        if g in agent1.genes and g in agent2.genes:
            child.addGene(choice([agent1, agent2]).getGene(i).copy())
        elif g in agent1.genes:
            if alpha == None or alpha == agent1:
                child.addGene(agent1.getGene(i).copy())
        elif g in agent2.genes:
            if alpha == None or alpha == agent2:
                child.addGene(agent2.getGene(i).copy())
    
    return child

def evalAgent(agent: Agent, input_data: list[float], out=1) -> list[float]:
        inputList = [i for i in range(len(input_data))]
        outputList = [i for i in range(len(inputList), len(inputList)+out)]
        
        for i in range(len(input_data)):
            if i in agent.network:
                agent.network[i].value = input_data[i]
        
        for i in range(100):
            node: Node        
            for node in agent.network.values():
                node.buffer_value = 0
                for link in node.links:
                    if agent.network[link[0]].value == None:
                        continue
                    node.buffer_value += agent.network[link[0]].value * link[1]
            
            for node in agent.network.values():
                if node.id in inputList:
                    continue
                node.activate()
                
            for node in agent.network.values():
                if node.id in outputList and node.value == None:
                    node.value = 0.00
        return [np.clip(agent.network[n].value,0,1) for n in outputList if n in agent.network]

def plot_agent(nn, agent):
    agent.genNetwork(nn.inputList, nn.outputList)
    plt.close()
    plt.ion()
    plt.show()
    
    G = nx.DiGraph()
    
    def rec_layer(agent, nodes, layer_id):
        next_nodes = set()
        for node in nodes:
            node.layer = layer_id
            for link in node.links:
                if agent.network[link[0]].layer == None:
                    next_nodes.add(agent.network[link[0]])
        if len(next_nodes) == 0:
            return
        rec_layer(agent, next_nodes, layer_id-1)
    
    rec_layer(agent, [agent.network[id] for id in nn.outputList], 100)

    first_layer = 100
    for node in agent.network.values():
        if node.layer == None:
            node.layer = 100
        if node.layer < first_layer:
            first_layer = node.layer
    
    for node in agent.network.values():
        if node.id in nn.inputList:
            node.layer = first_layer - 1
        elif node.id in nn.outputList:
            node.layer = 100
    
    for node in agent.network.values():
        if node.layer != None:
            G.add_node(node.id, layer=node.layer)
    
    for gene in agent.genes:
        G.add_edge(gene.src, gene.to)

    pos = nx.multipartite_layout(G, subset_key="layer")

    nx.draw(G, pos, with_labels=True)
    
    plt.show()
    plt.pause(0.001)
    
def graph_mutations(nn, agent):
    
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
        
def save_agent(agent: Agent, filename='agent.net'):
    genes = []
    for gene in agent.genes:
        genes.append({'src': gene.src, 'to': gene.to, 'weight': gene.weight, 'enabled': gene.enabled, 'id': gene.id})
    net = json.dumps(genes, indent=4)
    
    with open(filename, 'w') as file:
        file.write(net)
    
    print(f"Saved agent at {filename} . . .")

def load_agent(filename='agent.net'):
    net = None
    agent = Agent()
    with open(filename, 'r') as file:
        net = json.loads(file.read())
    for gene in net:
        agent.addGene(Gene(gene["id"], gene["src"], gene["to"], gene["weight"], gene["enabled"]))
        
    print(f"Loaded agent from {filename} . . .")
    agent.genNetwork()
    return agent

import re

def load_sharp_agent(filename='agent.net'):
    net = None
    agent = Agent()
    gene = []
    i = 0
    with open(filename, 'r') as file:
        for line in file.readlines():
            g = re.split("\n|\t", line)[:-1]
            if len(g) == 3:
                agent.addGene(Gene(i, int(g[0]), int(g[1]), float(g[2])))
                i += 1
        
    print(f"Loaded agent from {filename} . . .")
    agent.genNetwork()
    return agent