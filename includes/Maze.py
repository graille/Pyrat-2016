# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:55 2016

@author: Thibault/Clément
"""

from algorithms.Astar import *
from algorithms.FloydWarshall import *

import numpy as np


class Maze:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight

        self.pathMatrix = None
        self.matrixMap = None

        self.convertToMatrix()
        self.nodes = list(self.getNodes())

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
        if origin != goal:
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
        else:
            return False

    def getNeighbors(self, position):
        return self.mazeMap[position].keys()