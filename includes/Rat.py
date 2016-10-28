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
        self.destination = None

        self.previousNodes = []

    def setLocation(self, new_location):
        if new_location != self.location:
            # We keep the 40 lastest nodes
            self.previousNodes.append(self.location)
            self.previousNodes = self.previousNodes[:40]

            # Update location
            self.location = new_location

        # Update path
        if self.location == self.destination and len(self.path) > 1:
            self.setPath(self.path[1::])

    def setPath(self, path, verbose = False):
        if path:
            if path[0]:
                self.path = path
                self.destination = path[0][-1]

                if verbose:
                    print("### Path updated : switch to destination " + repr(self.destination))
        else:
            self.path = []
            self.destination = None

class Player(Rat):
    pass

class Opponent(Rat):
    pass