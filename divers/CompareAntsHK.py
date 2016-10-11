from includes.Maze import *
from includes.Rat import *
from algorithms.Fourmis import *
from algorithms.HK import *
import time
import matplotlib.pyplot as plt

mazeMap = {(0, 0) : {(0, 1) : 1}, (0, 1) : {(0, 2) : 1, (1, 1) : 1, (0, 0) : 1}, (0, 2) : {(0, 3) : 1, (1, 2) : 1, (0, 1) : 1}, (0, 3) : {(1, 3) : 1, (0, 2) : 1}, (1, 0) : {(1, 1) : 1, (2, 0) : 1}, (1, 1) : {(2, 1) : 1, (1, 0) : 1, (0, 1) : 1}, (1, 2) : {(1, 3) : 1, (0, 2) : 1, (2, 2) : 1}, (1, 3) : {(0, 3) : 1, (1, 2) : 1}, (2, 0) : {(3, 0) : 1, (1, 0) : 1}, (2, 1) : {(1, 1) : 1, (2, 2) : 1}, (2, 2) : {(2, 1) : 1, (3, 2) : 1, (1, 2) : 1, (2, 3) : 1}, (2, 3) : {(2, 2) : 1}, (3, 0) : {(3, 1) : 1, (2, 0) : 1}, (3, 1) : {(3, 0) : 1, (3, 2) : 1}, (3, 2) : {(3, 1) : 1, (3, 3) : 1, (2, 2) : 1}, (3, 3) : {(3, 2) : 1}}

def trace(n):
    timeTabHK = [0]*n
    timeTabAnts = [0]*n
    for k in range(2,20):
        liste = [(rd.randint(0,3), rd.randint(0,3))for i in range(k)]
        print(liste)
        origin = (0,0)
        maze = Maze(mazeMap, 4, 4)
        maze.calculateMetaGraph(origin, liste)
        hk = HeldKalp(maze, origin, liste)
        ants = Fourmis(maze, origin, liste, pheromonesTime = 10, antNumber = 300, pheromonesMax = 40)
        t1 = time.clock()
        #print(hk.process())
        t2 = time.clock()
        timeTabHK.append(t2-t1)
        t1 = time.clock()
        print(ants.process())
        t2 = time.clock()
        timeTabAnts.append(t2-t1)
        print("Elapsed time : ", t2-t1)
    plt.plot(timeTabHK)
    plt.plot(timeTabAnts)
    plt.show()

def test(nb):
    liste = [(rd.randint(0,3), rd.randint(0,3))for i in range(nb)]
    origin = (0,0)
    maze = Maze(mazeMap, 4, 4)
    maze.calculateMetaGraph(origin, liste)
    hk = HeldKalp(maze, origin, liste)
    t1 = time.clock()
    print(hk.process())
    t2 = time.clock()
    print("Elapsed time : ", t2-t1)
	
trace(5)