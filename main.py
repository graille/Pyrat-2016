#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from includes.Engine import *
import time

TEAM_NAME = "PLS RAT"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

engine = None

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    t = time.clock()
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
    return engine.turn()