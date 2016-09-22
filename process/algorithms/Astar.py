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

# Represent each node as a list, ordering the elements so that a heap of nodes
# is ordered by f = g + h, with h as a first, greedy tie-breaker and num as a
# second, definite tie-breaker. Store the redundant g for fast and accurate
# calculations.

F, H, NUM, G, POS, OPEN, VALID, PARENT = xrange(8)


def astar(start_pos, neighbors, goal, start_g, cost, heuristic, limit=maxint,
          debug=None):

    """Find the shortest path from start to goal.
    Arguments:
      start_pos      - The starting position.
      neighbors(pos) - A function returning all neighbor positions of the given
                       position.
      goal(pos)      - A function returning true given a goal position, false
                       otherwise.
      start_g        - The starting cost.
      cost(a, b)     - A function returning the cost for moving from one
                       position to another.
      heuristic(pos) - A function returning an estimate of the total cost
                       remaining for reaching goal from the given position.
                       Overestimates can yield suboptimal paths.
      limit          - The maximum number of positions to search.
      debug(nodes)   - This function will be called with a dictionary of all
                       nodes.
    The function returns the best path found. The returned path excludes the
    starting position.
    """

    

class Astar(Algorithm):
    def __init__(self, Maze maze):
        self.maze = maze
        self.heuristics = {}
        self.cost = {}
        pass
    
    def process(self):
        pass

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