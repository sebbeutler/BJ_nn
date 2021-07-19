import pytest
from Nodelution import *

class Test_Nodelution:
    nn = Nodelution(DefaultSettings)

    def test_initNodelution(self):
        settings = DefaultSettings.copy()
        settings["Input"] = 3
        settings["Output"] = 2

        nn = Nodelution(DefaultSettings)

        assert nn.inputList == [1,2,3]
        assert nn.outputList == [4,5]
        assert nn.nodeCount == 5

    def test_mutateAddLink(self):
        self.nn.setup()

        assert len(self.nn.test.nodes) == 5