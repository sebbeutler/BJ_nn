from nn.nn import NN
from nn.Agent import Agent
from nn.Utils import *

Settings = {
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

netenv = NN(Settings)

agent = load_sharp_agent('blackjack.genome')
plot_agent(netenv, agent)
# plt.pause(30000)

a = ''
while a != 'q':
    a = input("Input>")
    inp = a.split(" ")
    if len(inp) != 4:
        print("Wrong input.")
        continue
    print([1] + list(map(int, inp)))
    print(evalAgent(agent, [1] + list(map(int, inp)), 4))