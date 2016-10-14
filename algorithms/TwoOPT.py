#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

class TwoOPT:
    def __init__(self, maze, origin = None, goals = None):
        self.maze = maze
        self.origin = origin if origin else ()
        self.goals = goals if goals else ()

        self.NB_OF_NODES = len(goals) + 1 if goals else 0
        self.path = []

        self.improveAlg = False

    def setOrigin(self, origin):
        self.origin = origin

    def setGoals(self, goals):
        self.goals = goals
        self.NB_OF_NODES = len(goals) + 1

    def calculateFirstPath(self):
        """
        Create a naive path
        """
        self.path = [self.origin]

        # We start with a random
        for n in self.goals:
            if n not in self.path:
                self.path.append(n)

        #print("First path " + repr(self.getResult()))

    def process(self):
        self.algorithm()

    def setImprove(self, val):
        self.improveAlg = val

    def algorithm(self):
        """
        Calculate a path with the 2-opt algorithm
        """
        self.calculateFirstPath()
        improve = True
        while improve:
            improve = False

            # Personnal improve
            if self.NB_OF_NODES > 1 and self.improveAlg:
                for i in range(self.NB_OF_NODES - 1):
                    if self.getDistance(i, -1) < self.getDistance(i, i+1):
                        #print(list(range(1, self.NB_OF_NODES - i)))
                        self.path = self.path[:(i+1)] + (self.path[(i+1)::])[::-1]
                        #print("personnal improve")
                        #print("Current path " + repr(self.getResult()))
                        improve = True

            for i in range(self.NB_OF_NODES): #range(self.NB_OF_NODES) optimize the loop, range(1, self.NB_OF_NODES - 1) optimize a way, but keep the last point at is place
                for j in range(self.NB_OF_NODES):
                    print(self.path)
                    if j in [i - 1 % self.NB_OF_NODES, i, i + 1 % self.NB_OF_NODES]:
                        continue

                    if self.getDistance(i, i + 1) + self.getDistance(j, j + 1) > self.getDistance(i, j) + self.getDistance(i + 1, j + 1):
                        self.exchange(i, j)
                        #print("Exchange " + str(i) + "|" + str(j) + ". Comparaison distance : (before) " + repr(self.getDistance(i, j) + self.getDistance(i + 1, j + 1)) + " | (after) " + repr(self.getDistance(i, i + 1) + self.getDistance(j, j + 1)))
                        #print("Current path " + repr(self.getResult()))
                        improve = True

    def getResult(self):
        return (self.getResultDistance(), self.getResultPath())

    def getResultPath(self):
        return self.path

    def getResultDistance(self):
        r = 0
        for k in range(self.NB_OF_NODES - 1):
            #print("Distance " + str(k) + " " + repr(self.path[k]) + " to " + str(k+1) + " " + repr(self.path[k+1]) + " = " + str(self.maze.distanceMetagraph[self.path[k]][self.path[k + 1]]))
            r += self.maze.distanceMetagraph[self.path[k]][self.path[k + 1]]

        return r # Get the longer of the path, without loop

    def getDistance(self, i, j):
        return self.maze.distanceMetagraph[self.path[i % self.NB_OF_NODES]][self.path[j % self.NB_OF_NODES]]

    def exchange(self, i, j): # bug quand ça reboucle !!!
        """
        Echange deux arrêtes
        :param i: arrete partant de i
        :param j: arrete partant de j
        """
        #print(str(int(round(abs(i - j)/2))) +  repr((i, j)))
        if i > j:
            i, j = j, i
        for k in range(int(round(abs(i - j)/2))):
            #print(((i + k + 1) % self.NB_OF_NODES, j - k))
            self.path[(i + k + 1) % self.NB_OF_NODES], self.path[j - k] = self.path[j - k], self.path[(i + 1 + k) % self.NB_OF_NODES]