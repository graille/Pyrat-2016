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
from algorithms.Kmeans import *
# Debug
from debug.Debug import *

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

class Engine:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        # Cache maze and algorithms
        self.maze = Maze(mazeMap, mazeWidth, mazeHeight)
        self.algorithms = AlgorithmsList(self.maze)

        # Init vars
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8

        # Cache players
        self.player = None
        self.opponent = None

        # Cache clusters
        self.cluster = []
        self.clusterMiddle = []

    def turn(self):
        if self.CURRENT_CHEESES_NB == 1:
            alg = self.algorithms.get('astar')
            alg.setOrigin(self.player.location)
            alg.setGoal(self.CURRENT_CHEESES_LOCATION[0])
            alg.process()

            self.player.path = alg.getResult()[1]
        elif self.CURRENT_CHEESES_NB == 2:
            factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
            n1, n2 = self.CURRENT_CHEESES_LOCATION[0], self.CURRENT_CHEESES_LOCATION[1]

            alg = self.algorithms.get('astar')
            alg.setOrigin(self.player.location)

            if factors[n1] <= 1 and factors[n2] <= 1:
                if factors[n1] > factors[n2]:
                    alg.setGoal(n1)
                    alg.process()
                else:
                    alg.setGoal(n2)
                    alg.process()

                self.player.path = alg.getResult()[1]
            elif factors[n1] < 1 and factors[n2] > 1:
                alg.setGoal(n1)
                alg.process()

                self.player.path = alg.getResult()[1]
            elif factors[n1] > 1 and factors[n2] < 1:
                alg.setGoal(n2)
                alg.process()

                self.player.path = alg.getResult()[1]
            else:
                if factors[n1] > factors[n2]:
                    alg.setGoal(n2)
                    alg.process()
                else:
                    alg.setGoal(n1)
                    alg.process()

                self.player.path = alg.getResult()[1]
        else:
            # Add player and opponent to metaGraph
            self.maze.addNodeToMetagraph(self.player.location, self.CURRENT_CHEESES_LOCATION)
            self.maze.addNodeToMetagraph(self.opponent.location, self.CURRENT_CHEESES_LOCATION + [self.player.location])

            # Update DF_MAX
            self.DF_MAX = (self.TOTAL_CHEESES - self.player.score) / (self.TOTAL_CHEESES - self.opponent.score)

            if not self.player.path or self.player.destination not in self.CURRENT_CHEESES_LOCATION:
                # Update clusters
                alg = K_Means(self.maze)
                alg.setNodes(self.CURRENT_CHEESES_LOCATION)
                alg.setK(round(self.CURRENT_CHEESES_NB * 7 / self.INITIAL_CHEESES))

                result = alg.process(10)

                # Detect nearest cluster
                dij = Dijkstra(self.maze)


            # Get cheeses we can have
            #self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION, True)
            #self.EXPLOITABLE_CHEESES = self.returnUnderValue(self.factors, self.DF_MAX, False)

        # Return path
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
            self.maze.createMetaGraph(piecesOfCheese)

            # Get the total number of cheeses
            self.TOTAL_CHEESES = len(piecesOfCheese)
            self.INITIAL_CHEESES = piecesOfCheese

            # Create clusters
            alg = K_Means(self.maze)
            alg.setNodes(piecesOfCheese)
            alg.setK(7)

            result = alg.process(500)

            for i in range(len(result[1])):
                self.cluster.append((len(result[1][i]), result[1][i]))
                self.clusterMiddle.append(result[0][i])

        # Miscellaneous
        self.CURRENT_CHEESES_NB = len(piecesOfCheese)
        self.CURRENT_CHEESES_LOCATION = piecesOfCheese

        # Update locations
        self.player.setLocation(playerLocation)
        self.opponent.setLocation(opponentLocation)

        # Update scores
        self.player.score = playerScore
        self.opponent.score = opponentScore

    # Factors management
    def calculateFactors(self, nodes, metaGraph = False):
        if metaGraph:
            # Calculate factors
            factors = {}

            for c in nodes:
                factors[c] = float(self.maze.distanceMetagraph[self.player.location][c] / self.maze.distanceMetagraph[self.opponent.location][c])
        else:
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