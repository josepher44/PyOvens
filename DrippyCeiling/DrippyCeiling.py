import math
import numpy as np
from random import *

compartments = 3
initialValue = 1000
parts = []
processing = 0
nextToPull = 0
nextToAdd = 0
maxTotal = 0



for i in range(compartments):
    parts.append(initialValue)
    print(parts[i])

for j in range(400000):
    if processing is 0:
        index_max = np.argmax(parts)
        if parts[index_max] > maxTotal:
            maxTotal = parts[index_max]
        processing = parts[index_max]
        parts[index_max]=0
        #processing = parts[nextToPull]
        #parts[nextToPull] = 0
        #nextToPull += 1
        #if nextToPull >= len(parts):
        #    nextTopull = 0
        print("Pulled next bin")
        print(parts)
    else:
        processing -= 1
        parts[nextToAdd] += 1
        nextToAdd = randint(0,compartments-1)
        #nextToAdd += 1
        #if nextToAdd >= len(parts):
        #    nextToAdd = 0
        #print("Incremented lists")
        #print(parts)
        print(j)

print(maxTotal)
