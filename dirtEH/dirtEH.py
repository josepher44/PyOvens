import numpy as np
import os


def getPaths(dir):
    files = os.listdir(dir)
    for i in files:
        print(dir+i)
    return files

workspacePath = "C:/Users/Owner/Documents/Portfolio/"
subdirectory = "Media/Collage Canidates/"
print("Hello, Canada?")
files = getPaths(workspacePath+subdirectory)
print(files)
for path in files:
    print("<img class=\"\" href=\"" + subdirectory+path + "\">")
