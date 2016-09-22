#!/usr/bin/env python3
# -*- coding: utf-8 -*-

TEAM_NAME = "Speedy Gonzalez"


import copy as cp
import numpy as np

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'
total_path = ""
cheeses = []
import time

def preprocessing(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed):
    t = time.clock()
    print('Position : ' + repr(playerLocation))

    maze = Maze(mazeMap, mazeWidth, mazeHeight)
    o = playerLocation
    a = Astar(maze, (0,0), (0,0))

    global total_path
    global cheeses
    cheeses = piecesOfCheese
    path = ""

    while cheeses:
        m = (np.inf, "")
        m_c = o
        for c in piecesOfCheese:
            a.setOrigin(o)
            a.setGoal(c)
            a.process()

            if a.result[0] < m[0]:
                m = a.result
                m_c = c

        piecesOfCheese.remove(m_c)
        path += m[1]
        o = m_c

    total_path = path
    print(time.clock() - t)

def turn(mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese,
         timeAllowed):
    global total_path
    if total_path:
        c= total_path[0]
        total_path = total_path[1::]
        print('[Move]:'+ c + ' - [Time Allowed] : ' + str(timeAllowed))
        return c