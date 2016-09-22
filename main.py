#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from includes import Maze
from includes import Rat
from includes import Engine

TEAM_NAME = "PLS_TEAM"

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

def update(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    # Update players
    player.location = playerLocation
    opponent.location = opponentLocation

    # Update Engine    
    engine.update(player, opponent)
    
def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed):
    
    player.process(maze, opponent, piecesOfCheese)