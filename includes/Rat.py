# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:35:42 2016

@author: Thibault/Clément
"""

class Rat:
    def __init__(self, location):
        self.location = location
        self.score = 0

        # Paths managers
        self.path = []
        self.precedentNodes = []
        self.destination = None

    def addCheese(self):
        self.score += 1

    def setLocation(self, new_location):
        if new_location != self.location:
            self.precedentNodes.append(self.location)
            self.location = new_location

            # Update path
            if (new_location == self.destination) and self.path:
                self.path = self.path[1::]
                if self.path and self.path[0][-1]:
                    self.destination = self.path[0][-1]
                    print("## Switch to destination " + repr(self.destination))

class Player(Rat):
    pass

class Opponent(Rat):
    pass