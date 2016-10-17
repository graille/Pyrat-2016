import os
import sys
import time
from debug.Debug import *
from process.Engine import *
from algorithms.Fourmis import *
from algorithms.TwoOPT import *
from algorithms.Dijkstra import *

import matplotlib.pyplot as plt

import random as rd
import numpy as np

mazeMap = {(7, 3): {(6, 3): 5, (8, 3): 1}, (6, 9): {(6, 8): 1, (7, 9): 1}, (17, 11): {(18, 11): 1, (17, 12): 1}, (19, 19): {(19, 18): 1, (18, 19): 1}, (16, 6): {(17, 6): 1, (16, 7): 1}, (7, 12): {(7, 11): 1, (7, 13): 1, (8, 12): 1}, (24, 5): {(23, 5): 4}, (20, 20): {(20, 19): 1}, (19, 4): {(20, 4): 1, (19, 3): 1}, (18, 4): {(18, 5): 1, (18, 3): 2}, (17, 20): {(16, 20): 9}, (22, 19): {(23, 19): 5, (21, 19): 1}, (21, 9): {(22, 9): 1, (21, 10): 1, (21, 8): 1}, (20, 7): {(21, 7): 1, (20, 6): 1}, (18, 19): {(19, 19): 1, (18, 20): 1, (18, 18): 1}, (22, 6): {(21, 6): 1}, (21, 6): {(20, 6): 1, (22, 6): 1}, (8, 5): {(8, 4): 1, (8, 6): 1, (7, 5): 1, (9, 5): 1}, (23, 7): {(23, 6): 1, (22, 7): 1, (24, 7): 1}, (10, 8): {(10, 7): 1, (11, 8): 10, (9, 8): 1}, (9, 0): {(10, 0): 6}, (8, 24): {(9, 24): 1, (7, 24): 1}, (11, 5): {(10, 5): 1, (11, 4): 1, (11, 6): 1}, (10, 7): {(10, 8): 1, (9, 7): 1}, (9, 21): {(8, 21): 10, (9, 22): 9, (9, 20): 1}, (14, 18): {(14, 19): 1, (15, 18): 1}, (12, 6): {(13, 6): 1, (12, 7): 8}, (11, 22): {(11, 23): 1, (10, 22): 1, (12, 22): 1, (11, 21): 1}, (10, 18): {(11, 18): 1, (10, 17): 1}, (0, 17): {(0, 16): 1, (0, 18): 9, (1, 17): 1}, (15, 11): {(15, 12): 1, (14, 11): 1}, (14, 1): {(13, 1): 1, (14, 2): 1}, (13, 7): {(13, 6): 1, (12, 7): 1, (13, 8): 1}, (12, 17): {(12, 18): 8, (11, 17): 1, (12, 16): 1}, (0, 4): {(0, 5): 1, (1, 4): 1}, (15, 4): {(14, 4): 1, (15, 5): 1, (15, 3): 1, (16, 4): 1}, (13, 20): {(13, 21): 1, (13, 19): 1}, (1, 1): {(0, 1): 1, (2, 1): 1}, (24, 18): {(24, 17): 1, (24, 19): 1}, (4, 10): {(4, 9): 1, (3, 10): 1, (5, 10): 1, (4, 11): 10}, (3, 2): {(4, 2): 1, (3, 1): 1, (3, 3): 1}, (2, 6): {(2, 7): 5, (1, 6): 1, (3, 6): 1}, (5, 11): {(6, 11): 1, (4, 11): 1}, (4, 5): {(4, 4): 1, (3, 5): 1}, (3, 23): {(3, 24): 1, (3, 22): 4}, (6, 0): {(5, 0): 1}, (5, 24): {(5, 23): 1}, (4, 16): {(3, 16): 1, (4, 15): 1, (5, 16): 1}, (19, 24): {(19, 23): 1, (20, 24): 1, (18, 24): 1}, (7, 5): {(7, 6): 1, (8, 5): 1}, (6, 23): {(7, 23): 1, (6, 22): 1}, (5, 21): {(5, 20): 1}, (20, 19): {(20, 20): 1, (21, 19): 1}, (19, 13): {(20, 13): 1, (18, 13): 1}, (16, 5): {(17, 5): 1}, (7, 22): {(8, 22): 1, (7, 21): 1, (7, 23): 1, (6, 22): 1}, (24, 4): {(24, 3): 6}, (17, 7): {(17, 8): 1, (16, 7): 1}, (20, 14): {(21, 14): 1, (20, 13): 10, (20, 15): 1, (19, 14): 1}, (18, 10): {(19, 10): 1, (18, 11): 1, (18, 9): 1}, (17, 18): {(17, 19): 1, (17, 17): 1}, (23, 19): {(23, 20): 1, (22, 19): 5, (24, 19): 1, (23, 18): 1}, (21, 15): {(21, 14): 1, (22, 15): 1, (21, 16): 10}, (16, 8): {(16, 9): 1, (16, 7): 1}, (8, 12): {(7, 12): 1, (8, 11): 1, (8, 13): 1, (9, 12): 1}, (22, 12): {(22, 11): 1, (21, 12): 1, (22, 13): 1}, (9, 9): {(9, 10): 1, (9, 8): 1, (10, 9): 5}, (23, 9): {(22, 9): 1, (23, 8): 4}, (10, 14): {(9, 14): 1, (11, 14): 1}, (8, 18): {(8, 17): 1, (7, 18): 1}, (14, 21): {(14, 20): 1, (15, 21): 1, (13, 21): 1}, (11, 15): {(12, 15): 1}, (9, 19): {(9, 18): 1, (10, 19): 1, (9, 20): 1}, (15, 16): {(15, 15): 1, (14, 16): 1, (15, 17): 1}, (14, 8): {(14, 9): 3, (14, 7): 1}, (13, 0): {(14, 0): 1}, (12, 8): {(11, 8): 1, (12, 7): 1, (12, 9): 1}, (11, 16): {(11, 17): 1}, (1, 21): {(2, 21): 1, (0, 21): 1, (1, 20): 1}, (16, 0): {(17, 0): 1, (15, 0): 1}, (15, 13): {(15, 12): 1}, (13, 13): {(12, 13): 1}, (2, 18): {(3, 18): 1}, (0, 14): {(1, 14): 1, (0, 15): 1}, (3, 11): {(3, 12): 1}, (2, 1): {(2, 0): 1, (1, 1): 1, (2, 2): 1}, (1, 15): {(2, 15): 1, (1, 16): 4}, (24, 21): {(24, 22): 1, (23, 21): 1}, (4, 12): {(4, 13): 1, (5, 12): 1, (4, 11): 5}, (2, 12): {(3, 12): 1, (2, 13): 1, (2, 11): 1}, (5, 1): {(6, 1): 10, (5, 0): 1}, (3, 17): {(4, 17): 1, (2, 17): 1}, (7, 2): {(6, 2): 5, (8, 2): 1, (7, 1): 1}, (6, 14): {(5, 14): 1, (6, 15): 1, (6, 13): 1}, (19, 18): {(20, 18): 1, (19, 19): 1}, (17, 6): {(16, 6): 1, (18, 6): 1, (17, 5): 1}, (7, 15): {(8, 15): 1}, (20, 21): {(19, 21): 1, (20, 22): 1, (21, 21): 1}, (19, 7): {(18, 7): 10}, (18, 5): {(18, 6): 1, (18, 4): 1, (19, 5): 1}, (16, 4): {(15, 4): 1}, (7, 24): {(8, 24): 1, (7, 23): 7, (6, 24): 5}, (22, 16): {(22, 15): 1}, (21, 8): {(21, 9): 1, (22, 8): 1, (20, 8): 1}, (20, 0): {(20, 1): 1, (21, 0): 1}, (24, 17): {(24, 18): 1, (23, 17): 1}, (18, 16): {(18, 15): 1}, (17, 24): {(17, 23): 1}, (22, 18): {(22, 17): 5, (21, 18): 1, (23, 18): 1}, (22, 7): {(21, 7): 1, (22, 8): 1, (23, 7): 1}, (21, 5): {(20, 5): 1, (21, 4): 1, (22, 5): 1}, (8, 6): {(9, 6): 1, (8, 5): 1, (8, 7): 1}, (23, 6): {(23, 7): 1}, (22, 10): {(22, 11): 1, (22, 9): 1, (21, 10): 1, (23, 10): 1}, (10, 9): {(11, 9): 1, (9, 9): 5, (10, 10): 1}, (9, 7): {(10, 7): 1, (9, 8): 1, (9, 6): 1}, (21, 3): {(21, 2): 1}, (11, 4): {(11, 3): 1, (11, 5): 1}, (10, 4): {(10, 5): 1, (10, 3): 1}, (9, 20): {(9, 21): 1, (9, 19): 1, (10, 20): 1, (8, 20): 1}, (14, 19): {(14, 20): 1, (14, 18): 1, (13, 19): 1}, (12, 7): {(13, 7): 1, (12, 6): 8, (12, 8): 1}, (11, 9): {(11, 10): 1, (10, 9): 1}, (10, 19): {(9, 19): 1, (11, 19): 1}, (0, 18): {(0, 17): 9}, (15, 10): {(14, 10): 1, (16, 10): 1, (15, 9): 1}, (14, 6): {(13, 6): 1, (14, 7): 1}, (13, 6): {(13, 7): 1, (12, 6): 1, (14, 6): 1}, (12, 18): {(11, 18): 1, (12, 17): 8}, (1, 19): {(0, 19): 4, (2, 19): 1, (1, 20): 1}, (0, 5): {(0, 6): 1, (1, 5): 1, (0, 4): 1}, (15, 7): {(14, 7): 1, (15, 6): 1, (15, 8): 1, (16, 7): 1}, (13, 19): {(14, 19): 1, (13, 20): 1, (13, 18): 1}, (24, 20): {(23, 20): 1, (24, 19): 1}, (2, 24): {(2, 23): 1}, (1, 0): {(0, 0): 1}, (0, 8): {(0, 9): 1, (1, 8): 1}, (4, 11): {(4, 10): 10, (4, 12): 5, (5, 11): 1}, (3, 5): {(4, 5): 1, (2, 5): 1, (3, 4): 1, (3, 6): 1}, (2, 7): {(3, 7): 1, (2, 6): 5, (1, 7): 1}, (16, 13): {(17, 13): 1, (16, 14): 1, (16, 12): 1}, (5, 10): {(4, 10): 1}, (4, 6): {(5, 6): 1, (4, 7): 1}, (3, 22): {(3, 23): 4, (2, 22): 1, (4, 22): 1, (3, 21): 1}, (6, 1): {(5, 1): 10}, (5, 7): {(6, 7): 1, (5, 8): 1}, (4, 17): {(4, 18): 1, (3, 17): 1}, (24, 1): {(24, 0): 7, (23, 1): 1}, (7, 4): {(8, 4): 9}, (6, 20): {(6, 19): 1, (6, 21): 2}, (5, 20): {(4, 20): 1, (5, 21): 1}, (19, 12): {(20, 12): 1, (18, 12): 1}, (17, 12): {(17, 13): 1, (17, 11): 1, (16, 12): 1}, (7, 17): {(8, 17): 1, (7, 16): 1}, (21, 17): {(22, 17): 1, (20, 17): 1, (21, 16): 1}, (20, 15): {(19, 15): 1, (20, 14): 1, (20, 16): 1}, (19, 1): {(19, 0): 1, (19, 2): 1, (20, 1): 5}, (18, 11): {(17, 11): 1, (19, 11): 1, (18, 10): 1}, (16, 3): {(15, 3): 10, (17, 3): 1}, (23, 18): {(23, 19): 1, (22, 18): 1, (23, 17): 1}, (24, 2): {(24, 3): 1, (23, 2): 1}, (21, 14): {(21, 15): 1, (20, 14): 1, (22, 14): 1}, (18, 22): {(17, 22): 5, (19, 22): 1}, (8, 13): {(8, 14): 1, (8, 12): 1}, (22, 13): {(22, 12): 1, (23, 13): 1, (22, 14): 1}, (9, 8): {(10, 8): 1, (9, 9): 1, (9, 7): 1}, (8, 0): {(8, 1): 1}, (23, 8): {(24, 8): 1, (22, 8): 1, (23, 9): 4}, (10, 15): {(10, 16): 3, (9, 15): 1}, (8, 19): {(7, 19): 1}, (11, 14): {(10, 14): 1, (11, 13): 1}, (9, 18): {(9, 19): 1, (9, 17): 1}, (15, 19): {(16, 19): 1}, (14, 9): {(14, 8): 3, (15, 9): 1}, (24, 12): {(24, 13): 1}, (12, 9): {(13, 9): 1, (12, 8): 1}, (11, 19): {(11, 20): 1, (10, 19): 1}, (1, 20): {(1, 21): 1, (1, 19): 1, (2, 20): 1}, (15, 12): {(14, 12): 2, (15, 11): 1, (15, 13): 1, (16, 12): 1}, (13, 12): {(12, 12): 1}, (12, 20): {(11, 20): 1, (12, 19): 1}, (2, 19): {(1, 19): 1, (2, 20): 1, (3, 19): 1}, (0, 15): {(0, 14): 1, (0, 16): 1}, (16, 22): {(17, 22): 1, (15, 22): 1, (16, 21): 1, (16, 23): 1}, (3, 10): {(4, 10): 1, (3, 9): 1, (2, 10): 1}, (1, 14): {(1, 13): 4, (2, 14): 1, (0, 14): 1}, (4, 13): {(4, 12): 1, (3, 13): 1}, (2, 13): {(1, 13): 1, (2, 14): 1, (2, 12): 1, (3, 13): 1}, (5, 0): {(5, 1): 1, (6, 0): 1, (4, 0): 1}, (4, 24): {(3, 24): 1, (4, 23): 1}, (3, 16): {(3, 15): 1, (4, 16): 1, (2, 16): 1}, (6, 15): {(5, 15): 1, (6, 16): 1, (6, 14): 1}, (16, 9): {(16, 8): 1, (17, 9): 1, (15, 9): 1}, (19, 21): {(20, 21): 1, (18, 21): 1, (19, 22): 1}, (16, 10): {(17, 10): 1, (16, 11): 1, (15, 10): 1}, (7, 14): {(8, 14): 1}, (6, 18): {(6, 19): 1, (6, 17): 1, (5, 18): 1, (7, 18): 1}, (20, 22): {(20, 21): 1, (21, 22): 1, (20, 23): 1, (19, 22): 1}, (19, 6): {(18, 6): 1, (20, 6): 1, (19, 5): 1}, (18, 2): {(17, 2): 1, (19, 2): 1, (18, 3): 1, (18, 1): 1}, (17, 10): {(16, 10): 1}, (22, 17): {(21, 17): 1, (22, 18): 5, (23, 17): 1}, (21, 23): {(21, 22): 1, (20, 23): 1}, (20, 1): {(19, 1): 5, (20, 0): 1}, (18, 17): {(19, 17): 1, (17, 17): 1, (18, 18): 1}, (16, 2): {(17, 2): 1}, (23, 20): {(23, 19): 1, (23, 21): 1, (22, 20): 1, (24, 20): 1}, (22, 4): {(23, 4): 1, (22, 5): 1}, (21, 4): {(20, 4): 8, (21, 5): 1}, (8, 7): {(8, 6): 1, (7, 7): 1}, (23, 1): {(24, 1): 1, (22, 1): 1, (23, 0): 1, (23, 2): 1}, (22, 11): {(23, 11): 1, (22, 10): 1, (22, 12): 1, (21, 11): 1}, (9, 6): {(8, 6): 1, (10, 6): 1, (9, 7): 1}, (11, 7): {(11, 8): 1, (11, 6): 1}, (10, 5): {(10, 6): 1, (10, 4): 1, (11, 5): 1}, (15, 24): {(14, 24): 6}, (14, 16): {(14, 17): 1, (15, 16): 1, (13, 16): 10}, (12, 0): {(11, 0): 1, (12, 1): 1}, (11, 8): {(11, 7): 1, (10, 8): 10, (12, 8): 1}, (10, 16): {(10, 15): 3, (10, 17): 1}, (0, 19): {(1, 19): 4}, (15, 21): {(16, 21): 1, (14, 21): 1}, (14, 7): {(14, 6): 1, (15, 7): 1, (14, 8): 1}, (13, 5): {(13, 4): 1, (14, 5): 1}, (12, 19): {(12, 20): 1}, (1, 18): {(1, 17): 1}, (0, 6): {(0, 5): 1, (0, 7): 1}, (15, 6): {(15, 5): 1, (15, 7): 1}, (13, 18): {(13, 17): 1, (13, 19): 1}, (1, 7): {(2, 7): 1, (1, 6): 1, (0, 7): 1}, (0, 9): {(0, 8): 1, (1, 9): 1, (0, 10): 1}, (16, 21): {(16, 22): 1, (15, 21): 1, (17, 21): 1, (16, 20): 1}, (3, 4): {(3, 3): 1, (3, 5): 1}, (2, 4): {(2, 3): 1, (1, 4): 1}, (5, 9): {(4, 9): 1, (5, 8): 1}, (4, 7): {(3, 7): 1, (4, 6): 1, (4, 8): 1}, (6, 6): {(6, 7): 1, (6, 5): 1}, (5, 6): {(5, 5): 1, (4, 6): 1}, (4, 18): {(5, 18): 1, (3, 18): 1, (4, 17): 1}, (7, 7): {(6, 7): 1, (7, 6): 1, (7, 8): 1, (8, 7): 1}, (6, 21): {(6, 20): 2, (6, 22): 1}, (5, 19): {(6, 19): 1, (5, 18): 1, (4, 19): 1}, (19, 15): {(19, 16): 1, (20, 15): 1}, (17, 3): {(17, 2): 1, (16, 3): 1, (17, 4): 1}, (7, 16): {(6, 16): 6, (7, 17): 1}, (6, 24): {(7, 24): 5}, (21, 16): {(21, 17): 1, (21, 15): 10, (20, 16): 1}, (20, 8): {(19, 8): 1, (20, 9): 1, (21, 8): 1}, (19, 0): {(19, 1): 1}, (18, 8): {(18, 7): 1, (19, 8): 1, (17, 8): 6, (18, 9): 1}, (17, 16): {(17, 17): 1}, (16, 24): {(16, 23): 1}, (21, 13): {(21, 12): 1}, (16, 23): {(16, 22): 1, (16, 24): 1, (15, 23): 1}, (8, 14): {(8, 13): 1, (7, 14): 1, (9, 14): 1}, (22, 2): {(22, 3): 1, (22, 1): 5, (21, 2): 1}, (9, 15): {(10, 15): 1, (9, 14): 1, (8, 15): 1}, (8, 1): {(8, 0): 1, (8, 2): 1, (9, 1): 1}, (23, 11): {(22, 11): 1, (24, 11): 1, (23, 10): 4}, (10, 12): {(10, 13): 1, (9, 12): 2}, (8, 20): {(9, 20): 1}, (23, 21): {(23, 20): 1, (24, 21): 1, (22, 21): 1}, (11, 1): {(11, 0): 1, (11, 2): 1}, (9, 17): {(8, 17): 1, (9, 18): 1, (9, 16): 1, (10, 17): 1}, (15, 18): {(14, 18): 1, (16, 18): 1, (15, 17): 1}, (14, 14): {(15, 14): 1, (14, 15): 1, (14, 13): 1}, (12, 10): {(12, 11): 1}, (11, 18): {(12, 18): 1, (11, 17): 1, (10, 18): 1}, (10, 22): {(10, 23): 1, (11, 22): 1}, (15, 15): {(14, 15): 5, (15, 14): 1, (15, 16): 1}, (13, 11): {(14, 11): 1, (13, 10): 1, (12, 11): 1}, (12, 21): {(13, 21): 1, (12, 22): 1, (11, 21): 1}, (2, 16): {(3, 16): 1, (1, 16): 1, (2, 17): 1}, (1, 24): {(0, 24): 1, (1, 23): 1}, (0, 0): {(0, 1): 1, (1, 0): 1}, (13, 24): {(13, 23): 1, (12, 24): 1}, (3, 13): {(4, 13): 1, (2, 13): 1}, (1, 13): {(0, 13): 1, (2, 13): 1, (1, 14): 4}, (16, 20): {(15, 20): 8, (16, 19): 1, (16, 21): 1, (17, 20): 9}, (4, 14): {(5, 14): 1, (4, 15): 1}, (2, 10): {(3, 10): 1, (2, 11): 1}, (24, 10): {(24, 9): 1, (23, 10): 1}, (5, 15): {(5, 14): 2, (6, 15): 1}, (3, 19): {(2, 19): 1, (3, 20): 1, (4, 19): 1}, (6, 12): {(6, 11): 1, (5, 12): 1}, (4, 20): {(4, 21): 1, (5, 20): 1, (3, 20): 8}, (19, 20): {(18, 20): 9}, (17, 4): {(17, 5): 1, (17, 3): 1}, (7, 9): {(8, 9): 1, (6, 9): 1, (7, 10): 1}, (6, 19): {(6, 20): 1, (6, 18): 1, (5, 19): 1}, (20, 23): {(21, 23): 1, (20, 22): 1, (20, 24): 1}, (19, 9): {(19, 10): 2, (18, 9): 1}, (18, 3): {(18, 4): 2, (18, 2): 1}, (17, 9): {(16, 9): 1}, (22, 22): {(22, 23): 1, (22, 21): 1}, (21, 22): {(21, 23): 1, (21, 21): 1, (20, 22): 1}, (20, 2): {(19, 2): 1, (21, 2): 1}, (18, 14): {(18, 13): 1, (17, 14): 1}, (23, 23): {(22, 23): 1, (24, 23): 1}, (20, 13): {(20, 12): 5, (20, 14): 10, (19, 13): 1}, (17, 17): {(16, 17): 1, (17, 18): 1, (17, 16): 1, (18, 17): 1}, (8, 8): {(8, 9): 1}, (23, 0): {(24, 0): 1, (23, 1): 1}, (22, 8): {(23, 8): 1, (22, 7): 1, (21, 8): 1}, (16, 15): {(16, 16): 1, (17, 15): 1}, (9, 5): {(8, 5): 1}, (23, 13): {(23, 12): 2, (23, 14): 2, (22, 13): 1}, (24, 7): {(24, 6): 9, (24, 8): 1, (23, 7): 1}, (11, 6): {(11, 7): 1, (11, 5): 1}, (10, 2): {(9, 2): 1, (11, 2): 1}, (14, 17): {(14, 16): 1, (15, 17): 1}, (12, 1): {(12, 2): 1, (12, 0): 1}, (11, 11): {(12, 11): 1}, (10, 17): {(10, 16): 1, (9, 17): 1, (10, 18): 1}, (0, 20): {(0, 21): 6}, (15, 20): {(16, 20): 8}, (14, 4): {(15, 4): 1}, (13, 4): {(12, 4): 1, (13, 5): 1, (13, 3): 1}, (12, 12): {(12, 13): 1, (13, 12): 1, (11, 12): 1, (12, 11): 1}, (1, 17): {(1, 18): 1, (0, 17): 1, (2, 17): 1}, (0, 7): {(0, 6): 1, (1, 7): 1}, (15, 1): {(16, 1): 1, (15, 0): 1}, (13, 17): {(13, 18): 1, (13, 16): 1}, (2, 22): {(2, 23): 5, (2, 21): 1, (3, 22): 1}, (1, 6): {(1, 5): 1, (2, 6): 1, (1, 7): 1}, (0, 10): {(1, 10): 1, (0, 9): 1, (0, 11): 1}, (17, 13): {(17, 14): 1, (16, 13): 1, (17, 12): 1}, (3, 7): {(3, 8): 1, (2, 7): 1, (4, 7): 1}, (2, 5): {(1, 5): 5, (3, 5): 1}, (1, 11): {(1, 10): 2, (2, 11): 1, (1, 12): 2}, (16, 19): {(15, 19): 1, (17, 19): 1, (16, 18): 1, (16, 20): 1}, (5, 8): {(5, 9): 1, (5, 7): 1}, (4, 0): {(3, 0): 1, (4, 1): 1, (5, 0): 1}, (3, 24): {(3, 23): 1, (4, 24): 1}, (6, 7): {(5, 7): 1, (7, 7): 1, (6, 6): 1}, (5, 5): {(5, 6): 1, (6, 5): 1}, (4, 19): {(3, 19): 1, (5, 19): 1}, (21, 18): {(22, 18): 1, (21, 19): 1}, (7, 6): {(7, 5): 1, (7, 7): 1}, (6, 10): {(6, 11): 1, (7, 10): 1}, (5, 18): {(4, 18): 1, (6, 18): 1, (5, 19): 1}, (19, 14): {(20, 14): 1}, (17, 2): {(16, 2): 1, (17, 3): 1, (17, 1): 1, (18, 2): 1}, (7, 19): {(7, 20): 1, (8, 19): 1, (7, 18): 1}, (20, 9): {(20, 10): 1, (20, 8): 1}, (19, 3): {(19, 4): 1}, (18, 9): {(18, 8): 1, (19, 9): 1, (18, 10): 1}, (17, 23): {(17, 24): 1, (17, 22): 1}, (22, 5): {(22, 4): 1, (23, 5): 1, (21, 5): 1}, (21, 12): {(22, 12): 1, (21, 13): 1}, (20, 4): {(21, 4): 8, (19, 4): 1, (20, 3): 1}, (18, 20): {(19, 20): 9, (18, 21): 1, (18, 19): 1}, (8, 15): {(8, 16): 1, (7, 15): 1, (9, 15): 1}, (22, 3): {(23, 3): 1, (22, 2): 1}, (9, 14): {(8, 14): 1, (10, 14): 1, (9, 15): 1}, (8, 2): {(8, 1): 1, (9, 2): 1, (8, 3): 1, (7, 2): 1}, (23, 10): {(23, 11): 4, (22, 10): 1, (24, 10): 1}, (10, 13): {(9, 13): 1, (10, 12): 1, (11, 13): 1}, (9, 3): {(8, 3): 1, (10, 3): 1}, (8, 21): {(9, 21): 10, (7, 21): 1}, (14, 24): {(15, 24): 6, (14, 23): 1}, (11, 0): {(11, 1): 1, (12, 0): 1}, (10, 24): {(11, 24): 1, (9, 24): 1}, (9, 16): {(9, 17): 1}, (24, 24): {(23, 24): 1, (24, 23): 1}, (14, 15): {(13, 15): 1, (15, 15): 5, (14, 14): 1}, (12, 11): {(12, 10): 1, (12, 12): 1, (11, 11): 1, (13, 11): 1}, (11, 21): {(12, 21): 1, (10, 21): 1, (11, 20): 1, (11, 22): 1}, (10, 23): {(11, 23): 1, (10, 22): 1}, (15, 14): {(15, 15): 1, (14, 14): 1}, (14, 2): {(14, 1): 1, (13, 2): 1}, (13, 10): {(14, 10): 1, (13, 11): 1}, (12, 22): {(12, 21): 1, (12, 23): 1, (11, 22): 1}, (2, 17): {(2, 16): 1, (3, 17): 1, (1, 17): 1}, (16, 17): {(16, 18): 1, (17, 17): 1}, (0, 1): {(0, 0): 1, (0, 2): 1, (1, 1): 1}, (13, 23): {(13, 22): 1, (13, 24): 1}, (3, 12): {(3, 11): 1, (2, 12): 1}, (1, 12): {(1, 11): 2}, (4, 15): {(4, 14): 1, (4, 16): 1}, (3, 1): {(3, 2): 1, (4, 1): 1}, (2, 11): {(1, 11): 1, (2, 12): 1, (2, 10): 1}, (24, 6): {(24, 7): 9}, (16, 18): {(16, 17): 1, (16, 19): 1, (15, 18): 1}, (5, 14): {(5, 15): 2, (5, 13): 1, (4, 14): 1, (6, 14): 1}, (3, 18): {(4, 18): 1, (2, 18): 1}, (6, 13): {(7, 13): 1, (5, 13): 1, (6, 14): 1}, (4, 21): {(4, 20): 1}, (19, 23): {(18, 23): 10, (19, 24): 1}, (7, 8): {(7, 7): 1}, (6, 16): {(7, 16): 6, (6, 17): 1, (6, 15): 1, (5, 16): 1}, (21, 24): {(22, 24): 1, (20, 24): 1}, (20, 16): {(20, 15): 1, (20, 17): 1, (21, 16): 1}, (19, 8): {(18, 8): 1, (20, 8): 1}, (18, 0): {(17, 0): 5}, (17, 8): {(18, 8): 6, (17, 7): 1}, (7, 21): {(7, 20): 1, (7, 22): 1, (8, 21): 1}, (22, 23): {(23, 23): 1, (22, 24): 1, (22, 22): 1}, (21, 21): {(21, 22): 1, (20, 21): 1, (21, 20): 1, (22, 21): 1}, (20, 3): {(20, 4): 1}, (18, 15): {(18, 16): 1, (17, 15): 1}, (23, 22): {(24, 22): 1}, (21, 2): {(21, 1): 4, (22, 2): 1, (21, 3): 1, (20, 2): 1}, (8, 9): {(8, 8): 1, (7, 9): 1}, (23, 3): {(23, 4): 1, (22, 3): 1, (24, 3): 1}, (22, 9): {(21, 9): 1, (22, 10): 1, (23, 9): 1}, (9, 4): {(8, 4): 8}, (16, 14): {(16, 13): 1}, (23, 12): {(23, 13): 2}, (10, 3): {(9, 3): 1, (11, 3): 1, (10, 4): 1}, (24, 3): {(23, 3): 1, (24, 2): 1, (24, 4): 6}, (24, 22): {(23, 22): 1, (24, 21): 1, (24, 23): 1}, (14, 22): {(13, 22): 1, (15, 22): 1}, (12, 2): {(12, 1): 1, (13, 2): 1, (12, 3): 1}, (11, 10): {(11, 9): 1}, (0, 21): {(1, 21): 1, (0, 22): 1, (0, 20): 6}, (15, 23): {(15, 22): 3, (14, 23): 1, (16, 23): 1}, (14, 5): {(15, 5): 1, (13, 5): 1}, (13, 3): {(14, 3): 1, (13, 4): 1, (13, 2): 1, (12, 3): 1}, (12, 13): {(12, 12): 1, (13, 13): 1, (12, 14): 1, (11, 13): 1}, (1, 16): {(2, 16): 1, (0, 16): 1, (1, 15): 4}, (0, 24): {(1, 24): 1, (0, 23): 7}, (15, 0): {(16, 0): 1, (14, 0): 1, (15, 1): 1}, (13, 16): {(13, 17): 1, (14, 16): 10, (12, 16): 1}, (12, 24): {(12, 23): 1, (13, 24): 1}, (2, 23): {(2, 24): 1, (2, 22): 5, (1, 23): 1}, (1, 5): {(1, 6): 1, (2, 5): 5, (0, 5): 1, (1, 4): 1}, (0, 11): {(0, 10): 1, (0, 12): 1}, (3, 6): {(2, 6): 1, (3, 5): 1}, (2, 2): {(2, 3): 1, (2, 1): 1}, (1, 10): {(1, 11): 2, (0, 10): 1}, (4, 1): {(4, 2): 1, (3, 1): 1, (4, 0): 1}, (6, 4): {(6, 3): 1, (5, 4): 9, (6, 5): 1}, (5, 4): {(6, 4): 9}, (24, 14): {(23, 14): 1, (24, 13): 1, (24, 15): 1}, (7, 1): {(7, 0): 1, (7, 2): 1}, (6, 11): {(6, 12): 1, (6, 10): 1, (5, 11): 1}, (5, 17): {(6, 17): 10}, (19, 17): {(19, 16): 1, (18, 17): 1}, (17, 1): {(17, 2): 1, (17, 0): 7, (18, 1): 1}, (7, 18): {(7, 19): 1, (6, 18): 1, (8, 18): 1}, (20, 10): {(19, 10): 1, (20, 9): 1}, (19, 2): {(20, 2): 1, (19, 1): 1, (18, 2): 1}, (18, 6): {(18, 7): 1, (18, 5): 1, (17, 6): 1, (19, 6): 1}, (17, 22): {(16, 22): 1, (18, 22): 5, (17, 23): 1}, (24, 8): {(24, 9): 1, (23, 8): 1, (24, 7): 1}, (21, 11): {(22, 11): 1, (20, 11): 1}, (20, 5): {(21, 5): 1, (19, 5): 1}, (18, 21): {(17, 21): 5, (18, 20): 1, (19, 21): 1}, (23, 24): {(24, 24): 1}, (22, 0): {(22, 1): 1}, (9, 13): {(10, 13): 1, (9, 12): 1}, (8, 3): {(7, 3): 1, (9, 3): 1, (8, 2): 1, (8, 4): 1}, (23, 5): {(23, 4): 1, (24, 5): 4, (22, 5): 1}, (10, 10): {(9, 10): 1, (10, 11): 1, (10, 9): 1}, (9, 2): {(9, 1): 3, (8, 2): 1, (10, 2): 1}, (8, 22): {(7, 22): 1}, (11, 3): {(10, 3): 1, (11, 4): 1, (12, 3): 1}, (9, 23): {(9, 24): 1, (8, 23): 1}, (14, 12): {(14, 11): 1, (15, 12): 2}, (12, 4): {(12, 5): 1, (13, 4): 1}, (11, 20): {(12, 20): 1, (11, 19): 1, (11, 21): 1}, (10, 20): {(9, 20): 1}, (15, 9): {(16, 9): 1, (14, 9): 1, (15, 10): 1}, (14, 3): {(13, 3): 1}, (13, 9): {(12, 9): 1}, (12, 23): {(12, 22): 1, (12, 24): 1}, (0, 2): {(1, 2): 1, (0, 1): 1, (0, 3): 1}, (13, 22): {(13, 23): 1, (14, 22): 1}, (3, 15): {(2, 15): 1, (3, 16): 1, (3, 14): 1}, (1, 3): {(0, 3): 1, (2, 3): 1, (1, 4): 1}, (4, 8): {(3, 8): 1, (4, 7): 1, (4, 9): 1}, (3, 0): {(2, 0): 1, (4, 0): 1}, (2, 8): {(2, 9): 1}, (24, 13): {(24, 14): 1, (24, 12): 1}, (5, 13): {(5, 14): 1, (6, 13): 1}, (3, 21): {(3, 22): 1}, (6, 2): {(5, 2): 1, (7, 2): 5}, (4, 22): {(5, 22): 1, (3, 22): 1}, (19, 22): {(18, 22): 1, (20, 22): 1, (19, 21): 1}, (7, 11): {(7, 12): 1, (8, 11): 1, (7, 10): 1}, (6, 17): {(5, 17): 10, (6, 18): 1, (6, 16): 1}, (5, 23): {(5, 22): 1, (4, 23): 5, (5, 24): 1}, (20, 17): {(20, 18): 1, (20, 16): 1, (21, 17): 1}, (19, 11): {(19, 10): 1, (18, 11): 1}, (18, 1): {(17, 1): 1, (18, 2): 1}, (17, 15): {(18, 15): 1, (17, 14): 1, (16, 15): 1}, (7, 20): {(7, 19): 1, (7, 21): 1}, (22, 20): {(23, 20): 1, (22, 21): 1}, (21, 20): {(21, 21): 1, (21, 19): 1}, (20, 12): {(20, 13): 5, (19, 12): 1, (20, 11): 1}, (24, 11): {(23, 11): 1}, (18, 12): {(18, 13): 1, (19, 12): 1}, (23, 17): {(24, 17): 1, (22, 17): 1, (23, 18): 1}, (21, 1): {(21, 2): 4, (21, 0): 1}, (24, 0): {(24, 1): 7, (23, 0): 1}, (8, 10): {(8, 11): 1}, (23, 2): {(24, 2): 1, (23, 1): 1}, (22, 14): {(21, 14): 1, (22, 13): 1}, (9, 11): {(9, 12): 1}, (24, 15): {(24, 14): 1, (24, 16): 1, (23, 15): 1}, (23, 15): {(23, 16): 1, (24, 15): 1}, (10, 0): {(9, 0): 6, (10, 1): 1}, (9, 24): {(10, 24): 1, (8, 24): 1, (9, 23): 1}, (8, 16): {(8, 17): 1, (8, 15): 1}, (14, 23): {(14, 24): 1, (15, 23): 1}, (12, 3): {(12, 2): 1, (11, 3): 1, (13, 3): 1}, (11, 13): {(12, 13): 1, (10, 13): 1, (11, 14): 1}, (0, 22): {(0, 21): 1, (1, 22): 1}, (15, 22): {(16, 22): 1, (15, 23): 3, (14, 22): 1}, (14, 10): {(13, 10): 1, (15, 10): 1}, (13, 2): {(13, 1): 1, (14, 2): 1, (13, 3): 1, (12, 2): 1}, (12, 14): {(12, 13): 1}, (1, 23): {(2, 23): 1, (1, 24): 1, (1, 22): 1, (0, 23): 1}, (15, 3): {(15, 4): 1, (16, 3): 10, (15, 2): 9}, (13, 15): {(13, 14): 1, (14, 15): 1}, (2, 20): {(2, 19): 1, (1, 20): 1}, (1, 4): {(1, 5): 1, (1, 3): 1, (2, 4): 1, (0, 4): 1}, (0, 12): {(0, 11): 1}, (3, 9): {(3, 8): 10, (3, 10): 1, (2, 9): 1}, (2, 3): {(2, 4): 1, (1, 3): 1, (3, 3): 1, (2, 2): 1}, (1, 9): {(0, 9): 1, (1, 8): 1}, (4, 2): {(5, 2): 1, (3, 2): 1, (4, 1): 1, (4, 3): 1}, (2, 14): {(2, 15): 1, (2, 13): 1, (1, 14): 1, (3, 14): 1}, (6, 5): {(6, 4): 1, (5, 5): 1, (6, 6): 1}, (5, 3): {(6, 3): 1, (5, 2): 1, (4, 3): 1}, (7, 0): {(7, 1): 1}, (6, 8): {(6, 9): 1}, (5, 16): {(6, 16): 1, (4, 16): 1}, (20, 24): {(19, 24): 1, (20, 23): 1, (21, 24): 1}, (19, 16): {(19, 15): 1, (19, 17): 1}, (17, 0): {(18, 0): 5, (16, 0): 1, (17, 1): 7}, (7, 13): {(7, 12): 1, (6, 13): 1}, (20, 11): {(20, 12): 1, (21, 11): 1}, (19, 5): {(20, 5): 1, (18, 5): 1, (19, 6): 1}, (18, 7): {(18, 8): 1, (18, 6): 1, (19, 7): 10}, (17, 21): {(18, 21): 5, (16, 21): 1}, (18, 23): {(19, 23): 10}, (21, 10): {(21, 9): 1, (22, 10): 1}, (20, 6): {(21, 6): 1, (20, 7): 1, (19, 6): 1}, (24, 23): {(24, 22): 1, (24, 24): 1, (23, 23): 1}, (18, 18): {(18, 19): 1, (18, 17): 1}, (22, 1): {(22, 2): 5, (22, 0): 1, (23, 1): 1}, (21, 7): {(20, 7): 1, (22, 7): 1}, (24, 19): {(23, 19): 1, (24, 18): 1, (24, 20): 1}, (9, 12): {(9, 13): 1, (9, 11): 1, (10, 12): 2, (8, 12): 1}, (8, 4): {(7, 4): 9, (8, 3): 1, (8, 5): 1, (9, 4): 8}, (23, 4): {(23, 3): 1, (23, 5): 1, (22, 4): 1}, (10, 11): {(10, 10): 1}, (9, 1): {(9, 2): 3, (8, 1): 1, (10, 1): 1}, (8, 23): {(9, 23): 1}, (17, 5): {(17, 6): 1, (16, 5): 1, (17, 4): 1}, (11, 2): {(11, 1): 1, (10, 2): 1}, (10, 6): {(10, 5): 1, (9, 6): 1}, (9, 22): {(9, 21): 9}, (16, 11): {(16, 10): 1, (16, 12): 1}, (14, 13): {(14, 14): 1}, (12, 5): {(12, 4): 1}, (11, 23): {(10, 23): 1, (11, 22): 1}, (10, 21): {(11, 21): 1}, (0, 16): {(0, 17): 1, (1, 16): 1, (0, 15): 1}, (15, 8): {(15, 7): 1}, (14, 0): {(15, 0): 1, (13, 0): 1}, (13, 8): {(13, 7): 1}, (12, 16): {(12, 15): 1, (12, 17): 1, (13, 16): 1}, (11, 24): {(10, 24): 1}, (0, 3): {(1, 3): 1, (0, 2): 1}, (15, 5): {(15, 4): 1, (15, 6): 1, (14, 5): 1}, (13, 21): {(12, 21): 1, (13, 20): 1, (14, 21): 1}, (3, 14): {(3, 15): 1, (2, 14): 1}, (1, 2): {(0, 2): 1}, (4, 9): {(5, 9): 1, (4, 8): 1, (4, 10): 1}, (3, 3): {(2, 3): 1, (3, 2): 1, (3, 4): 1, (4, 3): 1}, (2, 9): {(2, 8): 1, (3, 9): 1}, (5, 12): {(6, 12): 1, (4, 12): 1}, (4, 4): {(4, 5): 1}, (3, 20): {(4, 20): 8, (3, 19): 1}, (24, 9): {(24, 8): 1, (24, 10): 1}, (6, 3): {(6, 4): 1, (7, 3): 5, (5, 3): 1}, (4, 23): {(5, 23): 5, (4, 24): 1}, (16, 7): {(16, 6): 1, (16, 8): 1, (15, 7): 1, (17, 7): 1}, (7, 10): {(7, 11): 1, (6, 10): 1, (7, 9): 1}, (6, 22): {(5, 22): 1, (7, 22): 1, (6, 23): 1, (6, 21): 1}, (5, 22): {(5, 23): 1, (4, 22): 1, (6, 22): 1}, (20, 18): {(19, 18): 1, (20, 17): 1}, (19, 10): {(20, 10): 1, (19, 9): 2, (19, 11): 1, (18, 10): 1}, (17, 14): {(17, 13): 1, (18, 14): 1, (17, 15): 1}, (7, 23): {(7, 24): 7, (7, 22): 1, (6, 23): 1}, (22, 21): {(22, 20): 1, (23, 21): 1, (21, 21): 1, (22, 22): 1}, (21, 19): {(22, 19): 1, (21, 20): 1, (21, 18): 1, (20, 19): 1}, (16, 12): {(15, 12): 1, (16, 11): 1, (16, 13): 1, (17, 12): 1}, (18, 13): {(18, 14): 1, (18, 12): 1, (19, 13): 1}, (17, 19): {(17, 18): 1, (16, 19): 1}, (23, 16): {(24, 16): 1, (23, 15): 1}, (22, 24): {(22, 23): 1, (21, 24): 1}, (21, 0): {(21, 1): 1, (20, 0): 1}, (18, 24): {(19, 24): 1}, (8, 11): {(7, 11): 1, (8, 10): 1, (8, 12): 1}, (22, 15): {(21, 15): 1, (22, 16): 1}, (9, 10): {(9, 9): 1, (10, 10): 1}, (23, 14): {(24, 14): 1, (23, 13): 2}, (16, 16): {(16, 15): 1}, (10, 1): {(10, 0): 1, (9, 1): 1}, (8, 17): {(8, 18): 1, (8, 16): 1, (9, 17): 1, (7, 17): 1}, (14, 20): {(14, 19): 1, (14, 21): 1}, (24, 16): {(23, 16): 1, (24, 15): 1}, (11, 12): {(12, 12): 1}, (0, 23): {(0, 24): 7, (1, 23): 1}, (15, 17): {(14, 17): 1, (15, 16): 1, (15, 18): 1}, (14, 11): {(14, 12): 1, (13, 11): 1, (15, 11): 1}, (13, 1): {(14, 1): 1, (13, 2): 1}, (12, 15): {(11, 15): 1, (12, 16): 1}, (11, 17): {(11, 16): 1, (11, 18): 1, (12, 17): 1}, (1, 22): {(0, 22): 1, (1, 23): 1}, (15, 2): {(15, 3): 9}, (13, 14): {(13, 15): 1}, (2, 21): {(1, 21): 1, (2, 22): 1}, (0, 13): {(1, 13): 1}, (3, 8): {(3, 7): 1, (3, 9): 10, (4, 8): 1}, (2, 0): {(3, 0): 1, (2, 1): 1}, (1, 8): {(0, 8): 1, (1, 9): 1}, (4, 3): {(4, 2): 1, (3, 3): 1, (5, 3): 1}, (2, 15): {(3, 15): 1, (2, 14): 1, (1, 15): 1}, (16, 1): {(15, 1): 1}, (5, 2): {(4, 2): 1, (6, 2): 1, (5, 3): 1}}
w, h = 25, 25
cheeses = [(23, 24), (1, 0), (13, 8), (11, 16), (20, 20), (4, 4), (11, 2), (20, 12), (13, 22), (4, 12), (16, 20), (9, 0), (24, 16), (22, 3), (8, 24), (2, 21), (16, 0), (10, 2), (8, 5), (14, 22), (16, 19), (20, 0), (4, 24), (12, 12), (15, 24), (0, 8), (10, 13), (3, 0), (24, 4), (14, 11), (21, 24), (0, 20), (8, 4), (1, 9), (3, 6), (21, 21), (12, 11), (23, 15), (21, 18), (3, 3), (12, 13)]

