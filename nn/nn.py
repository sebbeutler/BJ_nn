import numpy as np
from random import randint, random, choice
from enum import Enum
from datetime import datetime
from multipledispatch import dispatch
import math
import matplotlib
import json
from nn.Agent import Agent
from nn.Specie import Specie
from nn.Gene import Gene
from nn.Agent import Agent
from nn.Utils import *
import matplotlib.pyplot as plt

# TODO: 
# - Implement functions: (find: raise)
# - Implement tests for functions
# - Verify if we dont link nodes that dont exist               

class NN:
    def __init__(self, settings):
        self.settings = settings
        self.agents = [] # type: list[Agent]
        self.inputList = [i for i in range(settings["Input"])] # type: list[int]
        self.outputList = [i for i in range(len(self.inputList), len(self.inputList)+settings["Output"])] # type: list[int]
        self.neuronHistory = {} # type: dict[Gene, int]
        self.species = [] # type: list[Specie]
        self.maxFitness = 0.0 # type: float
        self.topAgent = None # type: Agent
        self.globalInnovations = set() # type: set[Gene]
        self.globalNeuronCount = len(self.inputList) + len(self.outputList) # type: int
    def reset(self):
        self.__init__(self.settings)
    
    def createAgent(self) -> Agent:
        agent = Agent()
        for i in self.inputList:
            for o in self.outputList:
                agent.addGene(Gene(self.newInnov(i,o),i,o,random()))
        return agent
    
    def newInnov(self, src, to):
        for gene in self.globalInnovations:
            if gene.src == src and gene.to == to:
                return gene.id
        self.globalInnovations.add(Gene(len(self.globalInnovations), src, to))
        return len(self.globalInnovations)-1

    def mutateGeneAdd(self, agent: Agent, percent=1):
        if random() > percent:
            return
        
        src = choice(list(agent.nodes))
        to = choice(list(agent.nodes))
        gene = Gene(self.newInnov(src, to), src, to)
        invGene = Gene(self.newInnov(to, src), to, src)
        
        if src == to or (src in self.inputList and to in self.inputList) or to in self.inputList or gene in agent.genes or invGene in agent.genes:
            return
                
        agent.addGene(Gene(self.newInnov(src, to), src, to))        
        
    
    # TODO: don't shift >-1 / <1
    def mutateGeneShift(self, agent: Agent, percent=1, shift=0.2) -> None:
        if random() > percent:
            return
        
        gene = choice(list(agent.genes))
        gene.weight += random()*shift*2 - shift
        
    def mutateGeneRandom(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
        gene = choice(list(agent.genes))
        gene.weight = random()*2-1
    
    def mutateGeneToggle(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
        gene = choice(list(agent.genes))
        gene.enabled = not gene.enabled
    
    def mutateNodeAdd(self, agent: Agent, percent=1) -> None:
        if random() > percent:
            return
        
        gene = choice(list(agent.genes))
        if gene in self.neuronHistory.keys():
            neuron = self.neuronHistory[gene]
        else:
            self.globalNeuronCount += 1
            self.neuronHistory[gene] = self.globalNeuronCount
            neuron = self.globalNeuronCount
        
        gene.enabled = False
        
        agent.addGene(Gene(self.newInnov(gene.src, neuron), gene.src, neuron))
        agent.addGene(Gene(self.newInnov(neuron, gene.to), neuron, gene.to, gene.weight))

    def evolve(self, fitness_goal, data, fitness_eval, plot=False):
        
        self.initializePopulation()
        
        i = 1
        fitnessHistory = []
        while self.maxFitness < fitness_goal:
            self.speciatePopulation()

            self.killAgents()

            self.produceNextGen()

            self.mutatePopulation()
            
            self.scoreFitness(data, fitness_eval)

            print("{} gen={} fit={} pop={} sp={}".format(datetime.now().strftime("[%H:%M:%S]"), i, self.maxFitness, len(self.agents), len(self.species)))
            i += 1
            
            print(len(self.topAgent.genes))
            print(len(self.topAgent.nodes))
            
            if plot:
                fitnessHistory.append(self.maxFitness)
                plt.xlim(0, 300)
                plt.ylim(0, fitness_goal)
                plt.xlabel("generations")
                plt.ylabel("fitness")
                plt.plot(fitnessHistory, color='blue')
                plt.pause(0.5)

    def initializePopulation(self) -> None:
        for i in range(self.settings["Population_Size"]):
            self.agents.append(self.createAgent())
        
        self.mutatePopulation()

    def scoreFitness(self, data, fitness_eval) -> None:
        self.maxFitness = 0
        for agent in self.agents:            
            agent.genNetwork(self.inputList, self.outputList)    
            agent.fitness = fitness_eval(agent, data)
            
            if agent.fitness > self.maxFitness:
                self.maxFitness = agent.fitness
                self.topAgent = agent
                

    def speciatePopulation(self) -> None:
        self.species = []
        self.species.append(Specie(0))
        self.species[0].addAgent(self.agents[0])
        
        for agent in self.agents[1:]:
            found_specie = False
            for specie in self.species:
                if distance(agent, specie.rep) < self.settings["Distance_Treshold"]:
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
        for specie in self.species :
            specie.agents.sort(key=lambda x: -x.fitness)
            specie.agents = specie.agents[:int(len(specie.agents)/2)]
            
        for specie in self.species.copy():
            if len(specie.agents) == 0:
                self.species.remove(specie)
    
    def produceNextGen(self) -> None:
        total_fitness = 0
        for specie in self.species:
            if specie.fitness == 0.0:
                specie.fitness = 1.0
            total_fitness += specie.fitness
        
        next_gen = []
        
        for specie in self.species:
            for i in range(int(specie.fitness / total_fitness * self.settings["Population_Size"])):
                next_gen.append(progenerate(choice(specie.agents), choice(specie.agents)))
        
        if len(next_gen) < self.settings["Population_Size"]:
            for i in range(self.settings["Population_Size"] - len(next_gen)):
                next_gen.append(progenerate(choice(self.species[0].agents), choice(self.species[0].agents)))

        self.agents = next_gen

    # TODO: multiple mutations per agent
    def mutatePopulation(self) -> None:
        for agent in self.agents:
            self.mutateGeneAdd(agent, self.settings["mGeneAdd"])
            self.mutateGeneRandom(agent, self.settings["mGeneRandom"])
            self.mutateGeneShift(agent, self.settings["mGeneShift"])
            self.mutateGeneToggle(agent, self.settings["mGeneToggle"])
            self.mutateNodeAdd(agent, self.settings["mNodeAdd"])