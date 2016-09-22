# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import copy as cp
import numpy as np

class Astar:
    def __init__(self, maze, origin, destination):
        self.maze = maze
        self.setOrigin(origin)
        self.setGoal(destination)

    def heuristic(self, n1, n2):
        return np.sqrt((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2)

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def process(self):
        self.result = self.astar()

    def astar(self):
        # Initialize sets
        closedSet = []
        openSet = [self.origin]

        # declare cameFrom
        cameFrom = cp.deepcopy(self.maze.arrayMap)

        for k in cameFrom:
            cameFrom[k] = 0

        # declare gScore
        gScore = cp.deepcopy(self.maze.arrayMap)
        
        for k in gScore:
            gScore[k] = np.inf

        # declare fScore
        fScore = cp.deepcopy(self.gScore)
        
        gScore[self.origin] = 0
        fScore[self.origin] = self.heuristic(self.origin)
        
        while openSet:
            # Calculate the current node
            current = openSet[0]
            for node in openSet:
                if fScore[current] > fScore[node]:
                    current = node

            if current == goal:
                return self.reconstruct_path(cameFrom, current)

            openSet.remove(current)
            closedSet.append(current)

            for neighbor in self.maze.getNeighbors(current):
                if neighbor in closedSet:
                    continue

                tentative_gScore = gScore[current] + self.maze.getDistance(current, neighbor)

            if neighbor not in openSet:
                openSet.append(neighbor)

            elif tentative_gScore >= gScore[neighbor]:
                continue

            cameFrom[neighbor] = current
            gScore[neighbor] = tentative_gScore
            fScore[neighbor] = gScore[neighbor] + self.heuristic(neighbor, self.goal)

        return False

    def reconstruct_path(self, cameFrom, current):
        total_path = [current]
        total_distance = 0
        while current in cameFrom.keys():
            new = cameFrom[current]

            total_path.append(new)
            total_distance += self.maze.getDistance(current, new)
            current = new
        return (total_distance, total_path)