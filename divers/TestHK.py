import copy as cp
import numpy as np
import itertools as it
import time
import matplotlib.pyplot as plt
import random as rd

class Astar:
    def __init__(self, maze, origin = None, goal = None):
        self.maze = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

        # declare self.nPredecessor
        self.nPredecessor = cp.deepcopy(self.maze.mazeMap)

        # declare self.gScore
        self.gScore = cp.deepcopy(self.maze.mazeMap)

        # declare self.fScore
        self.fScore = cp.deepcopy(self.gScore)

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def heuristic(self, n1, n2):
        return np.sqrt((n1[0] - n2[0]) ** 2 + (n1[1] - n2[1]) ** 2)

    def clear(self):
        for k in self.nPredecessor.keys():
            self.nPredecessor[k] = 0
            
        for k in self.gScore.keys():
            self.gScore[k] = np.inf
            
        for k in self.fScore.keys():
            self.nPredecessor[k] = 0

    def process(self):
        self.result = self.algorithm()

    def algorithm(self):
        self.clear()

        self.closedSet = []
        self.openSet = [self.origin]

        self.gScore[self.origin] = 0
        self.fScore[self.origin] = self.heuristic(self.origin, self.goal)

        while self.openSet:
            # Calculate the current node
            current = self.openSet[0]
            for node in self.openSet:
                if self.fScore[current] > self.fScore[node]:
                    current = node
            if current == self.goal:
                return self.reconstruct_path(current)

            self.openSet.remove(current)
            self.closedSet.append(current)

            for neighbor in self.maze.getNeighbors(current):
                if neighbor in self.closedSet:
                    continue

                tentative_gScore = self.gScore[current] + self.maze.getDistance(current, neighbor)

                if neighbor not in self.openSet:
                    self.openSet.append(neighbor)

                elif tentative_gScore >= self.gScore[neighbor]:
                    continue

                self.nPredecessor[neighbor] = current
                self.gScore[neighbor] = tentative_gScore
                self.fScore[neighbor] = self.gScore[neighbor] + self.heuristic(neighbor, self.goal)

        return False

    def reconstruct_path(self, current):
        total_path = ""
        total_distance = 0
        path = []
        while current != self.origin:
            new = self.nPredecessor[current]

            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            path.append(current)
            current = new
        path.append(current)
        return (total_distance, total_path[::-1])

    def getResult(self):
        return self.result



class HeldKalp:
    def __init__(self, maze, from_location, locationList):
        """Prend la liste des cases a visiter"""
        self.maze = maze
        self.locationList = locationList
        self.from_location = from_location

    def process(self):
        comb = self.combinaisons(self.locationList)
        n = len(self.locationList)
        #init
        cost = {}
        for location in self.locationList :
            cost[tuple([(location)])] = self.maze.distanceMetagraph[self.from_location][location]
        
        costmin = np.inf
        costMinElement = None
        for i in range(2,n+1): #On travaille dans un nombre de points croissants
            for element in comb :
                if len(element) == i :
                    t_element = tuple(element)
                    for element3 in comb :
                        if len(element3) == 1 :
                            for element2 in comb :
                                if element2+element3 == element :
                                    t_element2 = tuple(element2)
                                    cost2to3 = self.maze.distanceMetagraph[element2[-1]][element3[0]]
                                    if t_element not in cost or cost[t_element] > cost[t_element2] + cost2to3:
                                        cost[t_element] = cost[t_element2] + cost2to3
                                        print(cost[t_element], element)
        
        for element in comb :
            t_element = tuple(element)
            if len(element) == n and costmin > cost[t_element] :
                costmin = cost[t_element]
                costMinElement = element
        
        return costMinElement




    def combinaisons(self, list):
        n = len(list)
        res = []
        for i in range(1<<n):
            ecr_bin = bin(i)
            ajout0 = n+2 - len(ecr_bin)
            ecr_bin = "0"*ajout0 + str(ecr_bin[2:len(ecr_bin)])
            tab = []
            for j in range(n):
                if ecr_bin[j] == "1":
                    tab.append(list[j])	
            for perm in it.permutations(tab):
                perm_tab = [i for i in perm]
                res.append(perm_tab)
        return res

class Maze:
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.mazeMap = mazeMap
        self.mazeWidth = mazeWidth
        self.mazeHeight = mazeHeight

        self.NB_CASES = self.mazeWidth * self.mazeHeight
        self.nodes = list(self.getNodes())

        self.pathMatrix = None
        self.matrixMap = {}

        self.convertToMatrix()

        # Metagraph

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

    def calculateMetaGraph(self, from_location, nodes_list):
        """Remplit les cases du dictionnaire d'adjacence et du dictionnaire de chemins pour les cases spécifiées"""
        dij = Dijkstra(self)
        nodes_list = nodes_list.copy() # Pour ne pas modifier la liste originale
        nodes_list.append(from_location)
        for n in nodes_list:
            self.distanceMetagraph[n] = {}
            self.pathMetagraph[n] = {}

        for n1 in nodes_list:
            dij.setOrigin(n1)
            dij.setGoal(None)
            dij.process()

            for n2 in nodes_list:
                result = dij.getResult(n2)
                self.distanceMetagraph[n1][n2] = result[0]
                self.pathMetagraph[n1][n2] = result[1]

    def deleteFromMetagraph(self, node):
        del self.pathMetagraph[node]
        del self.distanceMetagraph[node]

        for n in self.pathMetagraph:
            del self.pathMetagraph[n][node]
            del self.distanceMetagraph[n][node]
            
    def reversePath(self, path):
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
        return self.matrixMap[from_location][to_location]

    def getNodes(self):
        return self.mazeMap.keys()

    def findMostRapidWay(self, origin, goal):
        al = Astar(self, origin, goal)
        al.process()

        return al.result

    def getMove(self, origin, goal):
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


