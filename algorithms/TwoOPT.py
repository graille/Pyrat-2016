#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import random as rd
import time


class TwoOPT:
    def __init__(self, maze, origin = None, goals = None):
        self.maze = maze
        self.origin = origin if origin else ()
        self.goals = goals if goals else ()

        self.NB_OF_NODES = len(goals) + 1 if goals else 0
        self.path = []

        self.improveAlg = False
        self.allowedTime = np.inf

    def setOrigin(self, origin):
        self.origin = origin

    def setGoals(self, goals):
        self.goals = goals
        self.NB_OF_NODES = len(goals) + 1

    def setAllowedTime(self, time):
        self.allowedTime = time

    def calculateFirstPath(self):
        """
        Create a naive path
        """
        rd.shuffle(self.goals)
        self.path = [self.origin] + self.goals

        # We start with a random
        #for n in self.goals:
        #    if n not in self.path:
        #        self.path.append(n)

    def process(self):
        self.algorithm()


    def algorithm(self):
        """
        Calculate a path with the 2-opt algorithm
        """
        t = time.clock()
        self.calculateFirstPath()
        improve = True
        while improve and (self.allowedTime > (time.clock() - t)):
            improve = False

            for i in range(self.NB_OF_NODES): #range(self.NB_OF_NODES) optimize the loop, range(1, self.NB_OF_NODES - 1) optimize a way, but keep the last point at is place
                for j in range(self.NB_OF_NODES):
                    if j in [(i - 1) % self.NB_OF_NODES, i, (i + 1) % self.NB_OF_NODES]:
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
        if i > j:
            i, j = j, i

        for k in range(int(round(abs(i - j)/2))):
            self.path[(i + k + 1) % self.NB_OF_NODES], self.path[j - k] = self.path[j - k], self.path[(i + 1 + k) % self.NB_OF_NODES]