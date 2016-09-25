# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np


class Astar:
    def __init__(self, maze, origin = None, goal = None):
        self.maze = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

        # declare self.nPredecessor
        self.nPredecessor = cp.deepcopy(self.maze.mazeMap)

        # declare self.gScore
        self.gScore = cp.deepcopy(self.maze.mazeMap)

        # declare self.fScore
        self.fScore = cp.deepcopy(self.gScore)

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def heuristic(self, n1, n2):
        return np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)

    def clear(self):
        for k in self.nPredecessor.keys():
            self.nPredecessor[k] = 0
            
        for k in self.gScore.keys():
            self.gScore[k] = np.inf
            
        for k in self.fScore.keys():
            self.nPredecessor[k] = 0

    def process(self):
        self.result = self.algorithm()

    def algorithm(self):
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

            for neighbor in self.maze.getNeighbors(current):
                if neighbor in self.closedSet:
                    continue

                tentative_gScore = self.gScore[current] + self.maze.getDistance(current, neighbor)

                if neighbor not in self.openSet:
                    self.openSet.append(neighbor)

                elif tentative_gScore >= self.gScore[neighbor]:
                    continue

                self.nPredecessor[neighbor] = current
                self.gScore[neighbor] = tentative_gScore
                self.fScore[neighbor] = self.gScore[neighbor] + self.heuristic(neighbor, self.goal)

        return False

    def reconstruct_path(self, current):
        total_path = ""
        total_distance = 0
        path = []
        while current != self.origin:
            new = self.nPredecessor[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new
        path.append(current)
        return (total_distance, total_path[::-1])

    def getResult(self):
        return self.result