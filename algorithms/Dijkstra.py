# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np


class Dijkstra:
    def __init__(self, maze, origin = None, goal = None):
        self.graph = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def clear(self):
        self.pathArray = {}
        self.dist = {}

        for node in self.graph.nodes:
            self.pathArray[node] = None

        for node in self.graph.nodes:
            self.dist[node] = np.inf

    def process(self):
        self.algorithm()

    def algorithm(self):
        if self.origin != self.goal:
            self.clear()
            self.dist[self.origin] = 0

            Q = cp.copy(self.graph.nodes)

            while Q:
                n1 = self.findMin(Q)
                Q.remove(n1)

                if self.goal and n1 == self.goal:
                    break

                for n2 in self.graph.getNeighbors(n1):
                    self.majDistance(n1, n2)
        else:
            pass

    def findMin(self, Q):
        m = np.inf
        s = None

        for n in Q:
            if self.dist[n] < m:
                m = self.dist[n]
                s = n

        return s

    def majDistance(self, n1, n2):
        if self.dist[n2] > self.dist[n1] + self.graph.getDistance(n1, n2):
            self.dist[n2] = self.dist[n1] + self.graph.getDistance(n1, n2)
            self.pathArray[n2] = n1

    def reconstructPath(self, node):
        litteral_path = ""
        total_distance = 0
        current = node
        real_path = []
        while current != self.origin:
            new = self.pathArray[current]

            litteral_path += self.graph.getMove(new, current)
            total_distance += self.graph.getDistance(current, new)
            real_path.append(current)

            current = new

        real_path.append(current)
        return (total_distance, real_path[::-1])

    def getResult(self, node = None):
        if self.goal != self.origin:
            if (not node) and (self.goal):
                return self.reconstructPath(self.goal)
            else:
                return self.reconstructPath(node)
        else:
            return (0, [])