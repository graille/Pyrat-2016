# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:42 2016

@author: Thibault/Clément
"""

from . import Maze
from . import Engine

class Rat:
    def __init__(location):
        self.location = location
        self.recolted_cheese = 0
        self.score = 0
        self.path = []
        
    def canMoveTo(self, Maze maze, dest):
        return (dest in maze.arrayGraph[self.location])
            
    def process(self, Maze maze, Rat opponent, piecesOfCheese):
        self.NEXT_MOVE = pop(self.path)
        # Return time of execution

    def addCheese(self):
        self.recolted_cheese += 1

    def         
    
class Player(Rat):
    pass

class Opponent(Rat):
    pass