import tensorflow as tf
from tensorflow.keras.models import Sequential  
from tensorflow.keras.layers import *
import numpy as np  
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import SGD

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
            elif c1+c2 == 11 and not (c1 == 1 and c2 == 1):
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


X = np.array(X)
y = np.array(y)

model = Sequential()
model.add(Dense(8, input_shape=(4,), activation='sigmoid'))
model.add(Dense(8, activation='sigmoid'))
model.add(Dense(4, activation='sigmoid'))

opt = SGD(learning_rate=0.1)
model.compile(optimizer=opt, loss='binary_crossentropy', metrics=['accuracy'])

model.fit(X, y, batch_size=1, epochs=5000, use_multiprocessing=True)
print(model.predict(X))
