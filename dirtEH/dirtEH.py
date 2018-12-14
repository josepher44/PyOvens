import numpy as np
import os


def getPaths(dir):
    files = os.listdir(dir)
    for i in files:
        print(dir+i)


print("Hello, Canada?")
getPaths("C:/Users/Owner/Documents/Portfolio/Media/Collage Canidates/")
