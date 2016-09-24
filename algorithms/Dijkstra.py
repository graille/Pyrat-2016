# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np


class Dijkstra:
    def __init__(self, maze, origin = None, goal = None):
        self.maze = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

        # Initilialize pathArray
        self.pathArray = cp.deepcopy(self.maze.mazeMap)

        self.clear()

    def clear(self):
        self.d = None
        for node in self.maze.nodes:
            self.pathArray[node] = None

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def process(self):
        self.result = self.algorithm()

    def algorithm(self):
        self.clear()
        self.initialize()

        Q = cp.copy(self.maze.nodes)

        while Q:
            n1 = self.findMin(Q)
            Q.remove(n1)

            for n2 in self.maze.getNeighbors(n1):
                self.majDistance(n1, n2)

        return self.reconstructPath()

    def initialize(self):
        self.d = cp.deepcopy(self.maze.mazeMap)
        for node in self.maze.nodes:
            self.d[node] = np.inf

        self.d[self.origin] = 0

    def findMin(self, Q):
        m = np.inf
        s = None

        for n in Q:
            if self.d[n] < m:
                m = self.d[n]
                s = n

        return s

    def majDistance(self, n1, n2):
        if self.d[n2] > self.d[n1] + self.maze.getDistance(n1, n2):
            self.d[n2] = self.d[n1] + self.maze.getDistance(n1, n2)
            self.pathArray[n2] = n1

    def reconstructPath(self):
        total_path = ""
        total_distance = 0
        path = []
        current = self.goal

        while current != self.origin:
            new = self.pathArray[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new

        path.append(current)

        return (total_distance, total_path[::-1])

    def getResult(self):
        return self.result