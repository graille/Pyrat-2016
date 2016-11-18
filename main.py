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
from process.Utils import *

# Initialize vars
TEAM_NAME = "Paul La Souris"
engine = None

nb_turn = 0
global_time = time.clock()

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global engine
    global global_time

    t = time.clock()
    global_time = t
    
    print("Start preprocessing (" + str(timeAllowed) + ")")

    # Initialize the game
    engine = Engine(mazeMap, mazeWidth, mazeHeight)

    # Update with preprocessing argument
    engine.update(playerLocation, opponentLocation, 0, 0, piecesOfCheese, timeAllowed * 98/100)

    print("Total preprocessing executed in " + repr(time.clock() - t))
    print("")

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    try:
        global engine
        global nb_turn
        global global_time

        if nb_turn > 5:
            doSomething(nb_turn)

        t = time.clock()
        print("Begin turn " + str(nb_turn) + " at " + repr(time.clock() - global_time))

        # Update
        engine.update(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed * 98/100)
        action = engine.turn()

        nb_turn += 1
        print('[' + repr(action) + '] in ' + repr(time.clock() - t))
        print(" ")

        return action
    except Exception:
        engine.player.path = []
        engine.player.destination = None

        turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)