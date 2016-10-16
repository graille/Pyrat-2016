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

        self.PATH_COLOR = ['red', 'grey', 'green', 'blue', 'orange', 'yellow', 'pink', 'cyan4', 'cyan3', 'azure4', 'orchid']
        self.CURRENT_PATH_COLOR = 0

    def showPath(self, *args):
        mg = self.getMG()

        if len(args) == 2:
            mg.showPath(args[0], args[1])
        elif len(args) == 1:
            mg.showPath(args[0])

        mg.show()

    def showMetaPath(self, paths = []):
        if len(paths) > 0:
            origin = paths[0]

            paths = self.maze.convertMetaPathToRealPaths(paths)
            mg = self.getMG()

            size = 10
            current = origin
            k = 0
            for path in paths:
                current2 = mg.showPath(current, path, size=size, color=self.PATH_COLOR[self.CURRENT_PATH_COLOR])
                if k%5 == 0 and k >= 4:
                    self.CURRENT_PATH_COLOR = (self.CURRENT_PATH_COLOR + 1) % len(self.PATH_COLOR)
                print("## Path " + repr(k) + " from " + repr(current) + " to " + repr(current2) + " : " + repr(path))
                k += 1
                current = current2
            mg.show()
        else:
            mg = self.getMG()
            mg.show()
    def getMG(self):
        mg = MazeGenerator(self.maze.mazeMap, self.maze.mazeWidth, self.maze.mazeHeight)
        mg.showNodes(self.engine.INITIAL_CHEESES)

        return mg