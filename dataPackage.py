import numpy as np
import NiffteGeoADC as ng
import Voxel as voxel

def intoPoint(x):
    x = x[:len(x)-1]
    x = x.split(' ')
    i = 0
    for num in x:
        x[i] = int(x[i])
        if i == 0:
            voxel.volume = x[i]
        elif i == 1:
            voxel.row = x[i]
        elif i == 2:
            voxel.column = x[i]
        elif i == 3:
            voxel.bucket = x[i]
        elif i == 4:
            voxel.adc = x[i]
        i += 1
    point = ng.MapVoxeltoXYZ(voxel)
    return point

def package(x):
    f = open(x)
    pkg = []
    L = -1
    for line in f:
        if line[0] == '#':
            pkg.append([])
            L += 1
        else:
            pkg[L].append(intoPoint(line))
    return pkg


