import random as rd
import numpy as np

class Fourmis:
    def __init__(self, maze, fromLocation, locationList, pheromonesTime = 300, antNumber = 200, pheromonesMax = 100):
        """Prend la liste des cases a visiter"""
        self.maze = maze
        self.distances = self.maze.distanceMetagraph
        self.pheromonesTime = pheromonesTime
        self.locationList = locationList
        self.locationNumber = len(self.locationList)
        self.fromLocation = fromLocation
        self.antNumber = antNumber
        self.pheromonesDico = {location : {[0]*pheromonesTime for location in self.locationList} for location in self.locationList}
        self.pheromonesMax = pheromonesMax

    def process(self):
        for i in range(self.antNumber):
            locationList = self.locationList #On copie la liste pour pouvoir la modifier
            distanceSum = 0
            n = len(locationList)
            currentLocation = self.fromLocation
            while n > 0:
                (case, pheromones) = self.weightedChoice(locationList, pheromonesDico)
                n-=1
                self.pheromonesDico[currentLocation][case][-1] += self.partiePositive(self.pheromonesMax - distanceSum)
                distanceSum += self.distances[self.currentLocation][case]
                #On passe à la case suivante
                currentLocation = case
                self.decalerPheromones()
        return self.retournerCheminOpt()
    

    def weightedChoice(self, list, weightDico):
        """Fait un tirage au sort sans remise en affectant les poids, retourne l'élément choisi et son poids"""
        n = len(list)
        weightedList = []
        for elt in list:
            for j in range(weightDico[elt]):
                weightedList.append(elt)
        choicedElement = rd.choice(weightedList)
        indexElt = list.index(choicedElement)
        list.remove(indexElt)
        choicedElementweight = weightDico[choicedElement]
        return (choicedElement, choicedElementweight)

    def getPheromonesPath(self, fromLocation, toLocation):
        res = 0
        for pheromones in pheromonesDico[fromLocation][toLocation]:
            res+=pheromones[fromLocation][toLocation]
        return res

    def decalerPheromones():
        """Retire un cycle de vie aux phéromones"""
        for fromLocation in self.locationList :
            for toLocation in self.locationList :
                n = self.pheromones[fromLocation][toLocation]
                self.pheromones[fromLocation][toLocation] = self.pheromones[fromLocation][toLocation][1:n]
                self.pheromones[fromLocation][toLocation].append(0)

    def retournerCheminOpt():
        toVisitList = self.locationList
        orderedVisitList = [self.fromLocation]
        for i in range(self.locationNumber):
            maxPheromones = np.inf
            maxPheromonesToPathIndex = None
            for j in range(len(toVisitList)):
                currentPheromones = self.getPheromonesPath(orderedVisitList[i],toVisitList[j])
                if currentPheromones < maxPheromones :
                    maxPheromones = currentPheromones
                    maxPheromonesToPathIndex = j
            orderedVisitList.append(toVisitList[maxPheromonesToPathIndex])
            toVisitList.remove(maxPheromonesToPathIndex)
        return orderedVisitList


    def partiePositive(self, x):
        if x <= 0:
            return 0
        else:
            return x
