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

# Initialize vars
TEAM_NAME = "Paul La Souris"
engine = None

nb_turn = 0
global_time = time.clock()
OUTPUT_FILE = "./out/results.csv"
ERRORS_FILE = "./out/Errors/EXPT-" + str(time.clock()) + ".txt"

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    global engine
    global global_time

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
        engine.FACTOR_METHOD = int(elt[2])
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
        
        t = time.clock()
        print("Begin turn " + str(nb_turn) + " at " + repr(time.clock() - global_time))

        # Update
        engine.update(playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed * 98/100)
        action = engine.turn()

        nb_turn += 1
        print('[' + repr(action) + '] in ' + repr(time.clock() - t))
        print(" ")

        return action
    except Exception as e:    
        with open(ERRORS_FILE, "a") as file:
            file.write(repr((engine.NB_CLUSTER,engine.FACTOR_METHOD, engine.RENTABILITY_METHOD, engine.RADAR_RADIUS, engine.ABORT_RADIUS, engine.OPPONENT_ABORT_RADIUS)))
            file.write('\n\r')
            file.write(repr(mazeMap))
            file.write('\n\r')
            file.write("Fromages initiaux : " + repr(engine.INITIAL_CHEESES))
            file.write('\n\r')
            file.write("Fromages actuels : " + repr(piecesOfCheese))
            file.write('\n\r')
            
            file.write("Clusters : " + repr(engine.cluster))
            file.write('\n\r')
            file.write("Player path : " + repr(engine.player.path))
            file.write('\n\r')
            file.write("Player previousNodes : " + repr(engine.player.previousNodes))
            file.write('\n\r')
            file.write("Player destination : " + repr(engine.player.destination))
            file.write('\n\r')
            file.write("Player location : " + repr(engine.player.location)) 
            
            file.write('\n\r')
            file.write("Opponent path : " + repr(engine.opponent.path))
            file.write('\n\r')
            file.write("Opponent previousNodes : " + repr(engine.opponent.previousNodes))
            file.write('\n\r')
            file.write("Opponent destination : " + repr(engine.opponent.destination))
            file.write('\n\r')
            file.write("Opponent location : " + repr(engine.opponent.location))
            
            file.write('\n\r')
            file.write('\n\r')

            file.write("I/O error({0}): {1} " + repr(e.args))
            
            file.close()
        exit()
        

