import pytest
from nn import *

class Test_NN:
    nn = NN({
        "Input": 3,
        "Output": 2,
        "Generations": 1,
        "Population_Size": 200,
        "Species": 15,
        "Distance_Treshold": 0.7,
        
        "mGeneRandom": 0.988,
        "mGeneShift": 0.0988,
        "mGeneAdd": 0.01,
        "mGeneToggle": 0.001,
        "mNodeAdd": 0.01,
    })
    def test_Gene(self):
        g1 = Gene(1,1,1)
        g2 = Gene(2,1,1)
        g3 = Gene(3,1,1)
        g4 = Gene(1,1,1)
        
        g = sorted(set([g2,g3,g1]))
        
        assert g[0] == g1
        assert g1 < g2
        assert g1 == g4
        assert g4 in g
        
        g.remove(Gene(2,1,1))
        
        assert list(g) == [g1,g3]
        
        g5 = Gene(1,1,1,10)
        g = set([g1,g3])
        
        g.add(g5)
        
        assert len(g) == 2
        assert list(g)[0].weight == 1
        assert max(g) == Gene(3,1,1)
        assert max(Gene(5,1,1), Gene(3,1,1)) == Gene(5,1,1)
        
        g.remove(g5)
        
        assert len(g) == 1
    
    def test_distance(self):
        agent1 = self.nn.createAgent()
        
        agent2 = self.nn.createAgent()
        
        for g in agent1.genes:
            g.weight = 1
        for g in agent2.genes:
            g.weight = 1
        
        N = 6
        
        assert self.nn.distance(agent1, agent2) == 0
        gene = choice(list(agent1.genes))
        gene.weight = 0
        assert self.nn.distance(agent1, agent2) == 1/N
        agent2.genes.remove(gene)
        agent2.genes.pop()
        assert self.nn.distance(agent1, agent2) == 2/N
        agent1.genes.add(Gene(self.nn.newInnov(10,10)))
        assert self.nn.distance(agent1, agent2) == 2/(N+1) + 1/(N+1)        
        gene = choice(list(agent2.genes))
        gene.weight = 0
        assert self.nn.distance(agent1, agent2) == 2/(N+1) + 1/(N+1) + 1/(N-2)     
        
        
    def test_evalAgent(self):
        self.nn.reset()
        
        def tanh(x):
            return 2 / (1+math.exp(-2*x)) -1
        
        agent = Agent()
        
        agent.addGene(Gene(1, 1, 4))
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.0,0.0])] == [0.76,0.0]
        
        agent.addGene(Gene(2, 2, 6, 0.75))
        agent.addGene(Gene(3, 6, 5, -0.25))
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.6,0.0])] == [0.76,float(str(tanh(tanh(0.6*0.75)*-0.25))[:4])]
        
        agent.addGene(Gene(4, 3, 6, -0.1))
        agent.addGene(Gene(5, 1, 6, -0.6, False))
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.6,0.2])] == [0.76,float(str(tanh(tanh(0.6*0.75+(-0.1*0.2))*-0.25))[:4])]