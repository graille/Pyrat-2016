# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

from debug.MazeGenerator import *
from process.Enums import *

class Debug:
    def __init__(self, engine):
        self.engine = engine
        self.maze = engine.maze

        self.PATH_COLOR = ['red', 'grey', 'green', 'blue']
        self.CURRENT_PATH_COLOR = 0

    def showPath(self, *args):
        mg = self.getMG()

        if len(args) == 2:
            mg.showPath(args[0], args[1])
        elif len(args) == 1:
            mg.showPath(args[0])

        mg.show()

    def showMetaPath(self, path):
        origin = path[0] if path[0] != GameEnum.LOCATION_LABEL else self.engine.player.location

        paths = self.maze.convertMetaPathToRealPaths(path)
        mg = self.getMG()

        size = 10
        current = origin
        for path in paths:
            print("## Show path : " + repr(path))
            current = mg.showPath(current, path, size=size, color='red')
            size += 1

        mg.show()

    def getMG(self):
        mg = MazeGenerator(self.maze.mazeMap, self.maze.mazeWidth, self.maze.mazeHeight)
        mg.showNodes(self.engine.INITIAL_CHEESES)

        return mg