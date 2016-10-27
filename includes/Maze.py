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
            if to_location == from_location:
                return 0
            else:
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

    def convertMetaPathToRealPaths(self, pathMeta):
        path = []
        for k in range(len(pathMeta) - 1):
            path.append(self.pathMetagraph[pathMeta[k]][pathMeta[k+1]])

        return path

    def convertToRealPath(self, origin, pathNodes):
        L = [origin]

        x, y = origin
        for elt in pathNodes:
            if elt == 'L':
                y -= 1
            if elt == 'U':
                x -= 1
            if elt == 'D':
                x += 1
            if elt == 'R':
                y += 1
            L.append((x, y))

        return L

    def concatPaths(self, paths):
        r = ""
        for path in paths:
            r += path

        return r

    def createMetaGraph(self, cheeses_list):
        """
        Create the pattern of the metagraph(distance between cheeses
        :param nodes_list: List of currents cheeses
        :return:
        """
        dij = Dijkstra(self)
        for n1 in cheeses_list:
            self.distanceMetagraph[n1] = {}
            self.pathMetagraph[n1] = {}

            # Calculate path and distance with Dijkstra
            dij.setOrigin(n1)
            dij.setGoal(None)
            dij.process()

            for n2 in cheeses_list:
                result = dij.getResult(n2)
                self.distanceMetagraph[n1][n2] = result[0]
                self.pathMetagraph[n1][n2] = result[1]

    def addNodeToMetagraph(self, node, nodes_list):
        """
        Ajoute le noeud "node" par rapports aux nodes "nodes_list" qui doivent déja exister dans le metaGraph
        :param node: noeud a ajouter ou uploader
        :param nodes_list:
        :return:
        """

        dij = Dijkstra(self, node, None)
        dij.process()

        for n in nodes_list:
            d, p = dij.getResult(n)
            self.coupleNodesInMetagraph(node, n, d, p)

    def coupleNodesInMetagraph(self, n1, n2, d, p):
        if n1 in self.distanceMetagraph:
            self.distanceMetagraph[n1] = {}
            self.pathMetagraph[n1] = {}

        self.distanceMetagraph[n1][n2] = d
        self.pathMetagraph[n1][n2] = p

        if n2 not in self.distanceMetagraph:
            self.distanceMetagraph[n2] = {}
            self.pathMetagraph[n2] = {}

        self.distanceMetagraph[n2][n1] = d
        self.pathMetagraph[n2][n1] = p

    # Algoritms application
    def getFatestPath(self, origin, goal):
        try:
            return (self.distanceMetagraph[origin][goal], self.pathMetagraph[origin][goal])
        except KeyError:
            print("## Need to calculate the fastest path from " + repr(origin) + " to " + repr(goal))

            # Calculate path and distance with Astar
            dij = Astar(self, origin, goal)
            dij.process()

            d, p = dij.getResult()

            # Addto metagraph for a next time
            self.coupleNodesInMetagraph(origin, goal, d, p)

            return (d, p)

    def getNearestNode(self, origin, nodes):
        dij = Dijkstra(self)
        dij.setOrigin(origin)
        dij.setGoal(None)

        dij.process()

        n_list = [dij.getResult(n) for n in nodes]
        n_list.sort()

        return n_list[0] if len(n_list) > 0 else (0, [])