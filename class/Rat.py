# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:42 2016

@author: Thibault/Clément
"""

class Rat:
    def __init__(location):
        self.location = location
        self.recolted_cheese = 0
        self.path = []
        
    def canMove(self, Graph mazeMap, dest):
        if dest in mazeMap.arrayGraph[self.location]:
            return True
        else:
            return False
            
    def process(self, timeout):
        self.NEXT_MOVE = pop(self.path)
        # Return time of execution

class Player(Rat):
    pass

class Opponent(Rat):
    pass

