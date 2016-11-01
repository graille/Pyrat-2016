#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time

from LaunchersLibrary import *

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
PLAYER_1_FILENAME = "./in/Pyrat-2016/stats.py"
PLAYER_2_FILENAME = "./in/Pyrat-2016/Glouton.py"

configs = [repr(NB_CLUSTER) + ';' + repr(FACTOR_METHOD) + ';' + repr(RENTABILITY_METHOD) + ';' + repr(RADAR_RADIUS) + ';' + repr(ABORT_RADIUS) + ';' + repr(OPPONENT_ABORT_RADIUS) \
           for NB_CLUSTER in [6] \
           for FACTOR_METHOD in [1] \
           for RENTABILITY_METHOD in [1, 2, 3] \
           for RADAR_RADIUS in [2] \
           for ABORT_RADIUS in [3] \
           for OPPONENT_ABORT_RADIUS in [5]]

NB_ITERATION = 20
TOTAL_ITERATION = len(configs) * NB_ITERATION
CURRENT_ITERATION = 0

print("Nombre de tests : " + str(TOTAL_ITERATION))
print("Temps estimé : " + str(TOTAL_ITERATION * 20 / 3600) + " heures")
print("")

num_config = 0

with open(OUTPUT_FILE, "a") as f:
    f.write("Numero de configuration;Nombre de cluster;Methode facteur;Methode de rentabilité;Rayon du radar;Rayon d'abandon;Rayon d'abandon opposant;Nombre d'itération;Moyenne Total process;Moyenne par tour;Maximum total;Maximum tour;Minimum total;Minimum tour;Moyenne score joueur;Moyenne score opposant;Maximum score joueur;Maximum score opposant;Minimum score joueur;Minimum score opposant;Victoires joueur;Victoires opposant;Egalités")
    f.write('\n\r')
    f.close()
    
for c in configs:
    with open(OUTPUT_FILE, "a") as f:
        f.write(repr(num_config) + ';' + c)
        f.close()

    PLAYER_SCORES = []
    OPPONENT_SCORES = []

    PLAYER_MISSED = []
    PLAYER_PREPROCESSING_TIME = []
    PLAYER_TURN_TIME = []

    PLAYER_VICTORIES = 0
    OPPONENT_VICTORIES = 0
    EQUALITIES = 0

    for k in range(NB_ITERATION):
        print("Iteration " + str(CURRENT_ITERATION) + " : " + str(int(CURRENT_ITERATION * 100 * 100 / TOTAL_ITERATION) / 100.) + " %")
        result = startRandomGame(MAZE_WIDTH, MAZE_HEIGHT, MAZE_DENSITIES, MUD_PROBABILITY, MAZE_SYMMETRIC, NB_PIECES_OF_CHEESE, PREPROCESSING_TIME, TURN_TIME, GAME_MODE, OUTPUT_DIRECTORY, TIMEOUT, PLAYER_1_FILENAME, PLAYER_2_FILENAME)

        PLAYER_RESULTS = result['player1']
        OPPONENT_RESULTS = result['player2']

        PLAYER_SCORES.append(PLAYER_RESULTS['score'])
        OPPONENT_SCORES.append(OPPONENT_RESULTS['score'])

        PLAYER_PREPROCESSING_TIME.append(PLAYER_RESULTS['totalComputationTime'])
        PLAYER_TURN_TIME.append(PLAYER_RESULTS['meanComputationTime'])
        PLAYER_MISSED.append(PLAYER_RESULTS['nbTimingsMissed'])

        if PLAYER_RESULTS['score'] == OPPONENT_RESULTS['score']:
            EQUALITIES += 1
        elif PLAYER_RESULTS['score'] > OPPONENT_RESULTS['score']:
            PLAYER_VICTORIES += 1
        else:
            OPPONENT_VICTORIES +=1

        CURRENT_ITERATION += 1

    if not PLAYER_SCORES:
        PLAYER_SCORES.append(-1)
    if not OPPONENT_SCORES:
        OPPONENT_SCORES.append(-1)
    if not PLAYER_PREPROCESSING_TIME:
        PLAYER_PREPROCESSING_TIME.append(-1)
    if not PLAYER_TURN_TIME:
        PLAYER_TURN_TIME.append(-1)

    RESULT = repr(NB_ITERATION) + ';' \
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
             + repr(OPPONENT_VICTORIES) + ';' \
             + repr(EQUALITIES)

    num_config += 1

    with open(OUTPUT_FILE, "a") as f:
        f.write(';' + RESULT + '\n\r')
