# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:09:14 2016

@author: Clément
@modification : Thibault
"""

from __future__ import absolute_import

import copy as cp
import numpy as np

class Astar:
    def __init__(self, maze, origin, goal):
        self.maze = maze
        self.setOrigin(origin)
        self.setGoal(goal)

    def heuristic(self, n1, n2):
        return np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)

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
        cameFrom = cp.deepcopy(self.maze.mazeMap)

        for k in cameFrom.keys():
            cameFrom[k] = 0

        # declare gScore
        gScore = cp.deepcopy(self.maze.mazeMap)

        for k in gScore.keys():
            gScore[k] = np.inf

        # declare fScore
        fScore = cp.deepcopy(gScore)

        gScore[self.origin] = 0
        fScore[self.origin] = self.heuristic(self.origin, self.goal)

        while openSet:
            # Calculate the current node
            current = openSet[0]
            for node in openSet:
                if fScore[current] > fScore[node]:
                    current = node
            if current == self.goal:
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
        total_path = ""
        total_distance = 0
        path = []
        while current != self.origin:
            new = cameFrom[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new
        path.append(current)
        return (total_distance, total_path[::-1])


class Maze(object):
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight

        self.pathMatrix = None
        self.matrixMap = None

        self.convertToMatrix()
        #self.FM = FloydWarshall(self)
        #self.FM.process()

    def location_to_id(self, location):
        """Converti les coordonnees d'une case en sa cle primaire"""
        x, y = location[0], location[1]
        id_case = x * self.mazeHeight + y
        return id_case

    def id_to_location(self, id_case):
        """Converti la cle primaire d'une case en ses coordonnees"""
        location = (id_case // self.mazeHeight, id_case % self.mazeHeight)
        return location

    def convertToMatrix(self):
        """
        Prend en argument
        Renvoie une matrice où les cases sont triées en fonction de leur id et où
        np.inf signifie qu'il n'y a pas de passage direct entre les deux cases,
        n>0 signifie qu'il y a passage en n coups et 0 que l'on reste sur la même case
        """
        self.matrixMap = np.array([[np.inf if i != j else 0 for i in range(self.NB_CASES)] for j in range(
            self.NB_CASES)])  # On crée une matrice contenant que des -1 sauf sur la diagonale
        for locationCaseAccessible1 in self.mazeMap:
            cle_case1 = self.location_to_id(locationCaseAccessible1)
            for locationCaseAccessible2 in self.mazeMap[locationCaseAccessible1]:
                cle_case2 = self.location_to_id(locationCaseAccessible2)
                self.matrixMap[cle_case1][cle_case2], self.matrixMap[cle_case2][cle_case1] = \
                self.mazeMap[locationCaseAccessible1][locationCaseAccessible2], self.mazeMap[locationCaseAccessible1][
                    locationCaseAccessible2]

    def calculateMetaGraph(self, from_location, to_location_list):
        """Remplit les cases de la matrice des distances uniquement pour les cases spécifiées"""
        from_location_ID = self.location_to_id(from_location)

        for to_location in to_location_list:
            to_location_ID = self.location_to_id(to_location)

            astar = Astar(self, from_location, to_location)

            (dist, path) = astar.process()
            self.pathMatrix[from_location_ID, to_location_ID] = path
            self.matrixMap[from_location_ID, to_location_ID] = dist

    def getDistance(self, from_location, to_location):
        from_location_ID, to_location_ID = self.location_to_id(from_location), self.location_to_id(to_location)

        return self.matrixMap[from_location_ID, to_location_ID]

    def getNodes(self):
        return self.mazeMap.keys()

    def findMostRapidWay(self, origin, goal):
        al = Astar(self, origin, goal)
        al.process()

        return al.result

    def getMove(self, origin, goal):
        i1,j1 = origin
        i2,j2 = goal

        if i1 - i2 == -1:
            return 'D'
        elif i1 - i2 == 1:
            return 'U'
        elif j1 - j2 == -1:
            return 'R'
        elif j1 - j2 == 1:
            return 'L'
        else:
            return False

    def getNeighbors(self, position):
        return self.mazeMap[position].keys()

mazeMap = {(7, 3): {(6, 3): 1, (8, 3): 1, (7, 2): 1}, (6, 9): {(6, 8): 10}, (11, 11): {(11, 10): 1, (10, 11): 1}, (7, 12): {(6, 12): 1, (8, 12): 1}, (0, 7): {(0, 6): 1, (0, 8): 1, (1, 7): 1}, (1, 6): {(0, 6): 1, (1, 5): 1}, (0, 10): {(1, 10): 1, (0, 11): 1}, (3, 7): {(3, 8): 1, (2, 7): 1, (4, 7): 2}, (2, 5): {(1, 5): 1, (2, 6): 1, (3, 5): 1}, (1, 11): {(0, 11): 1, (2, 11): 1, (1, 12): 1}, (8, 5): {(8, 6): 1, (7, 5): 1, (8, 4): 9}, (5, 8): {(5, 7): 1, (6, 8): 5, (4, 8): 1}, (4, 0): {(4, 1): 1, (5, 0): 1}, (10, 8): {(11, 8): 1, (10, 9): 1}, (9, 0): {(10, 0): 6, (8, 0): 1, (9, 1): 9}, (6, 7): {(5, 7): 1, (6, 6): 1}, (5, 5): {(5, 6): 10}, (11, 5): {(10, 5): 1}, (10, 7): {(11, 7): 1}, (7, 6): {(8, 6): 1, (6, 6): 1}, (6, 10): {(6, 11): 1, (5, 10): 1, (7, 10): 1}, (0, 4): {(0, 3): 1, (0, 5): 1, (1, 4): 1}, (1, 1): {(0, 1): 1, (1, 2): 1, (1, 0): 1, (2, 1): 4}, (4, 10): {(5, 10): 1}, (3, 2): {(4, 2): 1, (3, 1): 1, (3, 3): 1}, (2, 6): {(2, 7): 7, (2, 5): 1, (3, 6): 1}, (9, 14): {(8, 14): 1, (9, 13): 1}, (8, 2): {(8, 1): 1, (8, 3): 1, (7, 2): 1}, (5, 11): {(6, 11): 5, (5, 12): 1, (5, 10): 1, (4, 11): 1}, (4, 5): {(4, 4): 1, (4, 6): 1, (3, 5): 1}, (10, 13): {(9, 13): 4, (10, 14): 1, (10, 12): 1, (11, 13): 1}, (9, 3): {(9, 2): 1, (10, 3): 1, (9, 4): 1}, (6, 0): {(7, 0): 1}, (11, 0): {(10, 0): 1, (11, 1): 1}, (7, 5): {(8, 5): 1, (6, 5): 1}, (0, 1): {(0, 0): 1, (0, 2): 1, (1, 1): 1}, (3, 12): {(4, 12): 1, (3, 11): 1, (3, 13): 1}, (1, 12): {(1, 13): 1, (1, 11): 1, (2, 12): 1, (0, 12): 1}, (8, 12): {(7, 12): 1, (8, 11): 1, (8, 13): 1}, (3, 1): {(3, 0): 1, (3, 2): 1}, (2, 11): {(1, 11): 1, (2, 12): 1, (2, 10): 1}, (9, 9): {(8, 9): 1, (9, 8): 1, (10, 9): 1}, (5, 14): {(4, 14): 1}, (10, 14): {(10, 13): 1, (11, 14): 6}, (6, 13): {(6, 12): 1, (7, 13): 1, (6, 14): 1}, (7, 8): {(6, 8): 1, (7, 9): 1}, (0, 14): {(1, 14): 1, (0, 13): 1}, (3, 11): {(3, 10): 1, (3, 12): 1, (4, 11): 1}, (2, 1): {(2, 0): 1, (1, 1): 4}, (8, 9): {(8, 8): 4, (9, 9): 1, (8, 10): 1, (7, 9): 1}, (4, 12): {(4, 13): 1, (5, 12): 1, (3, 12): 1, (4, 11): 1}, (2, 12): {(2, 11): 1, (1, 12): 1}, (9, 4): {(9, 5): 1, (9, 3): 1}, (5, 1): {(5, 2): 1, (4, 1): 1, (5, 0): 1}, (10, 3): {(9, 3): 1, (11, 3): 1, (10, 2): 1}, (7, 2): {(7, 3): 1, (6, 2): 1, (8, 2): 1, (7, 1): 1}, (6, 14): {(7, 14): 1, (6, 13): 1}, (11, 10): {(11, 9): 1, (11, 11): 1, (10, 10): 1}, (1, 5): {(0, 5): 1, (2, 5): 1, (1, 6): 1}, (0, 11): {(1, 11): 1, (0, 10): 1, (0, 12): 1}, (3, 6): {(2, 6): 1, (3, 5): 4}, (2, 2): {(1, 2): 1}, (1, 10): {(0, 10): 1, (1, 9): 1}, (8, 6): {(8, 5): 1, (7, 6): 1, (9, 6): 1, (8, 7): 1}, (4, 1): {(5, 1): 1, (4, 0): 1}, (10, 9): {(10, 8): 1, (11, 9): 1, (9, 9): 1}, (9, 7): {(9, 8): 7, (9, 6): 1, (8, 7): 1}, (6, 4): {(6, 3): 1, (7, 4): 1, (5, 4): 1, (6, 5): 1}, (5, 4): {(6, 4): 1, (4, 4): 1, (5, 3): 1}, (11, 4): {(10, 4): 1, (11, 3): 1}, (10, 4): {(10, 5): 1, (11, 4): 1}, (7, 1): {(8, 1): 1, (6, 1): 1, (7, 0): 1, (7, 2): 1}, (6, 11): {(6, 12): 1, (6, 10): 1, (7, 11): 1, (5, 11): 5}, (11, 9): {(11, 10): 1, (10, 9): 1}, (0, 5): {(1, 5): 1, (0, 4): 1}, (1, 0): {(0, 0): 6, (1, 1): 1}, (0, 8): {(1, 8): 1, (0, 7): 1}, (4, 11): {(4, 12): 1, (3, 11): 1, (5, 11): 1}, (3, 5): {(4, 5): 1, (2, 5): 1, (3, 4): 1, (3, 6): 4}, (2, 7): {(3, 7): 1, (2, 6): 7, (2, 8): 1}, (9, 13): {(10, 13): 4, (9, 14): 1}, (8, 3): {(7, 3): 1, (8, 2): 1, (8, 4): 1}, (5, 10): {(5, 9): 1, (6, 10): 1, (4, 10): 1, (5, 11): 1}, (4, 6): {(5, 6): 1, (4, 5): 1}, (10, 10): {(9, 10): 1, (11, 10): 1}, (9, 2): {(9, 3): 1, (10, 2): 1}, (6, 1): {(6, 2): 1, (7, 1): 1}, (5, 7): {(6, 7): 1, (5, 8): 1}, (11, 3): {(11, 4): 1, (11, 2): 1, (10, 3): 1}, (7, 4): {(6, 4): 1}, (0, 2): {(0, 1): 1, (1, 2): 1}, (1, 3): {(1, 2): 1, (0, 3): 1, (2, 3): 1}, (8, 13): {(8, 14): 1, (8, 12): 1}, (4, 8): {(3, 8): 1, (5, 8): 1}, (3, 0): {(2, 0): 1, (3, 1): 1}, (2, 8): {(3, 8): 1, (2, 7): 1, (2, 9): 1}, (9, 8): {(8, 8): 1, (9, 9): 1, (9, 7): 7}, (8, 0): {(8, 1): 1, (9, 0): 1}, (5, 13): {(4, 13): 1, (5, 12): 1}, (6, 2): {(6, 3): 1, (6, 1): 1, (7, 2): 1}, (11, 14): {(10, 14): 6, (11, 13): 1}, (7, 11): {(6, 11): 1, (8, 11): 1, (7, 10): 1}, (3, 10): {(3, 9): 9, (3, 11): 1}, (1, 14): {(0, 14): 1, (2, 14): 6}, (8, 10): {(9, 10): 1, (8, 9): 1, (8, 11): 1}, (4, 13): {(4, 12): 1, (5, 13): 1, (4, 14): 1, (3, 13): 1}, (2, 13): {(2, 14): 9, (3, 13): 1}, (9, 11): {(8, 11): 1, (10, 11): 1}, (5, 0): {(5, 1): 1, (4, 0): 1}, (10, 0): {(11, 0): 1, (9, 0): 6}, (11, 13): {(10, 13): 1, (11, 12): 1, (11, 14): 1}, (7, 14): {(7, 13): 1, (6, 14): 1}, (1, 4): {(2, 4): 1, (0, 4): 1}, (0, 12): {(0, 11): 1, (0, 13): 1, (1, 12): 1}, (3, 9): {(3, 8): 1, (3, 10): 9, (4, 9): 1}, (2, 3): {(1, 3): 1, (3, 3): 1}, (1, 9): {(0, 9): 1, (1, 10): 1}, (8, 7): {(8, 6): 1, (7, 7): 2, (9, 7): 1}, (4, 2): {(3, 2): 1, (5, 2): 1}, (2, 14): {(2, 13): 9, (1, 14): 6, (3, 14): 1}, (9, 6): {(8, 6): 1, (9, 7): 1, (9, 5): 1}, (6, 5): {(6, 4): 1, (7, 5): 1}, (5, 3): {(6, 3): 5, (5, 4): 1, (5, 2): 1, (4, 3): 1}, (11, 7): {(10, 7): 1, (11, 8): 1, (11, 6): 1}, (10, 5): {(10, 4): 1, (11, 5): 1}, (7, 0): {(6, 0): 1, (7, 1): 1}, (6, 8): {(6, 9): 10, (7, 8): 1, (5, 8): 5}, (11, 8): {(10, 8): 1, (11, 7): 1}, (7, 13): {(7, 14): 1, (6, 13): 1}, (0, 6): {(1, 6): 1, (0, 7): 1}, (1, 7): {(0, 7): 1}, (0, 9): {(1, 9): 1}, (3, 4): {(3, 3): 1, (2, 4): 1, (3, 5): 1}, (2, 4): {(3, 4): 1, (1, 4): 1}, (9, 12): {(10, 12): 1}, (8, 4): {(8, 3): 1, (8, 5): 9}, (5, 9): {(4, 9): 1, (5, 10): 1}, (4, 7): {(3, 7): 2}, (10, 11): {(9, 11): 1, (10, 12): 1, (11, 11): 1}, (9, 1): {(8, 1): 1, (9, 0): 9}, (6, 6): {(5, 6): 5, (7, 6): 1, (6, 7): 1}, (5, 6): {(6, 6): 5, (5, 5): 10, (4, 6): 1}, (11, 2): {(11, 1): 1, (11, 3): 1, (10, 2): 1}, (10, 6): {(11, 6): 1}, (7, 7): {(8, 7): 2}, (0, 3): {(1, 3): 1, (0, 4): 1}, (3, 14): {(2, 14): 1, (3, 13): 1}, (1, 2): {(1, 1): 1, (1, 3): 1, (0, 2): 1, (2, 2): 1}, (8, 14): {(9, 14): 1, (8, 13): 1}, (4, 9): {(5, 9): 1, (3, 9): 1}, (3, 3): {(3, 4): 1, (3, 2): 1, (2, 3): 1, (4, 3): 1}, (2, 9): {(2, 8): 1, (2, 10): 1}, (8, 1): {(9, 1): 1, (8, 0): 1, (8, 2): 1, (7, 1): 1}, (5, 12): {(4, 12): 1, (5, 13): 1, (5, 11): 1}, (4, 4): {(4, 5): 1, (5, 4): 1, (4, 3): 1}, (10, 12): {(10, 11): 1, (10, 13): 1, (11, 12): 1, (9, 12): 1}, (6, 3): {(6, 4): 1, (5, 3): 5, (6, 2): 1, (7, 3): 1}, (11, 1): {(11, 0): 1, (11, 2): 1, (10, 1): 1}, (7, 10): {(7, 11): 1, (6, 10): 1, (7, 9): 1}, (0, 0): {(0, 1): 1, (1, 0): 6}, (3, 13): {(4, 13): 1, (2, 13): 1, (3, 12): 1, (3, 14): 1}, (1, 13): {(0, 13): 1, (1, 12): 1}, (8, 11): {(7, 11): 1, (9, 11): 1, (8, 10): 1, (8, 12): 1}, (4, 14): {(5, 14): 1, (4, 13): 1}, (2, 10): {(2, 11): 1, (2, 9): 1}, (9, 10): {(8, 10): 1, (10, 10): 1}, (10, 1): {(11, 1): 1, (10, 2): 1}, (6, 12): {(7, 12): 1, (6, 11): 1, (6, 13): 1}, (11, 12): {(10, 12): 1, (11, 13): 1}, (7, 9): {(8, 9): 1, (7, 8): 1, (7, 10): 1}, (0, 13): {(0, 14): 1, (1, 13): 1, (0, 12): 1}, (3, 8): {(3, 7): 1, (3, 9): 1, (4, 8): 1, (2, 8): 1}, (2, 0): {(3, 0): 1, (2, 1): 1}, (1, 8): {(0, 8): 1}, (8, 8): {(8, 9): 4, (9, 8): 1}, (4, 3): {(4, 4): 1, (3, 3): 1, (5, 3): 1}, (9, 5): {(9, 6): 1, (9, 4): 1}, (5, 2): {(4, 2): 1, (5, 3): 1, (5, 1): 1}, (11, 6): {(11, 7): 1, (10, 6): 1}, (10, 2): {(9, 2): 1, (11, 2): 1, (10, 3): 1, (10, 1): 1}}

import time

def test():
    maze = Maze(mazeMap, 15, 12)
    print("Matrix map :")
    print(maze.matrixMap)

    print("Astar test:")
    t = time.clock()
    r = maze.findMostRapidWay((11,0), (9,4))
    print(r)
    print('time : ' + str(time.clock() - t))
test()