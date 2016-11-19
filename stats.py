#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Set the syspath
f_name = "stats.py"
a_path = str(os.path.abspath(__file__))
new_sys_entry = a_path[0:len(a_path) - len(f_name)]

print("Add " + new_sys_entry + "to sys path")
sys.path.insert(0, new_sys_entry)

from process.Engine import *
from process.Utils import *

# Initialize vars
TEAM_NAME = "Paul La Souris"
engine = None
utilities = None

nb_turn = 0
global_time = time.clock()
OUTPUT_FILE = "./out/results.csv"
ERRORS_FILE = "./out/Errors/EXPT-" + str(time.clock()) + ".txt"

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global engine
    global global_time
    global utilities

    utilities = Utils()

    t = time.clock()
    global_time = t
    
    print("Start preprocessing (" + str(timeAllowed) + ")")

    # Initialize the game
    engine = Engine(mazeMap, mazeWidth, mazeHeight)

    with open(OUTPUT_FILE, "r") as file:
        lines = file.readlines()
        elt = lines[-1].split(';')
        print(elt)

        engine.NB_CLUSTER = int(elt[1])
        utilities.method = int(elt[2])
        engine.RENTABILITY_METHOD = int(elt[3])
        engine.RADAR_RADIUS = int(elt[4])
        engine.ABORT_RADIUS = int(elt[5])
        engine.OPPONENT_ABORT_RADIUS = int(elt[6])

        print("NB_CLUSTER : " + repr(engine.NB_CLUSTER))
        print("RENTABILITY_METHOD : " + repr(engine.RENTABILITY_METHOD))

        file.close()

    # Update with preprocessing argument
    engine.update(playerLocation, opponentLocation, 0, 0, piecesOfCheese, timeAllowed * 98/100)

    print("Total preprocessing executed in " + repr(time.clock() - t))
    print("")

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    try:
        global engine
        global nb_turn
        global global_time
        global utilities
        
        nb_turn += 1
        
        utilities.makeCoffee(nb_turn, piecesOfCheese, playerScore, opponentScore)

        t = time.clock()
        print("Begin turn " + str(nb_turn) + " at " + repr(time.clock() - global_time))

        # Update
        engine.update(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed * 98/100)
        action = engine.turn()

        
        print('[' + repr(action) + '] in ' + repr(time.clock() - t))
        print(" ")

        return action
    except Exception as e:
        print("FATAL ERROR : " + repr(e.args))
        print("Restart entities")
        engine.player.path = []
        engine.player.destination = None

        turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed)
