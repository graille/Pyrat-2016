# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:09:14 2016

<<<<<<< HEAD
@author: Clément
"""

import numpy as np

class FloydWarshall():
    def __init__(self, maze, mazeWidth, mazeHeight):
        self.maze = maze
        self.NB_CASE = mazeWidth * mazeHeight
    def process(self):
        n = self.NB_CASES
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.maze.matrixMap[i][j] > self.maze.matrixMap[i][k] + self.maze.matrixMap[k][j]:
                        self.maze.matrixMap[i][j] = self.maze.matrixMap[i][k] + self.maze.matrixMap[k][j]
                        self.maze.pathMatrix[i][j] = self.maze.pathMatrix[i][k] + self.maze.pathMatrix[k][j]