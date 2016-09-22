# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:55 2016

@author: Thibault/Clément
"""

from numpy import *
from ..process.algorithms import Astar
from ..process.algorithms import FloydWarshall

class Maze(object):
    def __init__(self, mazeMap, mazeWidth, mazeHeight, piecesOfCheese):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight

        self.pathMatrix = None
        self.matrixMap = None

        self.convertToMatrix()
        self.FM = FloydWarshall(self)
        self.FM.process()

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
        self.pathMatrix = np.array([[None for i in range(self.NB_CASES)]for j in range(self.NB_CASES)]) # Matrice qui donne les chemins minimaux entre deux cases
        for i in range(self.NB_CASES):
            for j in range(self.NB_CASES):
                self.pathMatrix[i][j] = []

        self.matrixMap = np.array([[np.inf if i != j else 0 for i in range(self.NB_CASES)] for j in range(self.NB_CASES)]) # On crée une matrice contenant que des -1 sauf sur la diagonale
        for locationCaseAccessible1 in self.mazeMap:
            cle_case1 = self.location_to_id(locationCaseAccessible1)
            for locationCaseAccessible2 in self.mazeMap[locationCaseAccessible1]:
                cle_case2 = self.location_to_id(locationCaseAccessible2)
                self.matrixMap[cle_case1][cle_case2],self.matrixMap[cle_case2][cle_case1] = self.mazeMap[locationCaseAccessible1][locationCaseAccessible2],self.mazeMap[locationCaseAccessible1][locationCaseAccessible2]
                self.pathMatrix[cle_case1][cle_case2] = self.getMove(locationCaseAccessible1, locationCaseAccessible2)
                self.pathMatrix[cle_case2][cle_case1] = self.getMove(locationCaseAccessible2, locationCaseAccessible1)
    
    def calculateMetaGraph(self, from_location, to_location_list):
        """Remplit les cases de la matrice des distances uniquement pour les cases spécifiées"""
        from_location_ID = self.location_to_id(from_location)

        for to_location in to_location_list :
            to_location_ID = self.location_to_id(to_location)

            astar = Astar(self, from_location, to_location)

            (dist, path) = astar.process()
            self.pathMatrix[from_location_ID, to_location_ID] = path
            self.matrixMap[from_location_ID, to_location_ID] =  dist

    def getDistance(self, from_location, to_location):
        from_location_ID, to_location_ID = self.location_to_id(from_location), self.location_to_id(to_location)

        return self.pathMatrix[from_location_ID, to_location_ID]

    def getNodes(self):
        return self.mazeMap.keys()
    
    def findMostRapidWay(self, origin, goal):
        al = Astar(self, origin, goal)
        al.process()

        return al.result
    
    def getNeighbors(self, position):
        return self.arrayMap[position].keys()
