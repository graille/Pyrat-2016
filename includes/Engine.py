# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""


class Engine(object):
    def __init__(self, nb_cheese):
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8
        
        self.TOTAL_CHEESE = nb_cheese 
    
    def update(self, player, opponent):
        self.updateDFMAX(player, opponent)
        
    def updateDFMAX(self, player, opponent):
        self.DF_MAX = (self.TOTAL_CHEESE - player.recolted_cheese) / (self.TOTAL_CHEESE - opponent.recolted_cheese)