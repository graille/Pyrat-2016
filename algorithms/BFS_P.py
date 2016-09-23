# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np
from queue import *

class BFS_P:
    def __init__(self, maze, nodes = None):
        self.maze = maze
        self.setNodes(nodes) if nodes else ()

        # Initialize attributes
        self.nWeight = cp.deepcopy(maze.mazeMap)
        self.nPredecessor = cp.deepcopy(maze.mazeMap) # Precessessor of all nodes
        self.nExplored = cp.deepcopy(maze.mazeMap) # Explored nodes

        # Clear attributes
        self.clear()

    def clear(self):
        for n in self.maze.nodes:
            self.nWeight[n] = 0
        for n in self.maze.nodes:
            self.nPredecessor[n] = None
        for n in self.maze.nodes:
            self.nExplored[n] = False

    def setNodes(self, nodes):
        if isinstance(nodes, list):
            self.nodes = nodes
        else:
            print("Error : n is not a list")

    def setOrigin(self, origin):
        self.origin = origin

    def process(self):
        self.algorithm()

    def algorithm(self):
        q = Queue()
        q.put_nowait((0, self.origin))

        while self.nodes:
            p, c = q.get_nowait()

            if not self.nExplored[c]: # If these nodes have not be explored before (caused by costs)
                if p == 0:
                    self.nExplored[c] = True
                    if c in self.nodes: # If we are in a node
                        self.nodes.remove(c)

                    for n in self.maze.getNeighbors(c):
                        cost = self.maze.getDistance(c, n)
                        nCost = self.nWeight[c] + cost

                        if nCost < self.nWeight[n]: # If the current cost is better
                            if not self.nPredecessor[n]:
                                q.put_nowait((cost, n))

                            self.nPredecessor[n] = c
                            self.nWeight[n] = nCost
                else:
                    q.put_nowait((p - 1, c))
            else:
                continue

        self.clear()

    def getWeight(self, n):
        return self.nWeight[n]

