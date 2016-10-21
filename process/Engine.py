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
            if not self.player.path or (self.player.location != self.player.destination and self.player.destination not in self.CURRENT_CHEESES_LOCATION):
                # We activate the checker
                self.CHECKER = True

                if self.player.waitingPaths:
                    # TODO : Ici, il y a une erreur, si l'enemie a manger le fromage qu'on cherche, car on a un chemin faux, solution : séparer la condition juste au dessus en plusieurs sous-cas
                    self.player.path = self.player.waitingPaths[0]
                    self.player.waitingPaths = self.player.waitingPaths[1::] if (len(self.player.waitingPaths) > 1) else []
                    self.player.destination = self.player.path[-1]
                else:
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
                            b_r, b_k = self.clusterRentability[-1], k

                    # Calculate Path
                    to = TwoOPT(self.maze)
                    to.setOrigin(self.player.location)
                    to.setGoals(self.cluster[b_k])

                    to.process()
                    d, p = to.getResult()

                    # Set path
                    self.player.waitingPaths = self.maze.convertMetaPathToRealPaths(p)
            else:
                # Check around player
                if self.CHECKER:
                    for n in self.CURRENT_CHEESES_LOCATION:
                        if self.maze.distanceMetagraph[self.player.location][n] <= self.CHECKER_RADIUS and n != self.player.destination and (not self.inPath(self.player, n)):
                            path_to_n = self.maze.pathMetagraph[self.player.location][n]
                            path_to_n = self.maze.convertToRealPath(self.player.location, path_to_n)

                            if path_to_n:
                                self.addToPath(self.player, path_to_n)
                                self.CHECKER = False
                                break

        # Return path
        way = self.player.path[0]
        self.player.path = self.player.path[1::] if len(self.player.path) > 1 else []
        return way

    def isInteresting(self, player, node):
        return True

    def addToPath(self, player, path_to_goal, goal):
        print("## Chemin détourné pour aller sur " + repr(goal))

        # Recherche d'un nouveau chemin pour repartir sur notre état d'origine
        ast = Astar(self.maze, goal, player.destination)
        ast.process()
        d, P = ast.getResult()

        P = self.maze.convertToRealPath(player.location, P)

        # Ajout du chemin
        player.destination = goal
        player.path = path_to_goal
        player.waitingPaths = [P] + player.waitingPaths

    def inPath(self, player, node):
        return (node in player.path)

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
            nb_cluster = int(len(piecesOfCheese) / 4 - 1)
            alg = K_Means(self.maze)
            alg.setNodes(piecesOfCheese)
            alg.setK(nb_cluster)

            print("# " + repr(nb_cluster) + " clusters have been generated")

            result = alg.process((timeAllowed - (time.clock() - b_t)) * (1/3))
            tot_cheeses = 0

            for i in range(nb_cluster):
                self.cluster.append((len(result[1][i]), result[1][i]))
                self.clusterMiddle.append(result[0][i])
                tot_cheeses += len(result[1][i])

            # Check the total number of cheeses
            if not tot_cheeses == len(piecesOfCheese):
                print("# All cheeses has not been put in a cluster !!")

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

        # Update radius
        self.CHECKER_RADIUS = 2
        print("# Update executed in " + repr(time.clock() - b_t) + " seconds")

    # Factors management
    def calculateFactors(self, nodes):
        try:
            # Calculate factors
            factors = {}

            for c in nodes:
                factors[c] = float(self.maze.distanceMetagraph[self.player.location][c] / self.maze.distanceMetagraph[self.opponent.location][c])

            return factors
        except KeyError:
            print("# Factors calculated without metaGraph")
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