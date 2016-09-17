#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np

TEAM_NAME = "DreamTeam"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

DIMENSION_N = 15 #Vertical
DIMENSION_M = 15 #Horizontale
NB_CASES = DIMENSION_N * DIMENSION_M
class Maze():
    def __init__(self, location):
        self.location = location
    def canMove(self, mazeMap, dest):
        pass
        
class Graph():
    def __init__(self, mazeMap):
        """Initialise la classe graphe et crée une matrice d'adjacence matrixMap"""
        self.mazeMap = mazeMap
        self.convertToMatrix()

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


def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    print("<b>[mazeMap]</b> " + repr(mazeMap))
    print("<b>[mazeWidth]</b> " + repr(mazeWidth))
    print("<b>[mazeHeight]</b> " + repr(mazeHeight))
    print("<b>[playerLocation]</b> " + repr(playerLocation))
    print("<b>[opponentLocation]</b> " + repr(opponentLocation))
    print("<b>[piecesOfCheese]</b> " + repr(piecesOfCheese))
    print("<b>[timeAllowed]</b> " + repr(timeAllowed))

def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    
    # Example print that appears in the shell at every turn
    print("Move: [" + MOVE_UP + "]")
    
    # We always go up
    return MOVE_UP



###################################################################################################################################################################################################################################
###################################################################################################################################################################################################################################