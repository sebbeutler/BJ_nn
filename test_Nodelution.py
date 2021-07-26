import pytest
from Nodelution import *

class Test_Nodelution:
    nn = Nodelution(DefaultSettings)

    def setupBasicAgent(self):
        agent = Agent()

        agent.addNode(Node(1))
        agent.addNode(Node(2))
        agent.addNode(Node(3))
        agent.addNode(Node(4))
        agent.addNode(Node(5))

        return agent

    def test_initNodelution(self):
        settings = DefaultSettings.copy()
        settings["Input"] = 3
        settings["Output"] = 2

        nn = Nodelution(DefaultSettings)

        assert nn.inputList == [1,2,3]
        assert nn.outputList == [4,5]
        assert nn.nodeCount == 5

    def test_mutateLinkAdd(self):
        agent = self.setupBasicAgent()

        agent.addLink(1, 4)
        agent.addLink(3, 4)
        agent.addLink(2, 5)

        assert len(agent.active_links) == 3       
        self.nn.mutateLinkAdd(agent)
        assert len(agent.active_links) == 4  

    
    def test_mutateLinkShift(self):
        agent = self.setupBasicAgent()

        agent.addLink(1, 2)

        assert agent.nodes[2].links[0].weight == 1.0

        self.nn.mutateLinkShift(agent)

        assert agent.nodes[2].links[0].weight != 1.0

        assert agent.nodes[2].links[0].weight == agent.active_links[0].weight

        # TODO: test on agent without links / with all disabled links
    
    def test_mutateLinkToggle(self):
        agent = self.setupBasicAgent()

        agent.addLink(1, 2)
        agent.addLink(4, 5)
        agent.addLink(1, 3)

        assert len(agent.active_links) == 3 and len(agent.inactive_links) == 0

        self.nn.mutateLinkToggle(agent)

        assert len(agent.active_links) == 2 and len(agent.inactive_links) == 1

        # TODO: test toggling off some links