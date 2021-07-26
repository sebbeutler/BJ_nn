import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def dsigmoid(x):
    return x * (1.0 - x)

def softmax(x):
    l = []
    for e in x:
        l.append(np.exp(e) / sum(np.exp(x)))
    return l

def relu(x):
    return np.maximum(x, 0)

def drelu(x):
    return 1 if x > 0 else 0

def none(x):
    return x


class Neuron(object):
    def __init__(self, weights, bias, l_rate=0.5):
        self.weights = weights
        self.value = None
        self.bias = bias
        self.operation = none
        self.delta = None
        self.l_rate = l_rate
    
    def eval(self, inputs):
        n_values = [n.value for n in inputs]
        self.value = self.operation(sum([w * n for w, n in zip(self.weights, n_values)]) + self.bias)
        return self.value
    
    def update(self, previous_layer):
        for i in range(len(self.weights)):
            self.weights[i] += self.l_rate * self.delta * previous_layer[i].value
        self.bias += self.l_rate * self.delta


class Brain(object):
    def __init__(self, layers_info):
        self.layers_info = layers_info
        self.layers = []
        self.total_weights = []
        for index, info in list(enumerate(layers_info)):
            self.layers.append([Neuron([np.random.uniform(-1.0,1.0) for k in range(layers_info[index-1][0])], np.random.uniform(-1.0,1.0)) for j in range(info[0])])
        for l,i in zip(self.layers, layers_info):
            for n in l:
                n.operation = i[1]
    
    def input(self, inputs):
        for neuron, value in zip(self.layers[0], inputs):
            neuron.value = value
        previous_layer = self.layers[0]
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.eval(previous_layer)
            previous_layer = layer
        return [ neuron.value for neuron in self.layers[-1]]
    
    def backward_propagate_error(self, expected):
        # Backpropagate error and store in neurons
        for neuron, expected_value in zip(self.layers[-1], expected):            
            neuron.delta = (expected_value - neuron.value) * dsigmoid(neuron.value)

        for index in reversed(range(len(self.layers)-1)):
            layer = self.layers[index]
            errors =  []
            
            for current_neuron_index in range(len(layer)):
                error = 0.0
                for neuron_next in self.layers[index + 1]:
                    error += (neuron_next.weights[current_neuron_index] * neuron_next.delta)

                errors.append(error)
            for neuron, error in zip(layer, errors):
                neuron.delta = error * dsigmoid(neuron.value)
    
    def update_weights(self):
        previous_layer = self.layers[0]
        for layer in self.layers[1:]:
            for neuron in layer:
                neuron.update(previous_layer)
            previous_layer = layer
        
    def learn(self, data, n=100000):
        for i in range(n):
            np.random.shuffle(data)
            for inputs, expected in data:
                self.input(inputs)
                loss = sum([ (expected - output.value)**2  for output, expected in zip(self.layers[-1], expected) ])
                self.backward_propagate_error(expected)
                self.update_weights()
                print(loss)


if __name__ == "__main__":
    brain = Brain([(2, sigmoid), (3, sigmoid), (1, sigmoid)])

    brain.learn([
        ([0.,0.],[0.]),
        ([1.,0.],[1.]),
        ([0.,1.],[1.]),
        ([1.,1.],[0.]),
    ])
    print()
    print(brain.input([0.,0.])[0])
    print(brain.input([0.,1.])[0])    
    print(brain.input([1.,0.])[0])
    print(brain.input([1.,1.])[0])