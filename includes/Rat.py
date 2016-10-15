# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:42 2016

@author: Thibault/Clément
"""

class Rat:
    def __init__(self, location):
        self.location = location
        self.score = 0
        self.path = []
        self.precedentNodes = []

    def addCheese(self):
        self.score += 1

    def setLocation(self, new_location):
        if new_location != self.location:
            self.precedentNodes.append(self.location)
            self.location = new_location
    
class Player(Rat):
    pass

class Opponent(Rat):
    pass