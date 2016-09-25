# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:42 2016

@author: Thibault/Clément
"""

class Rat:
    def __init__(self, location):
        self.location = location
        self.recolted_cheese = 0
        self.score = 0
        self.path = []

    def addCheese(self):
        self.recolted_cheese += 1
    
class Player(Rat):
    pass

class Opponent(Rat):
    pass