player_origin = (24, 0)
opponent_origin = (0, 24)

maze = Maze(mazeMap, w, h)
maze.createMetaGraph(cheeses)
maze.addNodeToMetagraph(player_origin, cheeses)
maze.addNodeToMetagraph(opponent_origin, cheeses + [player_origin])

# Graph

def glouton(origin, nodes_list):
    nl = nodes_list.copy()
    current = origin
    dij = Dijkstra(maze)
    path = ""
    dist = 0

    while nl:
        dij.setOrigin(current)
        dij.setGoal(None)
        dij.process()

        r = []
        for n in nl:
            d, p = dij.getResult(n)
            r.append((d, p, n))

        r.sort()
        current = r[0][2]
        dist += r[0][0]
        path += r[0][1]
        nl.remove(current)

    return (dist, path)

X = []
T1 = []
T2 = []
T3 = []

T11 = []
T22 = []
T33 = []
for k in range(2, len(cheeses)):
    print(k)
    t = time.clock()
    X.append(k)

    ra = rd.randint(0, len(cheeses))
    ra2 = (ra + k) % len(cheeses)
    ch = cheeses[min(ra, ra2) : max(ra, ra2)]
    print(ch)

    # Glouton
    d, p1 = glouton(player_origin, ch)
    T1.append(time.clock() - t)
    T11.append(d)

    # 2-opt
    t = time.clock()
    to = TwoOPT(maze)
    to.setOrigin(player_origin)
    to.setGoals(ch)
    to.process()

    d, p = to.getResult()
    T2.append(time.clock() - t)
    T22.append(d)


    # Ants
    f = Fourmis(maze, player_origin, ch)
    p3 = f.process()
    p4 = ""
    d2 = 0
    for k in range(len(p) - 1):
        p4 += maze.pathMetagraph[p[k]][p[k + 1]]
        d2 += maze.distanceMetagraph[p[k]][p[k + 1]]

    T33.append(d2)

    if k == 9:
        mg = MazeGenerator(mazeMap, w, h)
        mg.showNodes(cheeses)
        mg.showPath(player_origin, p1)
        mg.show()
        p2 = ""
        for k in range(len(p) - 1):
            p2 += maze.pathMetagraph[p[k]][p[k+1]]

        print(p2)

        mg = MazeGenerator(mazeMap, w, h)
        mg.showNodes(cheeses)
        mg.showPath(player_origin, p2, color="grey")
        mg.show()

        mg = MazeGenerator(mazeMap, w, h)
        mg.showNodes(cheeses)

        mg.showPath(player_origin, p4, color="blue")
        mg.show()


print(T11)
print(T22)
plt.plot(X, T11, color='red')
plt.plot(X, T22, color='black')
plt.plot(X, T33, color='black')
plt.show()
