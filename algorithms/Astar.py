# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import numpy as np


class Astar:
    def __init__(self, maze, origin = None, goal = None, factor = 1):
        self.graph = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()
        self.factor = factor

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def heuristic(self, n1, n2):

        return np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2) * self.factor

    def clear(self):
        self.nPredecessor = {}
        self.gScore = {}
        self.fScore = {}
        
        for k in self.graph.nodes:
            self.nPredecessor[k] = 0
            
        for k in self.graph.nodes:
            self.gScore[k] = np.inf

        for k in self.graph.nodes:
            self.fScore[k] = np.inf

    def process(self):
        self.result = self.algorithm()

    def algorithm(self):
        if self.origin != self.goal:
            self.clear()

            self.closedSet = []
            self.openSet = [self.origin]

            self.gScore[self.origin] = 0
            self.fScore[self.origin] = self.heuristic(self.origin, self.goal)

            while self.openSet:
                # Calculate the current node
                current = self.openSet[0]
                for node in self.openSet:
                    if self.fScore[current] > self.fScore[node]:
                        current = node
                if current == self.goal:
                    return self.reconstruct_path(current)

                self.openSet.remove(current)
                self.closedSet.append(current)

                for neighbor in self.graph.getNeighbors(current):
                    if neighbor in self.closedSet:
                        continue

                    tentative_gScore = self.gScore[current] + self.graph.getDistance(current, neighbor)

                    if neighbor not in self.openSet:
                        self.openSet.append(neighbor)

                    elif tentative_gScore >= self.gScore[neighbor]:
                        continue

                    self.nPredecessor[neighbor] = current
                    self.gScore[neighbor] = tentative_gScore
                    self.fScore[neighbor] = self.gScore[neighbor] + self.heuristic(neighbor, self.goal)

            return False
        else:
            return (0, [])

    def reconstruct_path(self, current):
        litteral_path = ""
        total_distance = 0
        real_path = []
        while current != self.origin:
            new = self.nPredecessor[current]

            litteral_path += self.graph.getMove(new, current)
            total_distance += self.graph.getDistance(current, new)
            real_path.append(current)
            current = new

        real_path.append(current)
        return (total_distance, real_path[::-1])

    def getResult(self):
        return self.result