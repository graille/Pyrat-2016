# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:55 2016

@author: Thibault/Clément
"""
import numpy as np

# Import algorithms
from algorithms.Astar import *
from algorithms.FloydWarshall import *
from algorithms.Dijkstra import *

class Maze:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight
        self.nodes = list(self.mazeMap.keys())

        # Init matrixMap
        self.matrixMap = {}

        # Init metagraph
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

    def reversePath(self, path):
        """
        Inverse un chemin symétriquement par rapport a la diagonale
        :param path:
        :return:
        """
        r = ""
        for l in path:
            if l == 'D':
                r += 'U'
            if l == 'U':
                r += 'D'
            if l == 'R':
                r += 'L'
            if l == 'L':
                r += 'R'

        return r

    def getDistance(self, from_location, to_location):
        try:
            return self.mazeMap[from_location][to_location]
        except KeyError:
            return np.inf

    def getMove(self, origin, goal):
        """
        Retourne le mouvement à effectuer pour aller de origin à goal,
        qui doivent être adjacentes
        :param origin:
        :param goal:
        :return: bool
        """
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