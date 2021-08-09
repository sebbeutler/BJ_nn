import math

class Node:
    def tanh(x):
        return 2 / (1+math.exp(-2*x)) -1

    def leakyReLu(x):
        a = 0.001
        
        if x > 0.0:
            return x
        else:
            return x*a
    
    def sigmoid(x):
        return 1/(1+np.exp(-x))
    
    def __init__(self, id: int=0):
        self.id = id # type: int
        self.fn = Node.leakyReLu # type: function(float)
        self.links = [] # list{tuple(int, float)}
        self.value = None # type: float
        self.buffer_value = None # type: float
        self.layer = None
        
    def __eq__(self, other):
        return self.id == other.id
    
    def activate(self):
        self.value = self.fn(self.buffer_value)
        
    def __hash__(self) -> int:
        return self.id