# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""


from math import *
from heapq import heappush, heappop
from sys import maxint

import copy
import numpy as np

class Astar(Algorithm):
    def __init__(self, Maze maze, origin, destination):
        self.maze = maze
        self.setOrigin(origin)
        self.setDestination(destination)

    def process(self):
        closedSet = {}
        openSet = {self.origin}
        
        cameFrom = copy.deepcopy(self.maze.arrayMap)

        for k in cameFrom:
            cameFrom[k] = 0
            
        
        gScore = copy.deepcopy(self.maze.arrayMap)
        
        for k in gScore:
            gScore[k] = np.inf
        
        fScore = copy.deepcopy(self.gScore)
        
        gScore[self.origin] = 0
        fScore[self.origin] = self.heuristic(self.origin)
        
        while openSet:
            # Calculate the current node
            current = openSet[]
            for node in openSet:
                
        
        
    def heuristic(n):
        # return 0; # Dijkstra        
        return sqrt((n[0] - self.destination[0])**2 - (n[1] - self.destination[1])**2)
    
    def setOrigin(self, position):
        self.origin = position
        
    def setDestination(self, position):
        self.destination = position
    
    def compare(n1, n2):
        if self.getHeuristic(n1) < self.getHeuristic(n2):
            return 1
        elif self.getHeuristic(n1) == self.getHeuristic(n2):
            return 0
        else:
            return -1
    
    def setHeuristic(self, noeud, val):
        self.heuristics[noeud] = val
        
    def getHeuristic(self, noeud):
        return self.heuristics[noeud]