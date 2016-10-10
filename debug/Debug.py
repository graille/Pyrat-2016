# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

from debug.MazeGenerator import *

class Debug:
    def __init__(self, engine):
        self.engine = engine
        self.maze = engine.maze

        self.PATH_COLOR = ['red', 'grey', 'green', 'blue']
        self.CURRENT_PATH_COLOR = 0

    def showPath(self, origin, path):
        mg = MazeGenerator(self.maze)
        mg.generate()
        mg.showNodes(self.engine.INITIAL_CHEESES)

        mg.showPath(origin, path)
        mg.show()

    def showMetaPath(self, origin, path):
        mg = MazeGenerator(self.maze)
        mg.generate()
        mg.showNodes(self.engine.INITIAL_CHEESES)

        path = self.maze.convertMetaPathToRealPaths(path)

        mg.showPaths(origin, path)
        mg.show()

    def showMetaPaths(self, origins, paths):
        mg = MazeGenerator(self.maze)
        mg.generate()
        mg.showNodes(self.engine.INITIAL_CHEESES)

        k = 0
        for path in paths:
            origin = origins[k]
            path = self.maze.convertMetaPathToRealPaths(path)
            mg.showPaths(origin, path, self.PATH_COLOR[self.CURRENT_PATH_COLOR])
            self.CURRENT_PATH_COLOR = (self.CURRENT_PATH_COLOR + 1) % len(self.PATH_COLOR)
            k += 1

        self.CURRENT_PATH_COLOR = 0
        mg.show()