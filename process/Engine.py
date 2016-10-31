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
import numpy as np
import numpy.linalg as lg

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
        self.cluster = {}
        self.clusterMiddle = {}
        self.clusterApproxMiddle = {}
        self.clusterRentability = []

        self.clusterDistance = {}

        self.factors = {}

        # MODES
            # Current mode : 2 = NORMAL
            # 1 = TWO CHEESES
            # 0 = ONE CHEESE
        self.current_mode = 2

        # Parameters
        self.FACTOR_METHOD = 1 # [1,2]
        self.RENTABILITY_METHOD = 5 # [1, 2, 3]
        self.NB_CLUSTER = 2 # [2 - 10]

        self.RADAR_RADIUS = 2 # [0 - 5]
        self.ABORT_RADIUS = 5 # [0 - 7]
        self.OPPONENT_ABORT_RADIUS = 5 # [0 - 30]

        self.TEST = []

    #### CLUSTERS MANAGEMENT
    def getClusterFactor(self, k):
        if self.FACTOR_METHOD == 1:
            r, nb = 0, 0
            if self.cluster[k]:  # If the cluster is not empty
                for n in self.cluster[k]:
                    r += 1
                    nb += self.factors[n]

                return len(self.cluster[k]) / (float(nb / r))
            else:
                return 0
        elif self.FACTOR_METHOD == 2:
            nb = 1
            if self.cluster[k]:  # If the cluster is not empty
                for n in self.cluster[k]:
                    nb *= self.factors[n]

                return len(self.cluster[k]) / nb
            else:
                return 0

    def getClusterDistance(self, i, j):
        if i != j:
            return self.maze.distanceMetagraph[self.clusterApproxMiddle[i]][self.clusterApproxMiddle[j]]
        else:
            return 0

    def getClusterZeta(self, k):
        if self.cluster[k]:
            r = 0
            for i in self.cluster[k]:
                r += self.maze.distanceMetagraph[self.clusterApproxMiddle[k]][i]**2

            return np.sqrt(r / len(self.cluster[k]))
        else:
            return 1

    def getClusterCoordinate(self, i):
        x1, y1 = self.clusterMiddle[i]
        x1, y1 = round(x1), round(y1)

        return (x1, y1)

    #### ACTIONS MANAGEMENT
    def turn(self):
        t = time.clock()

        # Add player and opponent to metaGraph
        self.maze.addNodeToMetagraph(self.player.location, self.CURRENT_CHEESES_LOCATION)
        self.maze.addNodeToMetagraph(self.opponent.location, self.CURRENT_CHEESES_LOCATION + [self.player.location])

        # The opponent use a GLOUTON algorithm
        o_d, o_p = self.maze.getNearestNode(self.opponent.location, self.CURRENT_CHEESES_LOCATION)
        self.opponent.setPath([o_p])

        print("## Metagraph addition executed in " + str(time.clock() - t))

        # In case of particular reaction
        if self.player.destination:
            CHECKS = {}

            CHECKS['CHEESES_LOCATION'] = self.player.destination not in self.CURRENT_CHEESES_LOCATION
            CHECKS['CHEESES_NB'] = self.CURRENT_CHEESES_NB in [1, 2]

            if not CHECKS['CHEESES_LOCATION']:
                CHECKS['PLAYER_DESTINATION'] = self.maze.distanceMetagraph[self.opponent.location][self.player.destination] <= self.ABORT_RADIUS < self.maze.distanceMetagraph[self.player.location][self.player.destination]
                CHECKS['OPPONENT_DESTINATION'] = (self.player.destination == self.opponent.destination) and (self.maze.distanceMetagraph[self.opponent.location][self.opponent.destination] <= self.OPPONENT_ABORT_RADIUS < self.maze.distanceMetagraph[self.player.location][self.player.destination])

            CHECKS_RESULT = False
            for k in CHECKS:
                CHECKS_RESULT = CHECKS_RESULT or CHECKS[k]
        
            if CHECKS_RESULT:
                if (CHECKS['CHEESES_LOCATION'] or CHECKS['PLAYER_DESTINATION'] or CHECKS['OPPONENT_DESTINATION']) and (not CHECKS['CHEESES_NB']):
                    # On switch sur le fromage suivant si c'est rentable
                    erase = True
                    for p in self.player.path[1::]:
                        new_dest = p[-1]
                        if (new_dest in self.CURRENT_CHEESES_LOCATION) and (self.maze.distanceMetagraph[self.player.location][new_dest] < self.maze.distanceMetagraph[self.opponent.location][new_dest]):
                            self.player.setPath([self.maze.pathMetagraph[self.player.location][new_dest]] + self.player.path[2::])
                            erase = False
                            break

                    if erase:
                        self.player.setPath(None)
                else:
                    self.player.setPath(None)  # On reset le path

        # If we need calculate a path
        if (not self.player.path) or \
                (len(self.player.path) == 1 and len(self.player.path[0]) <= 1) or \
                (not self.player.destination):

            print("### No destination detected : " + repr(self.player.destination)) if not self.player.destination else ()

            # If there is only one cheese
            if self.CURRENT_CHEESES_NB == 1 and self.current_mode != 0:
                print("## ONE node mode")
                d, p = self.maze.getFastestPath(self.player.location, self.CURRENT_CHEESES_LOCATION[0])
                self.player.setPath([p])
                self.current_mode = 0
            
            # If there are 2 cheeses
            elif self.CURRENT_CHEESES_NB == 2 and self.current_mode != 1:
                print("## TWO node mode")
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

                d, p = self.maze.getFastestPath(self.player.location, goal)
                self.player.setPath([p])
                self.current_mode = 1

            # In other cases
            else:
                # Update clusters rentability
                if self.RENTABILITY_METHOD == 1:
                    self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
                    self.clusterRentability = []

                    for k in self.cluster:
                        rent = (self.getClusterFactor(k), k)

                        self.clusterRentability.append(rent)

                elif self.RENTABILITY_METHOD == 2:
                    self.factors = self.calculateFactors(self.CURRENT_CHEESES_LOCATION)
                    self.clusterRentability = []

                    A = np.zeros((len(self.cluster), len(self.cluster)))

                    # Create rentability matrix
                    for i in self.cluster:
                        A[i][i] = 1

                        for j in self.cluster:
                            if j != i:
                                d = - self.getClusterFactor(i) / self.clusterDistance[i][j]
                                A[i][j] = d

                    B = np.zeros((len(self.cluster), 1))

                    for i in range(len(B)):
                        B[i][0] = self.getClusterFactor(i)

                    R = lg.solve(A, B)
                    for k in self.cluster:
                        self.clusterRentability.append((R[k][0], k))

                elif self.RENTABILITY_METHOD == 3:
                    pass
                    # ICI : SANS FACTEUR DE COMMUNAUTE

                elif self.RENTABILITY_METHOD == 4:
                    self.clusterRentability = []
                    warning_ratio = {}
                    for k in self.cluster:
                        d_p, d_o = 0, 0
                        if self.cluster[k]:  # If the cluster is not empty
                            for n in self.cluster[k]:
                                d_p += self.maze.distanceMetagraph[self.player.location][n]
                                d_o += self.maze.distanceMetagraph[self.opponent.location][n]

                            m = len(self.cluster[k])
                            warning_ratio[k] = (2 * self.getClusterZeta(k) + (d_p / m)) / (d_o / m)
                        else:
                            warning_ratio[k] = 1 # On s'en fou car ça va etre nul apres

                    # Calcul de D
                    D, nb = 0, 0

                    for i in self.cluster:
                        for j in self.cluster:
                            if i != j:
                                D += self.getClusterDistance(i, j)
                                nb += 1

                    D = D / nb

                    print("D : " + repr(D))

                    A = np.zeros((len(self.cluster), len(self.cluster)))

                    # Create rentability matrix
                    for i in self.cluster:
                        A[i][i] = 1

                        for j in self.cluster:
                            if j != i:
                                di = - D * len(self.cluster[i]) / (self.getClusterDistance(i, j) * warning_ratio[i])
                                A[i][j] = di

                    print(A)

                    B = np.zeros((len(self.cluster), 1))

                    for i in range(len(B)):
                        B[i][0] = len(self.cluster[i]) / warning_ratio[i]

                    print(B)

                    R = lg.solve(A, B)
                    for k in self.cluster:
                        self.clusterRentability.append((R[k][0], k))

                elif self.RENTABILITY_METHOD == 5:
                    self.clusterRentability = []
                    warning_ratio = {}
                    for k in self.cluster:
                        d_p, d_o = 0, 0
                        if self.cluster[k]:  # If the cluster is not empty
                            for n in self.cluster[k]:
                                d_p += self.maze.distanceMetagraph[self.player.location][n]
                                d_o += self.maze.distanceMetagraph[self.opponent.location][n]

                            m = len(self.cluster[k])
                            warning_ratio[k] = (2 * self.getClusterZeta(k) + (d_p / m)) / (d_o / m)
                        else:
                            warning_ratio[k] = 1 # On s'en fou car ça va etre nul apres

                    #print(warning_ratio)
                    # Calcul de D
                    D, nb = 0, 0

                    for i in self.cluster:
                        for j in self.cluster:
                            if i != j:
                                D += self.getClusterDistance(i, j)
                                nb += 1

                    D = D / nb

                    community_ratio = {}

                    for i in self.cluster:
                        r = 0
                        for j in self.cluster:
                            if i != j:
                                r += len(self.cluster[j]) / (warning_ratio[j] * self.getClusterDistance(i, j))

                        r = 1 + D*r

                        community_ratio[i] = r

                    #print(community_ratio)

                    for k in self.cluster:
                        self.clusterRentability.append((len(self.cluster[k]) * community_ratio[k] / warning_ratio[k], k))

                self.clusterRentability.sort()
                print("### Rentability : " + repr(self.clusterRentability))
                
                # Choose cluster
                b_r, b_k = self.clusterRentability.pop()

                while len(self.cluster[b_k]) == 0:
                    b_r, b_k = self.clusterRentability.pop()
                
                print("## Choose cluster " + str(b_k) + " : " + repr(self.cluster[b_k]))


                # Calculate Path
                d, p = np.inf, [] # A remplacer par un glouton plus tard
                init = time.clock()

                NB_TESTS = 100
                for k in range(NB_TESTS):
                    if time.clock() - t > (self.TIME_ALLOWED * 80/100):
                        break

                    # Execute twoOPT
                    to = TwoOPT(self.maze, self.cluster[b_k] + [self.player.location], self.TIME_ALLOWED * 10/100)
                    to.process()

                    d_t, p_t = to.getResult(self.player.location)

                    if d_t < d:
                        d, p = d_t, p_t

                print("# Path of " + repr(d) + " found in " + repr(NB_TESTS) + " tests and " + repr(time.clock() - init) + " seconds")

                # Set path
                self.player.setPath(self.maze.convertMetaPathToRealPaths(p))

        # Radar
        if self.RADAR_RADIUS > 0:
            r_d, r_n = np.inf, None
            for n in self.CURRENT_CHEESES_LOCATION:
                # Check if we can have it
                if self.maze.distanceMetagraph[self.player.location][n] <= self.RADAR_RADIUS:
                    in_path = False
                    # Check if the node is not in the path
                    for li in self.player.path:
                        if n in li:
                            in_path = True

                    if not in_path:
                        # Check if the node is not for the opponent
                        if self.maze.distanceMetagraph[self.player.location][n] <= self.maze.distanceMetagraph[self.opponent.location][n]:

                            # Add n to path
                            if self.maze.distanceMetagraph[self.player.location][n] < r_d:
                                r_d, r_n = self.maze.distanceMetagraph[self.player.location][n], n

            if r_n:
                print("#### Switched destination to " + repr(r_n))
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

    def preprocessing(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
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

        # Create clusters
        nb_cluster = self.NB_CLUSTER
        alg = K_Means(self.maze, nb_cluster, self.INITIAL_CHEESES)

        # TIME : result = alg.process((timeAllowed - (time.clock() - b_t)) * (95 / 100))
        # ITERATION :
        result = alg.process(None, 100)

        ####################################### CLUSTERS GENERATION ###################################################

        # Checks clusters
        tot_cheeses = 0
        for i in range(nb_cluster):
            self.cluster[i] = result[1][i]
            self.clusterMiddle[i] = result[0][i]
            self.clusterApproxMiddle[i] = (round(result[0][i][0]), round(result[0][i][1]))

            # Calcul de l'écart type
            self.maze.addNodeToMetagraph(self.clusterApproxMiddle[i], piecesOfCheese)

            tot_cheeses += len(result[1][i])

        # Add approxs middles to metagraph
        middle_list = [self.clusterApproxMiddle[j] for j in self.cluster]
        for i in self.cluster:
            self.maze.addNodeToMetagraph(self.clusterApproxMiddle[i], middle_list)

        # Update clusters distance
        for i in self.cluster:
            self.clusterDistance[i] = {}
            for j in self.cluster:
                self.clusterDistance[i][j] = self.getClusterDistance(i, j)

        # Check the total number of cheeses
        if tot_cheeses != self.TOTAL_CHEESES:
            print("# All cheeses has not been put in a cluster !!")
            pass

        print("## Clusters : " + repr(alg.k) + " clusters have been generated with " + str(tot_cheeses) + " cheeses")
        print("# Pre-execution executed in " + repr(time.clock() - b_t) + " seconds")

    def update(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
        # If it's the first update (we are in the preprocessing)
        if (not self.player) or (not self.opponent):
            self.preprocessing(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)

        b_t = time.clock()

        # Update cluster (delete old cheeses)
        for cheese in self.CURRENT_CHEESES_LOCATION:
            if cheese not in piecesOfCheese:
                for k in self.cluster:
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
        self.TIME_ALLOWED = timeAllowed

        print("# Update executed in " + repr(time.clock() - b_t) + " seconds")

    #### MIS
    def calculateFactors(self, nodes):
        try:
            # Calculate factors
            factors = {}

            for n in nodes:
                factors[n] = float(self.maze.distanceMetagraph[self.player.location][n] / self.maze.distanceMetagraph[self.opponent.location][n])

            return factors
        except KeyError:
            print("# Factors calculated without metaGraph")

            # Calculate for player
            alg = Dijkstra(self.maze, self.player.location, None)
            alg.process()

            playerResult = alg.dist

            # Calculate for opponent
            alg = Dijkstra(self.maze, self.opponent.location, None)
            alg.process()

            opponentResult = alg.dist

            # Calculate factors
            factors = {}
            for c in nodes:
                factors[c] = float(playerResult[c] / opponentResult[c])

            return factors
