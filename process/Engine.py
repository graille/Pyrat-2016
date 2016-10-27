# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

from includes.Maze import *
from includes.Rat import *

# Import algorithms
from algorithms.Dijkstra import *
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
        t = time.clock()

        # Add player and opponent to metaGraph
        self.maze.addNodeToMetagraph(self.player.location, self.CURRENT_CHEESES_LOCATION)
        self.maze.addNodeToMetagraph(self.opponent.location, self.CURRENT_CHEESES_LOCATION + [self.player.location])

        print("## Metagraph addition executed in " + str(time.clock() - t))

        # In case of particular reaction
        if self.player.destination and \
                (self.player.destination not in self.CURRENT_CHEESES_LOCATION or \
                (self.maze.distanceMetagraph[self.opponent.location][self.player.destination] <= 2 and self.maze.distanceMetagraph[self.player.location][self.player.destination] > 2) or \
                self.CURRENT_CHEESES_NB in [1, 2]):  # Si l'adversaire a déja manger notre fromage ou qu'il se trouve dans un rayon de 2 cases de celui-ci
            self.player.setPath(None)

        # If we need calculate a path
        if (not self.player.path) or \
                (len(self.player.path) == 1 and len(self.player.path[0]) <= 1) or \
                (not self.player.destination):

            print("### No destination detected : " + repr(self.player.destination)) if not self.player.destination else ()

            # If there is only one cheese
            if self.CURRENT_CHEESES_NB == 1:
                self.player.setPath([self.maze.getFastestPath(self.player.location, self.CURRENT_CHEESES_LOCATION[0])[1]])

            # If there are 2 cheeses
            elif self.CURRENT_CHEESES_NB == 2:
                factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
                n1, n2 = self.CURRENT_CHEESES_LOCATION[0], self.CURRENT_CHEESES_LOCATION[1]

                if factors[n1] < 1 and factors[n2] < 1:
                    if factors[n1] > factors[n2]:
                        goal = n1
                    else:
                        goal = n2
                elif factors[n1] < 1 and factors[n2] > 1:
                    goal = n1
                elif factors[n1] > 1 and factors[n2] < 1:
                    goal = n2
                else: # Both >= 1
                    if factors[n1] > factors[n2]:
                        goal = n2
                    else:
                        goal = n1

                self.player.setPath([self.maze.getFastestPath(self.player.location, goal)[1]])

            # In other cases
            else:
                # Update clusters rentability
                self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)

                self.clusterRentability = []

                for k in range(len(self.cluster)):
                    r, nb = 0, 0
                    if self.cluster[k][1]: # If the cluster is not empty
                        # TODO : Verifier que l'adversaire n'est pas dans ce cluster actuelement

                        for n in self.cluster[k][1]:
                            r += 1
                            nb += self.factors[n]

                        r = (len(self.cluster[k]) / (float(nb / r)), k)

                        self.clusterRentability.append(r)

                self.clusterRentability.sort()
                b_r, b_k = self.clusterRentability[-1]

                # Calculate Path
                d, p = np.inf, [] # A remplacer par un glouton plus tard
                k, init = 0, time.clock()

                while (time.clock() - t) < (self.TIME_ALLOWED * 70/100):
                    # Execute twoOPT
                    to = TwoOPT(self.maze, self.cluster[b_k][1] + [self.player.location], self.TIME_ALLOWED * 20/100)
                    to.process()

                    d_t, p_t = to.getResult(self.player.location)

                    if d_t < d:
                        d, p = d_t, p_t

                    k += 1

                print("# Path of " + repr(d) + " found in " + repr(k) + " tests and " + repr(time.clock() - init) + " seconds")

                # Set path
                self.player.setPath(self.maze.convertMetaPathToRealPaths(p))

        # Radar
        r_d, r_n = np.inf, None
        for n in self.CURRENT_CHEESES_LOCATION:
            # Check if we can have it
            if self.maze.distanceMetagraph[self.player.location][n] <= 2:

                # Check if the node is not in the path
                for li in self.player.path:
                    if n not in li:

                        # Check if the node is not for the opponent
                        if self.maze.distanceMetagraph[self.player.location][n] <= self.maze.distanceMetagraph[self.opponent.location][n]:

                            # Add n to path
                            if self.maze.distanceMetagraph[self.player.location][n] < r_d:
                                r_d, r_n = self.maze.distanceMetagraph[self.player.location][n], n

        if r_n:
            self.player.setPath([self.maze.pathMetagraph[self.player.location][r_n]] + [self.maze.pathMetagraph[r_n][self.player.destination]] + self.player.path[1::])

        # Check
        if (not self.player.path) or len(self.player.path[0]) <= 1:
            raise Exception("LE PATH EST VIDE ! " + repr(self.player.path) + " | Cheeses ("+ repr(len(self.CURRENT_CHEESES_LOCATION)) + ") " + repr(self.CURRENT_CHEESES_LOCATION))

        # Select next node
        current_node, next_node = self.player.path[0][0], self.player.path[0][1]
        print("# Next node : " + repr(next_node))
        self.player.path[0] = self.player.path[0][1::]

        # Return path
        print("# Turn executed in " + repr(time.clock() - t) + " seconds")

        if time.clock() - t > 0.1:
            raise Exception("Temps dépasser")
        try:
            return self.maze.getMove(current_node, next_node)
        except TypeError:
            print("ERROR")
            print("Path : " + repr(self.player.path))
            print("Cheeses : " + repr(self.CURRENT_CHEESES_LOCATION))
            exit()

    def update(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed, PREPROCESSING = False):
        # If it's the first update (we are in the preprocessing)
        if PREPROCESSING:
            b_t = time.clock()
            # Create players
            self.player = Player(playerLocation)
            self.opponent = Opponent(opponentLocation)

            # Create Metagraph
            self.maze.createMetaGraph(piecesOfCheese)
            print("## Metagraph generated in " + repr(time.clock() - b_t))

            # Get the total number of cheeses
            self.TOTAL_CHEESES = len(piecesOfCheese)
            self.INITIAL_CHEESES = piecesOfCheese

            # Add player and opponent to metaGraph

            # Create clusters
            nb_cluster = round(self.TOTAL_CHEESES / 6)
            alg = K_Means(self.maze, nb_cluster, self.INITIAL_CHEESES)

            result = alg.process((timeAllowed - (time.clock() - b_t)) * (95/100))

            print("## Clusters : " + repr(alg.k) + " clusters have been generated")

            # Checks clusters
            tot_cheeses = 0
            for i in range(nb_cluster):
                self.cluster.append((len(result[1][i]), result[1][i]))
                self.clusterMiddle.append(result[0][i])
                tot_cheeses += len(result[1][i])

            # Check the total number of cheeses
            if not tot_cheeses == len(piecesOfCheese):
                print("# All cheeses has not been put in a cluster !!")
                pass

            # TODO : vérifié le nombre total de fromage, ajouté un cluster spécial pur les fromages non référencés

            print("# Pre-execution executed in " + repr(time.clock() - b_t) + " seconds")

        b_t = time.clock()

        # Update cluster (delete old cheeses)
        for cheese in self.CURRENT_CHEESES_LOCATION:
            if cheese not in piecesOfCheese:
                for k in range(len(self.cluster)):
                    if cheese in self.cluster[k][1]:

                        self.cluster[k][1].remove(cheese)

                    # If the cluster is empty, We delete it
                    if len(self.cluster[k]) == 0:
                        self.cluster.remove(self.cluster[k])

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
        self.TIME_ALLOWED = timeAllowed

        print("# Update executed in " + repr(time.clock() - b_t) + " seconds")

    # Factors management
    def calculateFactors(self, nodes):
        try:
            # Calculate factors
            factors = {}

            for n in nodes:
                factors[n] = float(self.maze.distanceMetagraph[self.player.location][n] / self.maze.distanceMetagraph[self.opponent.location][n])

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
