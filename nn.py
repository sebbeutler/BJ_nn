from multipledispatch import dispatch
import random
import numpy as np


# TO DO
# - mutate on enabled connections only
# - optimize add connection mutation (get stuck in loop because the "check all possible connection" take input/output neurons onto account)

# TO IMPLEMENT 
# - NN.distance
# - NN.crossOver

class Agent:
    # NN, List of [Gene, ...]
    def __init__(self, nn, genome):
        self.NN = nn
        self.genome = genome # Dictionnary of {enabled: [[innov_id, weight], ...], disabled:[[innov_id, weight], ...]}
        self.Neurons = {} # Dictionnary of {neuron_id: [(forward_neuron_id, weight), ...]}
        self.buildNetwork(genome)
    
    def buildNetwork(self, genome):
        for gene in [gene for gene in genome if gene[2]]:
            src, to = self.NN.GlobalInnovations[gene[0]]
            if not src in self.Neurons.keys():
                self.Neurons[src] = [(to, gene[1])]
            else:
                self.Neurons[src].append((to, gene[0]))
            if not to in self.Neurons.keys():
                self.Neurons[to] = []
    
    def run(self, args):
        print("To Implement")


class NN:
    def __init__(self):
        self.GlobalInnovations = [] # List of (neuron1_id, neuron2_id)
        self.Genomes = [] # List of Genomes [ [[innov_id, weight, enabled], ...], ...]
        self.Agents = [] # List of Agents
        self.NeuronCount = 2000 # input:1-1000, output: 1001-2000
        
    def setup(self):
        genome = []
        
        genome.append([self.getInnovation(1, 1004), 0.5, True])
        genome.append([self.getInnovation(1, 1005), 0.5, True])        
        
        genome.append([self.getInnovation(2, 1004), 0.5, True])
        genome.append([self.getInnovation(2, 1005), 0.5, True])        
        
        genome.append([self.getInnovation(3, 1004), 0.5, True])
        genome.append([self.getInnovation(3, 1005), 0.5, True])
        
        # for i in range(1,1000):
        #     genome["enabled"].append([self.getInnovation(3, self.NeuronCount + i), 1])        
        # self.NeuronCount += 999
        
        self.Genomes.append(genome)
        
    @dispatch(tuple)
    def getInnovation(self, connection):
        if connection in self.GlobalInnovations:
            return self.GlobalInnovations.index(connection)
        else:
            self.GlobalInnovations.append(connection)
            return len(self.GlobalInnovations)-1
    
    @dispatch(int, int)
    def getInnovation(self, src, to):
        return self.getInnovation((src, to))
    
    def isInput(self, id):
        if id < 1000:
            return True
        return False
    
    def isOutput(self, id):
        if 1000 < id < 2000:
            return True
        return False
    
    def mutateConnectionRandom(self, genome, percent=1):
        if random.random() > percent:
            return
        
        random.choice(genome)[1] = random.random()*2 -1
    
    def mutateConnectionShift(self, genome, percent=1, shift=0.2):
        if random.random() > percent:
            return
        
        random.choice(genome)[1] += random.random()*shift*2 -shift
        
    def mutateConnectionToggle(self, genome, percent=1):
        if random.random() > percent:
            return
        g = random.choice(genome)
        g[2] = not g[2]
    
    def mutateNeuronAdd(self, genome, percent=1):
        if random.random() > percent:
            return
        
        gene = random.choice([gene for gene in genome if gene[2]])
        src, to = self.GlobalInnovations[gene[0]]  
        gene[2] = False      
        
        genome.append([self.getInnovation(src, self.NeuronCount+1), 1, True])
        genome.append([self.getInnovation(self.NeuronCount+1, to), gene[1], True])
        
        self.NeuronCount += 1
        
    def mutateConnectionAdd(self, genome, percent=1):
        if random.random() > percent:
            return
        
        connections = [self.GlobalInnovations[gene[0]] for gene in genome]
        neurons = set()
        for con in connections:
            neurons.add(con[0])
            neurons.add(con[1])
        
        # All possible connections exist already
        if (len(neurons)-1)*len(neurons) == len(connections):
            return
                
        while True:
            new_con = (random.choice(list(neurons)), random.choice(list(neurons)))
            # if the connection doesnt exist and has different neuron ids
            if new_con[0] != new_con[1] and new_con not in connections:
                # if they are not both input or both output
                if not (self.isInput(new_con[0]) and self.isInput(new_con[1])) and not (self.isOutput(new_con[0]) and self.isOutput(new_con[1])):
                    break
        genome.append([self.getInnovation(new_con), 1, True])
    
    def distance(self, g1, g2, c1, c2):        
        matching = 0
        weight_diff = 0.0
        
        for gene1 in g1:
            for gene2 in g2:
                if gene1[0] == gene2[0]:
                    matching += 1
                    weight_diff += abs(gene1[1] - gene2[1])
        weight_diff /= matching
        
        disjoint = len(g1) - matching + len(g2) - matching
        N = disjoint + matching
        
        return disjoint * c1 / N + weight_diff * c2
    
    def crossOver(self, g1, g2, f1=1, f2=1):
        pass
            
                    

nn = NN()
nn.setup()
for i in range(10000):
    nn.mutateNeuronAdd(nn.Genomes[0], 1)
    nn.mutateConnectionToggle(nn.Genomes[0], 1)
    nn.mutateConnectionShift(nn.Genomes[0], 1)
    nn.mutateConnectionRandom(nn.Genomes[0], 1)
    # nn.mutateConnectionAdd(nn.Genomes[0], 1)