class Dijkstra:
    def __init__(self, maze, origin = None, goal = None):
        self.maze = maze
        self.setOrigin(origin) if origin else ()
        self.setGoal(goal) if goal else ()

        # Initilialize pathArray
        self.pathArray = cp.deepcopy(self.maze.mazeMap)
        self.dist = cp.deepcopy(self.maze.mazeMap)

    def clear(self):
        for node in self.pathArray.keys():
            self.pathArray[node] = None

        for node in self.dist.keys():
            self.dist[node] = np.inf

    def setOrigin(self, n):
        self.origin = n

    def setGoal(self, n):
        self.goal = n

    def process(self):
        self.algorithm()

    def algorithm(self):
        self.clear()
        self.dist[self.origin] = 0

        Q = cp.copy(self.maze.nodes)

        while Q:
            n1 = self.findMin(Q)
            Q.remove(n1)

            if self.goal and n1 == self.goal:
                break

            for n2 in self.maze.getNeighbors(n1):
                self.majDistance(n1, n2)

    def findMin(self, Q):
        m = np.inf
        s = None

        for n in Q:
            if self.dist[n] < m:
                m = self.dist[n]
                s = n

        return s

    def majDistance(self, n1, n2):
        if self.dist[n2] > self.dist[n1] + self.maze.getDistance(n1, n2):
            self.dist[n2] = self.dist[n1] + self.maze.getDistance(n1, n2)
            self.pathArray[n2] = n1

    def reconstructPath(self, node):
        total_path = ""
        total_distance = 0
        current = node

        while current != self.origin:
            new = self.pathArray[current]
            total_path += self.maze.getMove(new, current)
            total_distance += self.maze.getDistance(current, new)
            current = new

        return (total_distance, total_path[::-1])

    def getResult(self, node = None):
        if (not node) and (self.goal):
            return self.reconstructPath(self.goal)
        else:
            return self.reconstructPath(node)


mazeMap = {(0, 0) : {(0, 1) : 1}, (0, 1) : {(0, 2) : 1, (1, 1) : 1, (0, 0) : 1}, (0, 2) : {(0, 3) : 1, (1, 2) : 1, (0, 1) : 1}, (0, 3) : {(1, 3) : 1, (0, 2) : 1}, (1, 0) : {(1, 1) : 1, (2, 0) : 1}, (1, 1) : {(2, 1) : 1, (1, 0) : 1, (0, 1) : 1}, (1, 2) : {(1, 3) : 1, (0, 2) : 1, (2, 2) : 1}, (1, 3) : {(0, 3) : 1, (1, 2) : 1}, (2, 0) : {(3, 0) : 1, (1, 0) : 1}, (2, 1) : {(1, 1) : 1, (2, 2) : 1}, (2, 2) : {(2, 1) : 1, (3, 2) : 1, (1, 2) : 1, (2, 3) : 1}, (2, 3) : {(2, 2) : 1}, (3, 0) : {(3, 1) : 1, (2, 0) : 1}, (3, 1) : {(3, 0) : 1, (3, 2) : 1}, (3, 2) : {(3, 1) : 1, (3, 3) : 1, (2, 2) : 1}, (3, 3) : {(3, 2) : 1}}

def trace():
	nb_fromages_max = 7
	timeTab = []*6
	for k in range(1,nb_fromages_max):
		liste = [(rd.randint(0,3), rd.randint(0,3))for i in range(k)]
		origin = (1,0)
		t1 = time.clock()
		maze = Maze(mazeMap, 4, 4)
		maze.calculateMetaGraph(origin, liste)
		hk = HeldKalp(maze, origin, liste)
		print(hk.process())
		t2 = time.clock()
		timeTab.append(np.log(t2-t1))
		print("Elapsed time : ", t2-t1)

	plt.plot(timeTab)
	plt.show()

def test(nb):
	liste = [(rd.randint(0,3), rd.randint(0,3))for i in range(nb)]
	origin = (0,0)
	maze = Maze(mazeMap, 4, 4)
	maze.calculateMetaGraph(origin, liste)
	hk = HeldKalp(maze, origin, liste)
	t1 = time.clock()
	print(hk.process())
	t2 = time.clock()
	print("Elapsed time : ", t2-t1)
	
test(5)



