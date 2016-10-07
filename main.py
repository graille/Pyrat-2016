#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Set the syspath
f_name = "main.py"
a_path = str(os.path.abspath(__file__))
new_sys_entry = a_path[0:len(a_path) - len(f_name)]

print("Add " + new_sys_entry + "to sys path")
sys.path.insert(0, new_sys_entry)

from process.Engine import *

# Initialize vars
TEAM_NAME = "PLS"
engine = None

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global engine

    # Initialize the game
    engine = Engine(mazeMap, mazeWidth, mazeHeight)

    # Update
    engine.update(playerLocation, opponentLocation, 0, 0, piecesOfCheese, timeAllowed)
    engine.preprocessing()

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global engine

    # Update
    engine.update(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)
    action = engine.turn()

    print('[' + action + ']')
    return action