from nn.nn import NN
from nn.Utils import *
import matplotlib.pyplot as plt
import random
import numpy as np


XORSettings = {
    "Input": 5,
    "Output": 4,
    "Generations": 1,
    "Population_Size": 150,
    "Distance_Treshold": 0.8,
    
    "mGeneRandom": 0.7,
    "mGeneShift": 0.94,
    "mGeneAdd": 0.01,
    "mGeneToggle": 0.001,
    "mNodeAdd": 0.001,
}

def main():
    nn = NN(XORSettings)
    
    data = [
        ([1,0,0], 0),
        ([1,1,1], 0),
        ([1,1,0], 1),
        ([1,0,1], 1)
    ]
    
    # data = [
    #     [[1,0,0,0], 1],
    #     [[1,0,0,1], 1],
    #     [[1,0,1,0], 1],
    #     [[1,0,1,1], 1],
    #     [[1,1,0,0], 0],
    #     [[1,1,0,1], 0],
    #     [[1,1,1,0], 0],
    #     [[1,1,1,1], 1]
    # ]
    
    data = [
        [[1, 3, 1, 4, 4, ]   ,    [0, 1, 0, 0, ]],
        [[1, 3, 2, 5, 4, ]   ,    [0, 1, 0, 0, ]],
        [[1, 3, 3, 6, 4, ]   ,    [0, 0, 1, 0, ]],
        [[1, 3, 4, 7, 4, ]   ,    [0, 1, 0, 0, ]],
        [[1, 3, 5, 8, 4, ]   ,    [0, 1, 0, 0, ]],
        [[1, 3, 6, 9, 4, ]   ,    [0, 0, 0, 1, ]]
    ]
    
    # nn.evolve(98.5, data, gtEval, plot=True)
    # save_agent(nn.topAgent, 'gt.net')
    
    
    a = load_sharp_agent('blackjack.genome')
    print(bjEval(a))
    plot_agent(nn, a)
    
    # for d in data:
        # print(evalAgent(a, d[0]))
    
    # print(evalAgent(nn.topAgent, [1, 1, 0]))
    # print(evalAgent(nn.topAgent, [1, 0, 1]))
    # print(evalAgent(nn.topAgent, [1, 0.5, 0.7]))
    # print(evalAgent(nn.topAgent, [1, 0.7, 0.5]))
    # print(evalAgent(nn.topAgent, [1, 0.3, 0.5]))
    # print(evalAgent(nn.topAgent, [1, 0.5, 0.3]))
    
    plt.pause(300000) 
          
def bjEval(agent):
    fitness = 0.0
    sucess = True
    
    target_n = 0
    other_act = False
    
    for j in range(len(X)):
        output =  evalAgent(agent, [1] + X[j], 4)
        for i in range(len(output)):
            if y[j][i] != 1 and output[i] >= 0.5:
                other_act = True
            elif y[j][i] == 1:
                target_n = output[i]
        
        fitness += 1.0 - (1-np.clip(target_n, 0, 1))**2
    
    
    return fitness

def xorEval(agent, data):
    fitness = 0.0
    sucess = True
    
    for item in data:
        output =  evalAgent(agent, item[0])[0]
        if item[1] <= 0.5:
            sucess &= output <= 0.5
            fitness += 1.0 - output**2
        elif item[1] > 0.5:
            sucess &= output > 0.5
            fitness += 1.0 - (1-output)**2
    
    if sucess:
        fitness += 10
    
    return fitness

def gtEval(agent, data):
    fitness = 0.0
    sucess = True
    
    for i in range(100):
        a = random()
        b = random()
        output = evalAgent(agent, [1,a,b], 4)[0]
        if a <= b:
            sucess &= output <= 0.5
            fitness += 1.0 - output**2
        elif a > b:
            sucess &= output > 0.5
            fitness += 1.0 - (1-output)**2
    
    if sucess:
        fitness += 100
        
    return fitness

X = []
y = []

for row in range(1,11):
    for c1 in range(1,11):
        for c2 in range(1,11):            
            X.append([c1,c2,c1+c2,row])
            if sorted([1,10]) == sorted([c1,c2]):
                y.append([1,0,0,0])
            elif c1 == 1 and c2 == 1:
                y.append([0,0,1,0])
            elif sorted([1,2]) == sorted([c1,c2]) or sorted([1,3]) == sorted([c1,c2]):
                if 5 <= row <= 6:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif sorted([1,4]) == sorted([c1,c2]) or sorted([1,5]) == sorted([c1,c2]):
                if 4 <= row <= 6:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif sorted([1,6]) == sorted([c1,c2]):
                if 3 <= row <= 6:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif sorted([1,7]) == sorted([c1,c2]):
                if 2 <= row <= 8:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif sorted([1,8]) == sorted([c1,c2]) or sorted([1,9]) == sorted([c1,c2]):
                y.append([1,0,0,0])
            elif [2,2] == [c1,c2] or [3,3] == [c1,c2]:
                if 2 <= row <= 7:
                    y.append([0,0,1,0])
                else:
                    y.append([0,1,0,0])
            elif [4,4] == [c1,c2]:
                if 5 <= row <= 6:
                    y.append([0,0,1,0])
                else:
                    y.append([0,1,0,0])
            elif [5,5] == [c1,c2]:
                if 2 <= row <= 9:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif [6,6] == [c1,c2]:
                if 2 <= row <= 6:
                    y.append([0,0,1,0])
                else:
                    y.append([0,1,0,0])
            elif [7,7] == [c1,c2]:
                if 2 <= row <= 7:
                    y.append([0,0,1,0])
                else:
                    y.append([0,1,0,0])
            elif [8,8] == [c1,c2]:
                y.append([0,0,1,0])
            elif [9,9] == [c1,c2]:
                if 2 <= row <= 9:
                    y.append([0,0,1,0])
                else:
                    y.append([1,0,0,0])
            elif [10,10] == [c1,c2]:
                y.append([1,0,0,0])        
            elif c1+c2 <= 8:
                y.append([0,1,0,0])
            elif c1+c2 == 9:
                if 3 <= row <= 6:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 10:
                if 2 <= row <= 9:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 11:
                if 2 <= row <= 9:
                    y.append([0,0,0,1])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 12:
                if 4 <= row <= 6:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 13:
                if 2 <= row <= 6:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 14:
                if 2 <= row <= 6:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 15:
                if 2 <= row <= 6:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 == 16:
                if 2 <= row <= 6:
                    y.append([1,0,0,0])
                else:
                    y.append([0,1,0,0])
            elif c1+c2 >= 17:
                y.append([1,0,0,0])

if __name__ == '__main__':
    main()