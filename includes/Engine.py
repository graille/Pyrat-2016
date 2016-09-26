# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

from includes.Maze import *
from includes.Rat import *

from algorithms.Dijkstra import *
from algorithms.Astar import *

class Engine:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        # Cache maze
        self.maze = Maze(mazeMap, mazeWidth, mazeHeight)

        # Init vars
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8

        # Cache players
        self.player = None
        self.opponent = None

        # Init algorithms
        self.algorithms = {}

        self.algorithms['dijkstra'] = Dijkstra(self.maze)
        self.algorithms['astar'] = Astar(self.maze)

        self.results = {}

    def turn(self):
        if not self.player.path:
            algorithm = self.algorithms['dijkstra']

            # Calculate for player
            algorithm.setGoal(None)
            algorithm.setOrigin(self.player.location)
            algorithm.process()
            
            r = []
            for k in self.CURRENT_CHEESES_LOCATION:
                r.append(algorithm.getResult(k))

            r.sort()
            self.player.path = (r.pop())[1]

        return self.player.path.pop()

    def preprocessing(self):
        pass

    def update(self, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
        # If it's the first update (we are in the preprocessing)
        if not self.player or not self.opponent:
            self.player = Player(playerLocation)
            self.opponent = Opponent(opponentLocation)

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
        algorithm = self.algorithms['dijkstra']

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