#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import numpy as np
from algorithms.Astar import *

class K_Means:
    def __init__(self, maze, k = 4, nodes = None):
        self.maze = maze
        self.S = {}
        self.m = {}

        self.k = k
        self.nodes = nodes
        self.astar = Astar(maze)

        self.distanceGraph = {}

        if nodes:
            self.setNodes(nodes)

    def setK(self, k):
        self.k = k

    def setNodes(self, nodes):
        self.nodes = nodes
        self.NB_NODES = len(nodes)

    def getDistance(self, i, j):
        p = random.randint(0,100)
        if p < 0: # 80% de chance de faire Astar
            x1, y1 = round(i[0]), round(i[1])
            x2, y2 = round(j[0]), round(j[1])

            self.astar.setOrigin((x1, y1))
            self.astar.setGoal((x2, y2))
            self.astar.process()
            d = self.astar.getResult()[0]
            return d
        else:
            x1, y1 = i
            x2, y2 = j
            return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def sommeTuplesInList(self, L):
        x, y = 0, 0
        for n in L:
            x += n[0]
            y += n[1]

        return (x, y)

    def process(self, iteration = 100):
        if self.NB_NODES > self.k:
            #random.shuffle(self.nodes)
            t = 0

            # Initialise M
            self.m[t] = {}
            for i in range(self.k):
                self.m[t][i] = self.nodes[i]

            while t < iteration:
                self.S[t] = {}
                self.m[t + 1] = {}
                for i in range(self.k):
                    self.S[t][i] = []

                    for n in self.nodes:
                        d = self.getDistance(n, self.m[t][i])
                        c = True

                        for j in range(self.k):
                            if d > self.getDistance(n, self.m[t][j]):
                                c = False

                        if c:
                            self.S[t][i].append(n)

                    x, y = self.sommeTuplesInList(self.S[t][i])

                    self.m[t + 1][i] = (x / len(self.S[t][i]), y / len(self.S[t][i]))

                t += 1

            return (self.m[t - 1], self.S[t - 1])