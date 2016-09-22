# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:09:14 2016

@author: Clément
@modification : Thibault
"""

import numpy as np

class FloydWarshall:
    def __init__(self, maze):
        self.maze = maze

    def process(self):
        n = self.maze.NB_CASES
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.maze.matrixMap[i][j] > self.maze.matrixMap[i][k] + self.maze.matrixMap[k][j]:
                        self.maze.matrixMap[i][j] = self.maze.matrixMap[i][k] + self.maze.matrixMap[k][j]
                        self.maze.pathMatrix[i][j] = self.maze.pathMatrix[i][k] + self.maze.pathMatrix[k][j]