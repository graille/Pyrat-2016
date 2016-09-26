# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 15:02:00 2016

@author: Thibault/Clément

Held-Kald Algorithm
"""

import numpy as np
import itertools as it
from Astar import *

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