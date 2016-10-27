#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np


class K_Means:
    def __init__(self, maze, k = 4, nodes = None):
        self.maze = maze
        self.S = {}
        self.m = {}

        self.k = k

        if nodes:
            self.setNodes(nodes)

    def setK(self, k):
        self.k = k

    def setNodes(self, nodes):
        self.nodes = nodes
        self.NB_NODES = len(nodes)

    def getDistance(self, moy, n):
        x1, y1 = round(moy[0]), round(moy[1])

        dx1, dy1 = x1 - moy[0], y1 - moy[1]

        # Add moy to metagraph
        self.maze.addNodeToMetagraph((x1, y1), self.nodes)
        d = self.maze.distanceMetagraph[(x1, y1)][n]

        return d + np.sqrt(dx1**2 + dy1**2)

        #x1, y1 = i
        #x2, y2 = j
        #return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def sommeTuplesInList(self, L):
        x, y = 0, 0
        for n in L:
            x += n[0]
            y += n[1]

        return (x, y)

    def process(self, allowed_time):
        if self.NB_NODES > self.k:
            t, nb = time.clock(), 0

            # Initialise M
            self.m[nb] = {}
            for i in range(self.k):
                self.m[nb][i] = self.nodes[i]

            while allowed_time > (time.clock() - t):
                self.S[nb] = {}
                self.m[nb + 1] = {}
                for i in range(self.k):
                    self.S[nb][i] = []

                    for n in self.nodes:
                        d = self.getDistance(self.m[nb][i], n)
                        c = True

                        for j in range(self.k):
                            if d > self.getDistance(self.m[nb][j], n):
                                c = False

                        if c:
                            self.S[nb][i].append(n)

                    x, y = self.sommeTuplesInList(self.S[nb][i])

                    self.m[nb + 1][i] = (x / len(self.S[nb][i]), y / len(self.S[nb][i]))
                nb += 1

            print("## K-means executed in " + repr(allowed_time) + " seconds and " + repr(nb) + " operations")

            return (self.m[nb - 1], self.S[nb - 1])