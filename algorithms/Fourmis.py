import random as rd
import numpy as np

class Fourmis:
    def __init__(self, engine, fromLocation, locationList, pheromonesTime = 100, antNumber = 1000, pheromonesMax = 1, pheromonesMin = 0.01):
        """Prend la liste des cases a visiter"""
        self.engine = engine
        self.distances = engine.maze.distanceMetagraph
        self.pheromonesTime = pheromonesTime
        self.locationList = locationList
        self.locationNumber = len(self.locationList)
        self.fromLocation = fromLocation
        self.antNumber = antNumber
        self.pheromonesDico = {fLocation : {tLocation : [1./pheromonesTime]*pheromonesTime for tLocation in [self.fromLocation]+self.locationList} for fLocation in [self.fromLocation]+self.locationList}
        self.pheromonesMax = pheromonesMax
        self.pheromonesMin = pheromonesMin

    def process(self):
        for i in range(self.antNumber):
            locationList = self.locationList.copy() #On copie la liste pour pouvoir la modifier
            distanceSum = 1
            n = len(locationList)
            currentLocation = self.fromLocation
            while n > 0:
                (case, pheromones) = self.weightedChoice(locationList, currentLocation)
                n-=1
                self.pheromonesDico[currentLocation][case][-1] += max(np.sqrt(1./distanceSum), self.pheromonesMin)
                distanceSum += self.distances[currentLocation][case]
                #On passe à la case suivante
                currentLocation = case
                self.decalerPheromones()
        return self.retournerCheminOpt()
    

    def weightedChoice(self, list, currentLocation):
        """Fait un tirage au sort sans remise en affectant les poids, retourne l'élément choisi et son poids"""
        n = len(list)
        rand = rd.random()
        nbPhero = 0
        for elt in list:
            nbPhero += self.getPheromonesPath(currentLocation, elt)
        currentPhero = 0
        for elt in list:
            eltPhero = self.getPheromonesPath(currentLocation, elt)
            if rand < (currentPhero+eltPhero)/nbPhero:
                list.remove(elt)
                return(elt, eltPhero)
            currentPhero += eltPhero  

    def getPheromonesPath(self, fromLocation, toLocation):
        res = 0
        for pheromones in self.pheromonesDico[fromLocation][toLocation]:
            res+=pheromones
        return res

    def decalerPheromones(self):
        """Retire un cycle de vie aux phéromones"""
        for fromLocation in self.locationList :
            for toLocation in self.locationList :
                n = self.pheromonesDico[fromLocation][toLocation]
                self.pheromonesDico[fromLocation][toLocation].pop(0)
                self.pheromonesDico[fromLocation][toLocation].append(self.pheromonesMin)

    def retournerCheminOpt(self):
        toVisitList = self.locationList.copy()
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
            toVisitList.pop(maxPheromonesToPathIndex)
        orderedVisitList.pop(0) #On retire le fromLocation du début
        return orderedVisitList


    def partiePositive(self, x):
        if x <= 0:
            return 0
        else:
            return x
