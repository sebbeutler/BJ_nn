from nn.Node import Node

class Agent:
    def __init__(self):
        self.genes = set()
        self.nodes = set() # type: set[Gene]
        self.fitness = 0.0 # type: float
        self.network = {}
    
    def addGene(self, gene):
        self.genes.add(gene)
        self.nodes.add(gene.src)
        self.nodes.add(gene.to)
    
    def getGene(self, id):
        for gene in self.genes:
            if gene.id == id:
                return gene
        return None
    
    def clean(self):
        for node in self.nodes.values():
            node.value = None
            node.buffer_value = None
    
    def genNetwork(self, inputs=None, outputs=None):
        self.network = {}
        for gene in self.genes:
            if not gene.enabled:
                continue
            if gene.src not in self.network.keys():
                self.network[gene.src] = Node(gene.src)
            if gene.to not in self.network.keys():
                self.network[gene.to] = Node(gene.to)
            self.network[gene.to].links.append((gene.src, gene.weight))
        
        if inputs != None:
            for i in inputs:
                if i not in self.network.keys():
                    self.network[i] = Node(i)
        if outputs != None:
            for i in outputs:
                if i not in self.network.keys():
                    self.network[i] = Node(i)
        
        if len(self.network) < 3:
            assert False