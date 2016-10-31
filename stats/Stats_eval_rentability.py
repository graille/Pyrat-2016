#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

#from stats.LaunchersLibrary import *

# Maze configuration
MAZE_WIDTH = 25
MAZE_HEIGHT = 25
MAZE_DENSITIES = 0.8
MUD_PROBABILITY = 0.05
MAZE_SYMMETRIC = True
NB_PIECES_OF_CHEESE = 41

# Time configuration
PREPROCESSING_TIME = 3
TURN_TIME = 0.1
TIMEOUT = 60

# Other useful constants
GAME_MODE = "test"
OUTPUT_DIRECTORY = "./out/previousGame/"
OUTPUT_FILE = "./out/results.csv"

# Configs
PLAYER_1_FILENAME = "./in/Pyrat-2016/stat.py"
PLAYER_2_FILENAME = "./in/Glouton.py"

configs = [repr(RENTABILITY_METHOD) \
           for RENTABILITY_METHOD in [1, 2, 3]]

NB_ITERATION = 20
TOTAL_ITERATION = len(configs) * NB_ITERATION

print("Nombre de tests : " + str(TOTAL_ITERATION))
print("Temps estimé : " + str(TOTAL_ITERATION * 20 / 3600) + " heures")
print("")

num_config = 0
for c in configs:
    with open(OUTPUT_FILE, "a") as file:
        file.write(repr(num_config) + ';' + c)

    NB_ERROR = 0

    PLAYER_SCORES = []
    OPPONENT_SCORES = []

    PLAYER_MISSED = []
    PLAYER_PREPROCESSING_TIME = []
    PLAYER_TURN_TIME = []

    PLAYER_VICTORIES = 0
    OPPONENT_VICTORIES = 0

    for k in range(NB_ITERATION):
        try:
            result = startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, MAZE_DENSITIES, MUD_PROBABILITY, MAZE_SYMMETRIC, NB_PIECES_OF_CHEESE, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_1_FILENAME, PLAYER_2_FILENAME)

            PLAYER_RESULTS = result['player1']
            OPPONENT_RESULT = result['player2']

        except Exception:
            NB_ERROR += 1
            continue

    if not PLAYER_SCORES:
        PLAYER_SCORES.append(-1)
    if not OPPONENT_SCORES:
        OPPONENT_SCORES.append(-1)
    if not PLAYER_PREPROCESSING_TIME:
        PLAYER_PREPROCESSING_TIME.append(-1)
    if not PLAYER_TURN_TIME:
        PLAYER_TURN_TIME.append(-1)

    RESULT = repr(NB_ITERATION) + ';' \
             + repr(NB_ERROR) + ';' \
             + repr(sum(PLAYER_PREPROCESSING_TIME) / len(PLAYER_PREPROCESSING_TIME)) + ';' \
             + repr((sum(PLAYER_TURN_TIME) / len(PLAYER_TURN_TIME))) + ';' \
             + repr(max(PLAYER_PREPROCESSING_TIME)) + ';' \
             + repr(max(PLAYER_TURN_TIME)) + ';' \
             + repr(min(PLAYER_PREPROCESSING_TIME)) + ';' \
             + repr(min(PLAYER_TURN_TIME)) + ';' \
             + repr((sum(PLAYER_SCORES) / len(PLAYER_SCORES))) + ';' \
             + repr((sum(OPPONENT_SCORES) / len(OPPONENT_SCORES))) + ';' \
             + repr(max(PLAYER_SCORES)) + ';' \
             + repr(max(OPPONENT_SCORES)) + ';' \
             + repr(min(PLAYER_SCORES)) + ';' \
             + repr(min(OPPONENT_SCORES)) + ';' \
             + repr(PLAYER_VICTORIES) + ';' \
             + repr(OPPONENT_VICTORIES)

    with open(OUTPUT_FILE, "r") as file:
        file.write(';' + RESULT + '\n\r')
