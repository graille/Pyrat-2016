# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:55 2016

@author: Thibault/Clément
"""

from numpy import *
from . import Rat

class Graph(object):
    pass

class Maze(Graph):
    def __init__(self, mazeMap):
        self.arrayMap = mazeMap
        self.matrixMap = self.convertToMatrix(mazeMap)
        
    def location_to_id(self, location):
        """Converti les coordonnees d'une case en sa cle primaire"""
        x,y  = location[0], location[1]
        id_case = x*DIMENSION_M+y
        return id_case
    def id_to_location(self, id_case):
        """Converti la cle primaire d'une case en ses coordonnees"""
        location = (id_case//DIMENSION_M, id_case%DIMENSION_M)
        return location
    def convertToMatrix(self):
        """
        Prend en argument 
        Renvoie une matrice où les cases sont triées en fonction de leur id et où 
        -1 signifie qu'il n'y a pas de passage direct entre les deux cases, 
        1 signifie qu'il y a passage et 0 que l'on reste sur la même case
        """
        self.matrixMap = np.array([[ -1 if i != j else 0 for i in range(NB_CASES)] for j in range(NB_CASES)]) #On crée une matrice contenant que des -1 sauf sur la diagonale
        for locationCaseAccessible1 in self.mazeMap:
            cle_case1 = self.location_to_id(locationCaseAccessible1)
            for locationCaseAccessible2 in self.mazeMap[locationCaseAccessible1]:
                cle_case2 = self.location_to_id(locationCaseAccessible2)
                self.matrixMap[cle_case1][cle_case2],self.matrixMap[cle_case2][cle_case1] = self.mazeMap[locationCaseAccessible1][locationCaseAccessible2],self.mazeMap[locationCaseAccessible1][locationCaseAccessible2]

    
    def calculateMetaGraph(self, from_position, point_list):
        pass
    
    def getNodes():
        pass
    
    def findMostRapidWay(from_pos, to_pos)
        pass
    
    def getNeighbors(self, position):
        return self.arrayMap[position]
        
    def getCost(self, n1, n2):
        return self.matrixMap[n1, n2]
