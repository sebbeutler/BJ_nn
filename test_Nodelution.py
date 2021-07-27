import pytest
from Nodelution import *

class Test_Nodelution:
    nn = Nodelution({
        "Input": 3,
        "Output": 2,
        "Generations": 1,
        "Population_Size": 50,
        "Species": 8,
        "Distance_Treshold": 0.0,
        
        "mLinkAdd": 0.01,
        "mLinkRandom": 0.01,
        "mLinkShift": 0.01,
        "mLinkToggle": 0.01,
        "mNodeAdd": 0.01,
    })

    def test_initNodelution(self):
        assert self.nn.inputList == [1,2,3]
        assert self.nn.outputList == [4,5]
        assert self.nn.nodeCount == 5

    def test_mutateLinkAdd(self):
        agent = self.nn.createAgent(True)

        agent.addLink(1, 4)
        agent.addLink(3, 4)
        agent.addLink(2, 5)

        assert len(agent.active_links) == 3       
        self.nn.mutateLinkAdd(agent)
        assert len(agent.active_links) == 4  

    def test_mutateLinkShift(self):
        agent = self.nn.createAgent(True)

        agent.addLink(1, 2)

        assert agent.nodes[2].links[0].weight == 1.0

        self.nn.mutateLinkShift(agent)

        assert agent.nodes[2].links[0].weight != 1.0

        assert agent.nodes[2].links[0].weight == agent.active_links[0].weight

        # TODO: test on agent without links / with all disabled links
    
    def test_mutateLinkToggle(self):
        agent = self.nn.createAgent(True)

        agent.addLink(1, 2)
        agent.addLink(4, 5)
        agent.addLink(1, 3)

        assert len(agent.active_links) == 3 and len(agent.inactive_links) == 0

        self.nn.mutateLinkToggle(agent)

        assert len(agent.active_links) == 2 and len(agent.inactive_links) == 1

        # TODO: test toggling off some links
    
    def test_mutateNodeAdd(self):
        agent = self.nn.createAgent(True)
        
        self.nn.link_history[(4,5)] = 8
        self.nn.nodeCount = 8
        
        agent.addLink(4, 5)
        
        self.nn.mutateNodeAdd(agent)
        
        assert self.nn.nodeCount == 8
        assert len(agent.nodes) == 6
        assert len(agent.active_links) == 2
        assert len(agent.inactive_links) == 1
        assert list(agent.nodes.values())[-1].id == 8
        
        self.nn.mutateNodeAdd(agent)
        
        
        assert self.nn.nodeCount == 9
        assert len(agent.nodes) == 7
        assert len(agent.active_links) == 3
        assert len(agent.inactive_links) == 2
        assert list(agent.nodes.values())[-1].id == 9
    
    def test_distance(self):
        self.nn.reset()
        
        agent1 = Agent()
        agent1.addNode(Node(1))
        agent1.addNode(Node(2))
        agent1.addNode(Node(3))
        agent1.addNode(Node(4))
        agent1.addNode(Node(5))
        agent1.addNode(Node(6))
        
        agent1.addLink(Link(1, 6))
        agent1.addLink(Link(2, 6))
        agent1.addLink(Link(3, 6))
        agent1.addLink(Link(6, 4))
        agent1.addLink(Link(6, 5))
        
        
        agent2 = Agent()
        agent2.addNode(Node(1))
        agent2.addNode(Node(2))
        agent2.addNode(Node(3))
        agent2.addNode(Node(4))
        agent2.addNode(Node(5))
        agent2.addNode(Node(6))
        agent2.addNode(Node(7))
        
        agent2.addLink(Link(1, 6))
        agent2.addLink(Link(2, 6))
        agent2.addLink(Link(6, 5, -1.0))
        
        x =self.nn.distance(agent1, agent2)
        ()
    
    def test_progenerate(self):
        self.nn.reset()
        
        agent1 = Agent()
        agent1.addNode(Node(1))
        agent1.addNode(Node(2))
        agent1.addNode(Node(3))
        agent1.addNode(Node(4))
        agent1.addNode(Node(5))
        
        agent1.addLink(1,4)
        agent1.addLink(2,5)
        
        agent2 = Agent()
        agent2.addNode(Node(1))
        agent2.addNode(Node(2))
        agent2.addNode(Node(3))
        agent2.addNode(Node(4))
        agent2.addNode(Node(5))
        agent2.addNode(Node(6))
        
        agent1.addLink(Link(1,4,0.0))
        
        
        
        child = self.nn.progenerate(agent1, agent2)
        
        assert len(child.nodes) == 6
        assert len(child.active_links) == 2
        assert child.nodes[4].getLinkFrom(1).weight == 0.5
    
    def test_initializePopulation(self):
        self.nn.reset()
        
        self.nn.initializePopulation()
        
        assert len(self.nn.agents[0].nodes) == 5
        assert len(self.nn.agents[0].active_links) == 6
        assert len(self.nn.agents) == self.nn.settings["Population_Size"]
    
    def test_evalAgent(self):
        self.nn.reset()
        
        def tanh(x):
            return 2 / (1+math.exp(-2*x)) -1
        
        agent = self.nn.createAgent(True)
        
        agent.addLink(1,4)
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.0,0.0])] == [0.76,0.0]
        
        agent.addNode(Node(6))
        agent.addLink(Link(2,6,0.75))
        agent.addLink(Link(6,5,-0.25))
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.6,0.0])] == [0.76,float(str(tanh(tanh(0.6*0.75)*-0.25))[:4])]
        
        agent.addLink(Link(3,6, -0.1))
        agent.addLink(Link(1,6, -0.6, False))
        
        assert [float(str(v)[:4]) for v in self.nn.evalAgent(agent, [1.0,0.6,0.2])] == [0.76,float(str(tanh(tanh(0.6*0.75+(-0.1*0.2))*-0.25))[:4])]