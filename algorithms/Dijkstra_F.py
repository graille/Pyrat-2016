# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np

from libs.FibonacciHeap import *

class Dijkstra:
    def __init__(self, maze, origin = None, goal = None):
        self.maze = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

        # Initilialize pathArray
        self.prev = {}
        self.dist = {}
        self.entries = {}

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def process(self):
        self.algorithm()

    def algorithm(self):
        self.dist[self.origin] = 0

        Q = Fibonacci_heap()
        for n in self.maze.nodes:
            if n != self.origin:
                self.dist[n] = 1000
                
            self.prev[n] = None
            self.entries[n] = Q.enqueue(n, self.dist[n])

        while len(Q) != 0:
            n1 = Q.dequeue_min()

            if self.goal and n1.m_elem == self.goal:
                break

            for n2 in self.maze.getNeighbors(n1.m_elem):
                alt = self.dist[n1.m_elem] + self.maze.getDistance(n1.m_elem, n2)
                if alt < self.dist[n2]:
                    self.dist[n2] = alt
                    self.prev[n2] = n1.m_elem
                    Q.decrease_key(self.entries[n2], alt)

    def reconstructPath(self):
        total_path = ""
        total_distance = 0
        path = []
        current = self.goal

        while current != self.origin:
            new = self.prev[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new

        path.append(current)

        return (total_distance, total_path[::-1])

    def getResult(self):
        return self.reconstructPath()