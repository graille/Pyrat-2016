#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class TwoOPT:
    def __init__(self, maze, origin = None, goals = None):
        self.maze = maze
        self.origin = origin if origin else ()
        self.goals = goals if goals else ()

        self.NB_OF_NODES = len(goals) + 1

    def setOrigin(self, origin):
        self.origin = origin

    def setGoals(self, goals):
        self.goals = goals

    def calculateFirstPath(self):
        """
        Create a naive path
        """
        self.path = [self.origin]

        for n in self.goals:
            if n not in self.path:
                self.path.append(n)

    def process(self):
        self.algorithm()

    def algorithm(self):
        """
        Calculate a path with the 2-opt algorithm
        """
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
        """
        Echange deux arrêtes
        :param i: arrete partant de i
        :param j: arrete partant de j
        """
        for k in range(round((i - j)/2)):
            self.path[(i + k + 1) % self.NB_OF_NODES], self.path[j - k] = self.path[j - k], self.path[(i + 1 + k) % self.NB_OF_NODES]