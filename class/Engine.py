# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:41:11 2016

@author: Thibault/Clément
"""

class Engine:
    def __init__(nb_cheese):
        self.DF_MAX = 1
        self.DF_LIMIT = 1.8
        
        self.TOTAL_CHEESE = nb_cheese 
    def updateDFMAX(Rat player, Rat opponent):
        self.DF_MAX = (self.TOTAL_CHEESE - player.TOTAL_CHEESE) / (self.TOTAL_CHEESE - opponent.TOTAL_CHEESE)