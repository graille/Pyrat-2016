# -*- coding: utf-8 -*-
"""
Created on Thu Sep 23 15:02:00 2016

@author: Thibault/Clément

Held-Kald Algorithm
"""

import numpy as np
import itertools as it
from algorithms.Astar import *

class HeldKalp:
    def __init__(self, engine, from_location, locationList):
        """Prend la liste des cases a visiter"""
        self.engine = engine
        self.distances = engine.maze.distanceMetagraph
        self.locationList = locationList
        self.from_location = from_location

    def process(self):
        comb = self.combinaisons(self.locationList)
        comb_tab = comb[0]
        comb_tuple = comb[1]
        n = len(self.locationList)
        n_comb = len(comb_tab)
        #init
        cost = {}
        for location in self.locationList :
            cost[tuple([(location)])] = self.distances[self.from_location][location]
        
        costmin = np.inf
        costMinElement = None
        for i in range(2,n+1): #On travaille dans un nombre de points croissants
            for index in range(n_comb) :
                element = comb_tab[index]
                if len(element) == i :
                    for index3 in range(n_comb) :
                        element3 = comb_tab[index3]
                        if len(element3) == 1 :
                            for index2 in range(n_comb) :
                                element2 = comb_tab[index2]
                                if element2+element3 == element :
                                    cost2to3 = self.distances[element2[-1]][element3[0]]
                                    t_element = comb_tuple[index]
                                    t_element2 = comb_tuple[index2]
                                    if t_element not in cost or cost[t_element] > cost[t_element2] + cost2to3:
                                        cost[t_element] = cost[t_element2] + cost2to3
                                        if  len(element) == n and costmin > cost[t_element] : 
                                            costmin = cost[t_element]
                                            costMinElement = element
        return costMinElement




    def combinaisons(self, list):
        n = len(list)
        res = [[],[]]
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
                res[0].append(perm_tab)
                res[1].append(tuple(perm_tab))
        return res