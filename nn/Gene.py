class Gene:
    def __init__(self, id, src=None, to=None, weight=1.0, enabled=True) -> None:
        self.id = id
        self.src = src
        self.to = to
        self.weight = weight
        self.enabled = enabled
    
    def copy(self):
        return Gene(self.id, self.src, self.to, self.weight, self.enabled)
    
    def __repr__(self) -> str:
        return f'[{self.id}: ({self.src}, {self.to}, {self.weight})]'
    
    def __str__(self) -> str:
        return "({}, {}): {}".format(self.src, self.to, self.weight)
    
    def __lt__(self, other):
        return self.id < other.id
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __gt__(self, other):
        return self.id > other.id
    
    def __hash__(self) -> int:
        return self.id