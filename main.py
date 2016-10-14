#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time

# Set the syspath
f_name = "main.py"
a_path = str(os.path.abspath(__file__))
new_sys_entry = a_path[0:len(a_path) - len(f_name)]

print("Add " + new_sys_entry + "to sys path")
sys.path.insert(0, new_sys_entry)

from process.Engine import *

# Debug
from debug.Debug import *

# Initialize vars
TEAM_NAME = "Paul La Souris"
engine = None

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global engine

    # Initialize the game
    engine = Engine(mazeMap, mazeWidth, mazeHeight)

    # Update
    engine.update(playerLocation, opponentLocation, 0, 0, piecesOfCheese, timeAllowed, True)
    to = engine.algorithms.get('twoopt')

    to.setOrigin(GameEnum.LOCATION_LABEL)
    to.setGoals(piecesOfCheese)
    to.setImprove(False)

    to.process()

    path1 = to.getResult()[1]


    debug = Debug(engine)
    debug.showMetaPath(path1)


def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    global engine

    # Update
    engine.update(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)
    action = engine.turn()

    print('[' + action + ']')
    return action

if __name__ == "__main__":
    mazeMap = {(7, 3): {(8, 3): 1, (7, 2): 1}, (6, 9): {(5, 9): 9, (6, 8): 1}, (11, 11): {(11, 12): 1, (11, 10): 1, (10, 11): 1}, (7, 12): {(7, 13): 1, (8, 12): 1}, (0, 7): {(0, 8): 1, (1, 7): 1}, (1, 6): {(0, 6): 1, (2, 6): 1, (1, 5): 1}, (0, 10): {(0, 9): 1, (1, 10): 1}, (3, 7): {(3, 8): 1, (2, 7): 1, (3, 6): 9}, (2, 5): {(1, 5): 1, (2, 4): 1, (3, 5): 1}, (1, 11): {(1, 10): 1, (0, 11): 1, (2, 11): 10, (1, 12): 1}, (8, 5): {(9, 5): 1, (8, 4): 1}, (5, 8): {(5, 9): 9, (6, 8): 1, (4, 8): 9}, (4, 0): {(3, 0): 10, (4, 1): 1}, (10, 8): {(11, 8): 1, (9, 8): 1, (10, 9): 1}, (9, 0): {(10, 0): 1, (9, 1): 1}, (6, 7): {(5, 7): 1, (7, 7): 1, (6, 8): 1}, (5, 5): {(5, 6): 1, (6, 5): 9}, (11, 5): {(10, 5): 1, (11, 4): 1}, (10, 7): {(11, 7): 1}, (7, 6): {(8, 6): 1, (7, 5): 1, (6, 6): 9}, (6, 10): {(6, 11): 4, (5, 10): 1}, (0, 4): {(0, 3): 1, (0, 5): 1, (1, 4): 1}, (1, 1): {(1, 2): 1, (0, 1): 5, (1, 0): 1, (2, 1): 1}, (4, 10): {(5, 10): 1, (3, 10): 1, (4, 9): 1}, (3, 2): {(4, 2): 1, (3, 1): 1, (3, 3): 1}, (2, 6): {(2, 7): 9, (1, 6): 1, (3, 6): 1}, (9, 14): {(9, 13): 1, (10, 14): 1}, (8, 2): {(8, 1): 1, (9, 2): 10, (7, 2): 1}, (5, 11): {(6, 11): 1, (5, 10): 7}, (4, 5): {(3, 5): 1}, (10, 13): {(9, 13): 1, (10, 14): 1, (10, 12): 1, (11, 13): 5}, (9, 3): {(9, 2): 7, (8, 3): 1, (10, 3): 10, (9, 4): 5}, (6, 0): {(6, 1): 1, (7, 0): 1}, (11, 0): {(10, 0): 1, (11, 1): 1}, (7, 5): {(7, 4): 1, (7, 6): 1, (6, 5): 1}, (0, 1): {(0, 0): 1, (1, 1): 5}, (3, 12): {(4, 12): 1, (2, 12): 10, (3, 13): 1}, (1, 12): {(1, 11): 1, (0, 12): 1}, (8, 12): {(7, 12): 1, (8, 11): 1, (8, 13): 1}, (3, 1): {(3, 0): 9, (3, 2): 1, (4, 1): 1}, (2, 11): {(3, 11): 1, (1, 11): 10, (2, 12): 7, (2, 10): 5}, (9, 9): {(9, 10): 1, (8, 9): 1, (10, 9): 1}, (5, 14): {(4, 14): 1, (5, 13): 1}, (10, 14): {(10, 13): 1, (9, 14): 1}, (6, 13): {(6, 12): 1, (5, 13): 1, (6, 14): 1}, (7, 8): {(8, 8): 1, (7, 7): 6, (6, 8): 1}, (0, 14): {(1, 14): 1, (0, 13): 1}, (3, 11): {(2, 11): 1, (4, 11): 1}, (2, 1): {(2, 0): 1, (1, 1): 1, (2, 2): 1}, (8, 9): {(8, 8): 6, (9, 9): 1, (7, 9): 1}, (4, 12): {(4, 13): 8, (5, 12): 10, (3, 12): 1, (4, 11): 1}, (2, 12): {(2, 11): 7, (2, 13): 1, (3, 12): 10}, (9, 4): {(9, 3): 5}, (5, 1): {(6, 1): 1, (5, 2): 1, (5, 0): 1}, (10, 3): {(11, 3): 1, (9, 3): 10, (10, 4): 1, (10, 2): 1}, (7, 2): {(7, 3): 1, (6, 2): 10, (8, 2): 1, (7, 1): 8}, (6, 14): {(6, 13): 1}, (11, 10): {(11, 9): 1, (11, 11): 1, (10, 10): 1}, (1, 5): {(2, 5): 1, (1, 6): 1, (1, 4): 1}, (0, 11): {(1, 11): 1}, (3, 6): {(3, 7): 9, (2, 6): 1, (4, 6): 1, (3, 5): 6}, (2, 2): {(2, 3): 1, (2, 1): 1}, (1, 10): {(1, 11): 1, (0, 10): 1}, (8, 6): {(7, 6): 1, (9, 6): 1, (8, 7): 1}, (4, 1): {(4, 2): 1, (3, 1): 1, (4, 0): 1}, (10, 9): {(10, 8): 1, (9, 9): 1, (10, 10): 1}, (9, 7): {(9, 8): 9, (8, 7): 1}, (6, 4): {(7, 4): 1, (6, 3): 7, (5, 4): 1, (6, 5): 1}, (5, 4): {(6, 4): 1, (5, 3): 4}, (11, 4): {(10, 4): 1, (11, 5): 1}, (10, 4): {(11, 4): 1, (10, 3): 1}, (7, 1): {(8, 1): 1, (6, 1): 7, (7, 0): 5, (7, 2): 8}, (6, 11): {(7, 11): 1, (6, 10): 4, (5, 11): 1}, (11, 9): {(11, 8): 1, (11, 10): 1}, (0, 5): {(0, 6): 1, (0, 4): 1}, (1, 0): {(2, 0): 1, (1, 1): 1}, (0, 8): {(1, 8): 4, (0, 7): 1}, (4, 11): {(4, 12): 1, (3, 11): 1}, (3, 5): {(4, 5): 1, (2, 5): 1, (3, 6): 6}, (2, 7): {(3, 7): 1, (2, 6): 9}, (9, 13): {(10, 13): 1, (9, 14): 1, (9, 12): 1}, (8, 3): {(7, 3): 1, (9, 3): 1}, (5, 10): {(5, 9): 1, (4, 10): 1, (6, 10): 1, (5, 11): 7}, (4, 6): {(5, 6): 1, (4, 7): 6, (3, 6): 1}, (10, 10): {(9, 10): 1, (11, 10): 1, (10, 11): 1, (10, 9): 1}, (9, 2): {(9, 3): 7, (8, 2): 10, (9, 1): 1}, (6, 1): {(5, 1): 1, (6, 2): 1, (6, 0): 1, (7, 1): 7}, (5, 7): {(5, 6): 1, (4, 7): 1, (6, 7): 1}, (11, 3): {(10, 3): 1}, (7, 4): {(6, 4): 1, (7, 5): 1, (8, 4): 1}, (0, 2): {(1, 2): 1, (0, 3): 1}, (1, 3): {(0, 3): 1, (2, 3): 1, (1, 4): 1}, (8, 13): {(8, 14): 9, (7, 13): 1, (8, 12): 1}, (4, 8): {(3, 8): 1, (4, 9): 1, (5, 8): 9}, (3, 0): {(3, 1): 9, (4, 0): 10}, (2, 8): {(3, 8): 1, (1, 8): 1, (2, 9): 1}, (9, 8): {(10, 8): 1, (8, 8): 1, (9, 7): 9}, (8, 0): {(8, 1): 1, (7, 0): 1}, (5, 13): {(4, 13): 7, (5, 14): 1, (5, 12): 1, (6, 13): 1}, (6, 2): {(6, 1): 1, (7, 2): 10}, (11, 14): {(11, 13): 1}, (7, 11): {(6, 11): 1, (8, 11): 1, (7, 10): 1}, (3, 10): {(4, 10): 1, (3, 9): 1}, (1, 14): {(0, 14): 1, (2, 14): 1}, (8, 10): {(9, 10): 1, (8, 11): 1, (7, 10): 1}, (4, 13): {(4, 12): 8, (5, 13): 7, (4, 14): 5, (3, 13): 1}, (2, 13): {(1, 13): 1, (2, 14): 1, (2, 12): 1, (3, 13): 1}, (9, 11): {(10, 11): 1, (9, 12): 1}, (5, 0): {(5, 1): 1}, (10, 0): {(11, 0): 1, (9, 0): 1}, (11, 13): {(10, 13): 5, (11, 14): 1}, (7, 14): {(8, 14): 10, (7, 13): 1}, (1, 4): {(1, 5): 1, (1, 3): 1, (2, 4): 1, (0, 4): 1}, (0, 12): {(1, 12): 1}, (3, 9): {(3, 10): 1, (2, 9): 1}, (2, 3): {(1, 3): 1, (2, 2): 1}, (1, 9): {(0, 9): 1, (2, 9): 1}, (8, 7): {(8, 6): 1, (8, 8): 9, (9, 7): 1}, (4, 2): {(3, 2): 1, (4, 1): 1}, (2, 14): {(2, 13): 1, (1, 14): 1}, (9, 6): {(9, 5): 1, (10, 6): 1, (8, 6): 1}, (6, 5): {(6, 4): 1, (7, 5): 1, (5, 5): 9, (6, 6): 9}, (5, 3): {(6, 3): 1, (5, 4): 4, (4, 3): 1}, (11, 7): {(10, 7): 1, (11, 6): 1}, (10, 5): {(9, 5): 1, (11, 5): 1}, (7, 0): {(8, 0): 1, (6, 0): 1, (7, 1): 5}, (6, 8): {(6, 7): 1, (6, 9): 1, (7, 8): 1, (5, 8): 1}, (11, 8): {(10, 8): 1, (11, 9): 1}, (7, 13): {(7, 12): 1, (7, 14): 1, (8, 13): 1}, (0, 6): {(0, 5): 1, (1, 6): 1}, (1, 7): {(0, 7): 1}, (0, 9): {(1, 9): 1, (0, 10): 1}, (3, 4): {(4, 4): 1, (2, 4): 1, (3, 3): 1}, (2, 4): {(2, 5): 1, (3, 4): 1, (1, 4): 1}, (9, 12): {(9, 13): 1, (9, 11): 1}, (8, 4): {(7, 4): 1, (8, 5): 1}, (5, 9): {(5, 10): 1, (6, 9): 9, (4, 9): 1, (5, 8): 9}, (4, 7): {(5, 7): 1, (4, 6): 6}, (10, 11): {(9, 11): 1, (11, 11): 1, (10, 10): 1}, (9, 1): {(9, 2): 1, (8, 1): 1, (9, 0): 1, (10, 1): 1}, (6, 6): {(5, 6): 1, (7, 6): 9, (6, 5): 9}, (5, 6): {(5, 5): 1, (5, 7): 1, (4, 6): 1, (6, 6): 1}, (11, 2): {(10, 2): 1}, (10, 6): {(9, 6): 1, (11, 6): 4}, (7, 7): {(6, 7): 1, (7, 8): 6}, (0, 3): {(1, 3): 1, (0, 2): 1, (0, 4): 1}, (3, 14): {(4, 14): 1, (3, 13): 1}, (1, 2): {(1, 1): 1, (0, 2): 1}, (8, 14): {(7, 14): 10, (8, 13): 9}, (4, 9): {(5, 9): 1, (4, 10): 1, (4, 8): 1}, (3, 3): {(3, 2): 1, (3, 4): 1, (4, 3): 1}, (2, 9): {(2, 8): 1, (3, 9): 1, (1, 9): 1}, (8, 1): {(9, 1): 1, (8, 0): 1, (8, 2): 1, (7, 1): 1}, (5, 12): {(4, 12): 10, (5, 13): 1}, (4, 4): {(3, 4): 1, (4, 3): 1}, (10, 12): {(10, 13): 1, (11, 12): 1}, (6, 3): {(6, 4): 7, (5, 3): 1}, (11, 1): {(11, 0): 1}, (7, 10): {(7, 11): 1, (8, 10): 1}, (0, 0): {(0, 1): 1}, (3, 13): {(4, 13): 1, (2, 13): 1, (3, 12): 1, (3, 14): 1}, (1, 13): {(2, 13): 1}, (8, 11): {(7, 11): 1, (8, 10): 1, (8, 12): 1}, (4, 14): {(4, 13): 5, (5, 14): 1, (3, 14): 1}, (2, 10): {(2, 11): 5}, (9, 10): {(10, 10): 1, (9, 9): 1, (8, 10): 1}, (10, 1): {(9, 1): 1}, (6, 12): {(6, 13): 1}, (11, 12): {(11, 11): 1, (10, 12): 1}, (7, 9): {(8, 9): 1}, (0, 13): {(0, 14): 1}, (3, 8): {(3, 7): 1, (2, 8): 1, (4, 8): 1}, (2, 0): {(1, 0): 1, (2, 1): 1}, (1, 8): {(2, 8): 1, (0, 8): 4}, (8, 8): {(8, 9): 6, (9, 8): 1, (7, 8): 1, (8, 7): 9}, (4, 3): {(4, 4): 1, (3, 3): 1, (5, 3): 1}, (9, 5): {(8, 5): 1, (10, 5): 1, (9, 6): 1}, (5, 2): {(5, 1): 1}, (11, 6): {(11, 7): 1, (10, 6): 4}, (10, 2): {(11, 2): 1, (10, 3): 1}}
    w,h = 15, 12

    preprocessing(mazeMap, w, h, (11,0), (0,14), [(4,3), (5,8), (9,7),(3,8), (8,4), (11, 12), (10,11), (9,13), (11,1)], 3)