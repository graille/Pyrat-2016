#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TEAM_NAME = "Speedy Gonzales"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

engine = None
maze = None
player, opponent = None, None

def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    TOTAL_CHEESE = len(piecesOfCheese)

    # Initialize objects    
    engine = Engine(TOTAL_CHEESE)
    maze = Maze(mazeMap)
    player = Player(playerLocation)
    opponent = Opponent(opponentLocation)

def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    player.location = playerLocation
    opponent.location = opponentLocation
    player.process(opponent, piecesOfCheese)

###################################################################################################################################################################################################################################
###################################################################################################################################################################################################################################