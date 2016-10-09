# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

from includes.Maze import *
from includes.Rat import *

# Import algorithms
from algorithms.Dijkstra import *
from algorithms.Astar import *
from algorithms.TwoOPT import *

# Import enumrations
from process.Enums import *


class AlgorithmsList:
    def __init__(self, maze):
        self.algorithms = {}
        self.maze = maze

        self.initAlgorithms()

    def initAlgorithms(self):
        self.algorithms['dijkstra'] = Dijkstra(self.maze)
        self.algorithms['astar'] = Astar(self.maze)
        self.algorithms['twoopt'] = TwoOPT(self.maze)

    def get(self, name):
        return self.algorithms[name]


class MazeController:
    def __init__(self, maze, algorithms):
        self.maze = maze
        self.algorithms = algorithms

    def fastestPathToNode(self, origin, goal):
        """
        Find the fastest path from origin to goal
        :param origin:
        :param goal:
        :return:
        """
        al = dij = self.algorithms.get('astar')

        al.setOrigin(origin)
        al.setGoal(goal)

        al.process()

        return al.getResult()

    def createMetaGraph(self, player, nodes_list):
        """
        Remplit les cases du dictionnaire d'adjacence et du dictionnaire de chemins pour les cases spécifiées
        :param player: A Rat instance (player or opponnent)
        :param nodes_list: List of currents cheeses
        :return:
        """

        dij = self.algorithms.get('dijkstra')

        # Initiliaze cells for player location
        self.maze.distanceMetagraph[GameEnum.LOCATION_LABEL] = {}
        self.maze.pathMetagraph[GameEnum.LOCATION_LABEL] = {}
        self.maze.distanceMetagraph[GameEnum.LOCATION_LABEL][GameEnum.LOCATION_LABEL] = 0
        self.maze.pathMetagraph[GameEnum.LOCATION_LABEL][GameEnum.LOCATION_LABEL] = ""

        for n1 in nodes_list:
            self.maze.distanceMetagraph[n1] = {}
            self.maze.pathMetagraph[n1] = {}

            # Calculate path and distance with Dijkstra
            dij.setOrigin(n1)
            dij.setGoal(None)
            dij.process()

            for n2 in nodes_list:
                result = dij.getResult(n2)
                self.maze.distanceMetagraph[n1][n2] = result[0]
                self.maze.pathMetagraph[n1][n2] = result[1]

            # Initiliaze subcells for player location
            self.maze.distanceMetagraph[n1][GameEnum.LOCATION_LABEL] = {}
            self.maze.pathMetagraph[n1][GameEnum.LOCATION_LABEL] = {}

        self.updateMetaGraph(player, nodes_list)

    def updateMetaGraph(self, player, nodes_list):
        """
        :param player: A Rat instance (player or opponnent)
        :param nodes_list: List of currents cheeses
        :return:
        """
        dij = self.algorithms.get('dijkstra')

        dij.setOrigin(player.location)
        dij.setGoal(None)
        dij.process()

        for n in nodes_list:
            result = dij.getResult(n)
            self.maze.distanceMetagraph[GameEnum.LOCATION_LABEL][n] = result[0]
            self.maze.pathMetagraph[GameEnum.LOCATION_LABEL][n] = result[1]

            self.maze.distanceMetagraph[n][GameEnum.LOCATION_LABEL] = result[0]
            self.maze.pathMetagraph[n][GameEnum.LOCATION_LABEL] = result[1]


class Engine:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        # Cache maze and algorithms
        self.maze = Maze(mazeMap, mazeWidth, mazeHeight)
        self.algorithms = AlgorithmsList(self.maze)
        self.mazeController = MazeController(self.maze, self.algorithms)

        # Init vars
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8

        # Cache players
        self.player = None
        self.opponent = None

    def turn(self):
        if not self.player.path:
            algorithm = self.algorithms.get('dijkstra')

            # Calculate for player
            algorithm.setGoal(None)
            algorithm.setOrigin(self.player.location)
            algorithm.process()

            r = []
            for k in self.CURRENT_CHEESES_LOCATION:
                r.append(algorithm.getResult(k))

            r.sort()
            self.player.path = (r[::-1].pop())[1]
            print("Current cheeses" + repr(self.CURRENT_CHEESES_LOCATION))
            print("New path for player : " + repr(self.player.path))

        way = self.player.path[0]
        self.player.path = self.player.path[1::] if len(self.player.path) > 1 else []
        return way

    def update(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed, PREPROCESSING = False):
        # If it's the first update (we are in the preprocessing)
        if PREPROCESSING:
            # Create players
            self.player = Player(playerLocation)
            self.opponent = Opponent(opponentLocation)

            # Create Metagraph
            self.mazeController.createMetaGraph(self.player, piecesOfCheese)

            # Get the total number of cheeses
            self.TOTAL_CHEESES = len(piecesOfCheese)

        # Miscellaneous
        self.CURRENT_CHEESES_NB = len(piecesOfCheese)
        self.CURRENT_CHEESES_LOCATION = piecesOfCheese

        # Update locations
        self.player.location = playerLocation
        self.opponent.location = opponentLocation

        # Update scores
        self.player.score = playerScore
        self.opponent.score = opponentScore

        # Update DF_MAX
        self.DF_MAX = (self.TOTAL_CHEESES - self.player.score) / (self.TOTAL_CHEESES - self.opponent.score)

        self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
        self.EXPLOITABLE_CHEESES = self.returnUnderValue(self.factors, self.DF_MAX, False)

    # Factors management
    def calculateFactors(self, nodes):
        algorithm = self.algorithms.get('dijkstra')

        # Calculate for player
        algorithm.setGoal(None)
        algorithm.setOrigin(self.player.location)
        algorithm.process()

        playerResult = algorithm.dist

        # Calculate for opponent
        algorithm.setGoal(None)
        algorithm.setOrigin(self.opponent.location)
        algorithm.process()

        opponentResult = algorithm.dist

        # Calculate factors
        factors = {}

        for c in nodes:
            factors[c] = float(playerResult[c] / opponentResult[c])

        return factors

    @staticmethod
    def returnUnderValue(factors, VAL_MAX, OR_EQUAL = False):
        result = {}
        for n in factors.keys():
            if OR_EQUAL:
                if factors[n] <= VAL_MAX:
                    result[n] = factors[n]
            else:
                if factors[n] < VAL_MAX:
                    result[n] = factors[n]

        return result