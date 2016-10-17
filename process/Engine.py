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

# Import libs
import time

class Engine:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        # Cache maze and algorithms
        self.maze = Maze(mazeMap, mazeWidth, mazeHeight)

        # Init vars
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8

        self.CURRENT_CHEESES_LOCATION = []
        self.CURRENT_CHEESES_NB = 0

        # Cache players
        self.player = None
        self.opponent = None

        # Cache clusters
        self.cluster = []
        self.clusterMiddle = []
        self.clusterRentability = []

        self.factors = {}

    def turn(self):
        if self.CURRENT_CHEESES_NB == 1:
            alg = Astar(self.maze)
            alg.setOrigin(self.player.location)
            alg.setGoal(self.CURRENT_CHEESES_LOCATION[0])
            alg.process()

            self.player.path = alg.getResult()[1]
        elif self.CURRENT_CHEESES_NB == 2:
            factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
            n1, n2 = self.CURRENT_CHEESES_LOCATION[0], self.CURRENT_CHEESES_LOCATION[1]

            alg = Astar(self.maze)
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

            # If we need to create a path
            if not self.player.path or self.player.destination not in self.CURRENT_CHEESES_LOCATION:
                # Update clusters rentability
                self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION, True)
                b_r, b_k = -1, -1

                for k in range(len(self.cluster)):
                    r, nb = 0, 0
                    for n in self.cluster[k]:
                        r += 1
                        nb += self.factors[n]
                    self.clusterRentability.append(len(self.cluster[k]) / (float(nb / r)))

                    if self.clusterRentability[-1] > b_r:
                        b_r = self.clusterRentability[-1]
                        b_k = k

                # Calculate Path
                to = TwoOPT(self.maze)
                to.setOrigin(self.player.location)
                to.setGoals(self.cluster[b_k])

                to.process()
                d, p = to.getResult()

                # Set path
                self.player.path = self.maze.concatPaths(self.maze.convertMetaPathToRealPaths(p))

            else:
                checker = 2
                # Check around player
                for n in self.CURRENT_CHEESES_LOCATION:
                    if self.maze.distanceMetagraph[self.player.location][n] <= checker and n != self.player.destination \
                            and (not self.inPath(self.player, n)) and (not self.isInteresting(self.player, n)):
                        self.addToPath(self.player, n)
                        checker = 1

        # Return path
        way = self.player.path[0]
        self.player.path = self.player.path[1::] if len(self.player.path) > 1 else []
        return way

    def isInteresting(self, player, node):
        # On regarde si ce noeud ne nous fait pas retournée en arrière...
        pass

    def addToPath(self, player, node):
        print("## Chemin détourné pour aller sur " + repr(node))
        if node in self.maze.getNeighbors(player.location):
            pass
        else:
            pass

    def inPath(self, player, node):
        pass

    def update(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed, PREPROCESSING = False):
        b_t = time.clock()
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
            alg.setK(9)

            result = alg.process((timeAllowed - (time.clock() - b_t)) * (1/3))

            for i in range(len(result[1])):
                self.cluster.append((len(result[1][i]), result[1][i]))
                self.clusterMiddle.append(result[0][i])

            # TODO : vérifié le nombre total de fromage, ajouté un cluster spécial pur les fromages non référencés

            print("# Preprocessing executed in " + repr(time.clock() - b_t) + " seconds")
            print(self.cluster)

        # Update cluster (delete old cheeses)
        for cheese in self.CURRENT_CHEESES_LOCATION:
            if cheese not in piecesOfCheese:
                for k in range(len(self.cluster)):
                    if cheese in self.cluster[k]:
                        self.cluster[k].remove(cheese)

        # Miscellaneous
        self.CURRENT_CHEESES_NB = len(piecesOfCheese)
        self.CURRENT_CHEESES_LOCATION = piecesOfCheese

        # Update locations
        self.player.setLocation(playerLocation)
        self.opponent.setLocation(opponentLocation)

        # Update scores
        self.player.score = playerScore
        self.opponent.score = opponentScore

        print("# Update executed in " + repr(time.clock() - b_t) + " seconds")

    # Factors management
    def calculateFactors(self, nodes, metaGraph = False):
        if metaGraph:
            # Calculate factors
            factors = {}

            for c in nodes:
                factors[c] = float(self.maze.distanceMetagraph[self.player.location][c] / self.maze.distanceMetagraph[self.opponent.location][c])
        else:
            alg = Dijkstra(self.maze)

            # Calculate for player
            alg.setGoal(None)
            alg.setOrigin(self.player.location)
            alg.process()

            playerResult = alg.dist

            # Calculate for opponent
            alg.setGoal(None)
            alg.setOrigin(self.opponent.location)
            alg.process()

            opponentResult = alg.dist

            # Calculate factors
            factors = {}
            for c in nodes:
                factors[c] = float(playerResult[c] / opponentResult[c])

        return factors