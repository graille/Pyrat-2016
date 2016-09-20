# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:55 2016

@author: Thibault/Clément
"""

from numpy import *
from . import Rat

class Graph(object):
    pass

class Maze(Graph):
    def __init__(self, mazeMap):
        self.arrayMap = mazeMap
        self.matrixMap = self.convertToMatrix(mazeMap)
        self.nodes = self.getNodes(mazeMap)
        
    def convertToMatrix(self, mazeMap):
        pass
    
    def calculateMetaGraph(self, from_position, point_list):
        pass
    
    def getNodes(self, mazeMap):
        r = []
        for key in mazeMap:
            r.append(key)
        return r
    
    def findMostRapidWay(from_pos, to_pos)
        pass
    
    def getNeighbors(self, position):
        return self.arrayMap[position]
        
    def getCost(self, n1, n2):
        return self.matrixMap[n1, n2]