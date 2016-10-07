#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TwoOPT:
    def __init__(self, maze, origin, goals):
        self.maze = maze
        self.origin = origin

        self.goals = goals
        self.NB_OF_NODES = len(goals) + 1

    def calculateFirstPath(self):
        self.path = [self.origin]

        for n in self.goals:
            if n not in self.path:
                self.path.append(n)

    def algorithm(self):
        improve = True
        while improve:
            improve = False
            for i in range(self.NB_OF_NODES):
                for j in range(self.NB_OF_NODES):
                    if j in [i - 1 % self.NB_OF_NODES, i, i + 1 % self.NB_OF_NODES]:
                        continue

                    if self.getDistance(i, i + 1) + self.getDistance(j, j + 1) > self.getDistance(i, j) + self.getDistance(i + 1, j + 1):
                        self.exchange(i, j)
                        improve = True

    def getResult(self):
        return (self.getResultDistance(), self.getResultPath())

    def getResultPath(self):
        return self.path

    def getResultDistance(self):
        r = 0
        for k in range(self.NB_OF_NODES - 1):
            r += self.maze.distanceMetagraph[k][k + 1]

        return r

    def getDistance(self, i, j):
        return self.maze.distanceMetagraph[self.path[i % self.NB_OF_NODES]][self.path[j % self.NB_OF_NODES]]

    def exchange(self, i, j):
        for k in range(round((i - j)/2)):
            self.path[(i + k + 1) % self.NB_OF_NODES], self.path[j - k] = self.path[j -k ], self.path[(i + 1 + k) % self.NB_OF_NODES]