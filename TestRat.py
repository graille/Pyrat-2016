#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TEAM_NAME = "Speedy Gonzalez"


import copy as cp
import numpy as np


class Astar:
    def __init__(self, maze, origin, goal):
        self.maze = maze
        self.setOrigin(origin)
        self.setGoal(goal)

    def heuristic(self, n1, n2):
        return np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def process(self):
        self.result = self.astar()

    def astar(self):
        # Initialize sets
        closedSet = []
        openSet = [self.origin]

        # declare cameFrom
        cameFrom = cp.deepcopy(self.maze.mazeMap)

        for k in cameFrom.keys():
            cameFrom[k] = 0

        # declare gScore
        gScore = cp.deepcopy(self.maze.mazeMap)

        for k in gScore.keys():
            gScore[k] = np.inf

        # declare fScore
        fScore = cp.deepcopy(gScore)

        gScore[self.origin] = 0
        fScore[self.origin] = self.heuristic(self.origin, self.goal)

        while openSet:
            # Calculate the current node
            current = openSet[0]
            for node in openSet:
                if fScore[current] > fScore[node]:
                    current = node
            if current == self.goal:
                return self.reconstruct_path(cameFrom, current)

            openSet.remove(current)
            closedSet.append(current)

            for neighbor in self.maze.getNeighbors(current):
                if neighbor in closedSet:
                    continue

                tentative_gScore = gScore[current] + self.maze.getDistance(current, neighbor)

                if neighbor not in openSet:
                    openSet.append(neighbor)

                elif tentative_gScore >= gScore[neighbor]:
                    continue

                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + self.heuristic(neighbor, self.goal)

        return False

    def reconstruct_path(self, cameFrom, current):
        total_path = ""
        total_distance = 0
        path = []
        while current != self.origin:
            new = cameFrom[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new
        path.append(current)
        return (total_distance, total_path[::-1])


class Maze(object):
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight

        self.pathMatrix = None
        self.matrixMap = None

        self.convertToMatrix()
        #self.FM = FloydWarshall(self)
        #self.FM.process()

    def location_to_id(self, location):
        """Converti les coordonnees d'une case en sa cle primaire"""
        x, y = location[0], location[1]
        id_case = x * self.mazeHeight + y
        return id_case

    def id_to_location(self, id_case):
        """Converti la cle primaire d'une case en ses coordonnees"""
        location = (id_case // self.mazeHeight, id_case % self.mazeHeight)
        return location

    def convertToMatrix(self):
        """
        Prend en argument
        Renvoie une matrice où les cases sont triées en fonction de leur id et où
        np.inf signifie qu'il n'y a pas de passage direct entre les deux cases,
        n>0 signifie qu'il y a passage en n coups et 0 que l'on reste sur la même case
        """
        self.matrixMap = np.array([[np.inf if i != j else 0 for i in range(self.NB_CASES)] for j in range(
            self.NB_CASES)])  # On crée une matrice contenant que des -1 sauf sur la diagonale
        for locationCaseAccessible1 in self.mazeMap:
            cle_case1 = self.location_to_id(locationCaseAccessible1)
            for locationCaseAccessible2 in self.mazeMap[locationCaseAccessible1]:
                cle_case2 = self.location_to_id(locationCaseAccessible2)
                self.matrixMap[cle_case1][cle_case2], self.matrixMap[cle_case2][cle_case1] = \
                self.mazeMap[locationCaseAccessible1][locationCaseAccessible2], self.mazeMap[locationCaseAccessible1][
                    locationCaseAccessible2]

    def calculateMetaGraph(self, from_location, to_location_list):
        """Remplit les cases de la matrice des distances uniquement pour les cases spécifiées"""
        from_location_ID = self.location_to_id(from_location)

        for to_location in to_location_list:
            to_location_ID = self.location_to_id(to_location)

            astar = Astar(self, from_location, to_location)

            (dist, path) = astar.process()
            self.pathMatrix[from_location_ID, to_location_ID] = path
            self.matrixMap[from_location_ID, to_location_ID] = dist

    def getDistance(self, from_location, to_location):
        from_location_ID, to_location_ID = self.location_to_id(from_location), self.location_to_id(to_location)

        return self.matrixMap[from_location_ID, to_location_ID]

    def getNodes(self):
        return self.mazeMap.keys()

    def findMostRapidWay(self, origin, goal):
        al = Astar(self, origin, goal)
        al.process()

        return al.result

    def getMove(self, origin, goal):
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

    def getNeighbors(self, position):
        return self.mazeMap[position].keys()



MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
total_path = ""
cheeses = []
import time

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    t = time.clock()
    print('Position : ' + repr(playerLocation))

    maze = Maze(mazeMap, mazeWidth, mazeHeight)
    o = playerLocation
    a = Astar(maze, (0,0), (0,0))

    global total_path
    global cheeses
    cheeses = piecesOfCheese
    path = ""

    while cheeses:
        m = (np.inf, "")
        m_c = o
        for c in piecesOfCheese:
            a.setOrigin(o)
            a.setGoal(c)
            a.process()

            if a.result[0] < m[0]:
                m = a.result
                m_c = c

        piecesOfCheese.remove(m_c)
        path += m[1]
        o = m_c

    total_path = path
    print(time.clock() - t)

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese,
         timeAllowed):
    global total_path
    if total_path:
        c= total_path[0]
        total_path = total_path[1::]
        print('[Move]:'+ c + ' - [Time Allowed] : ' + str(timeAllowed))
        return c