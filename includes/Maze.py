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
        self.nodes = list(self.getNodes())


        self.pathMatrix = None
        self.matrixMap = {}

        self.convertToMatrix()

        # Metagraph

        self.distanceMetagraph = {} # matrice des distances du métagraph sous forme de dictionnaire
        self.pathMetagraph = {} # matrice des chemins du métagraph sous forme de dictionnaire

    def convertToMatrix(self):
        """
        Prend en argument
        Renvoie une un dictionnaire où les clefs sont les clefs sont des cases et où
        np.inf signifie qu'il n'y a pas de passage direct entre les deux cases,
        n>0 signifie qu'il y a passage en n coups et 0 que l'on reste sur la même case
        """
        for n in self.nodes:
            self.matrixMap[n] = {}

        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1 == n2:
                    self.matrixMap[n1][n1] = 0
                elif n2 in self.mazeMap[n1]:
                    self.matrixMap[n1][n2] = self.mazeMap[n1][n2]
                    self.matrixMap[n2][n1] = self.mazeMap[n2][n1]
                else:
                    self.matrixMap[n1][n2] = np.inf
                    self.matrixMap[n2][n1] = np.inf

    def calculateMetaGraph(self, from_location, to_location_list):
        """Remplit les cases du dictionnaire d'adjacence et du dictionnaire de chemins pour les cases spécifiées"""
        bfs = BFS_P(self.matrixMap, from_location, to_location_list)
        bfs.process()
        for to_location in to_location_list:
            self.distanceMetagraph[from_location][to_location] = bfs.getWeight(to_location)
            self.pathMetagraph[from_location][to_location] = bfs.getPath(to_location)

    def getDistance(self, from_location, to_location):
        return self.matrixMap[from_location][to_location]

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