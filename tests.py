#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from debug.MazeViewer import *
from process.Engine import *
from algorithms.TwoOPT import *
from algorithms.Fourmis import *
from algorithms.Kmeans import *

mazeMap = {(7, 3): {(6, 3): 1, (7, 2): 1}, (4, 7): {(3, 7): 2, (4, 6): 1}, (1, 3): {(0, 3): 1, (1, 4): 1}, (6, 4): {(7, 4): 1, (6, 3): 1}, (3, 0): {(3, 1): 1, (4, 0): 2}, (5, 4): {(5, 3): 1}, (0, 7): {(0, 6): 1}, (5, 6): {(5, 7): 1, (4, 6): 1, (5, 5): 1, (6, 6): 1}, (0, 0): {(0, 1): 1, (1, 0): 1}, (1, 6): {(2, 6): 1}, (5, 1): {(5, 2): 6, (6, 1): 1, (4, 1): 1}, (3, 7): {(2, 7): 1, (4, 7): 2, (3, 6): 1}, (0, 3): {(1, 3): 1, (0, 2): 1}, (2, 5): {(1, 5): 1, (2, 6): 6}, (7, 2): {(7, 3): 1, (6, 2): 1, (7, 1): 1}, (4, 0): {(3, 0): 2, (4, 1): 1, (5, 0): 1}, (1, 2): {(1, 1): 1, (2, 2): 10}, (6, 7): {(5, 7): 1, (7, 7): 1, (6, 6): 1}, (3, 3): {(3, 2): 1, (3, 4): 1, (4, 3): 1}, (0, 6): {(0, 5): 1, (0, 7): 1}, (7, 6): {(7, 5): 1, (7, 7): 1}, (4, 4): {(4, 5): 1, (3, 4): 1, (4, 3): 3}, (6, 3): {(7, 3): 1, (6, 4): 1, (6, 2): 1, (5, 3): 1}, (1, 5): {(2, 5): 1, (0, 5): 1, (1, 4): 1}, (3, 6): {(3, 7): 1, (2, 6): 1}, (0, 4): {(0, 5): 1, (1, 4): 1}, (7, 7): {(7, 6): 1, (6, 7): 1}, (5, 7): {(5, 6): 1, (6, 7): 1}, (5, 3): {(6, 3): 1, (5, 4): 1, (4, 3): 1}, (4, 1): {(5, 1): 1, (4, 0): 1}, (1, 1): {(1, 2): 1, (1, 0): 1, (2, 1): 1}, (0, 1): {(0, 0): 1, (0, 2): 1}, (3, 2): {(3, 1): 1, (3, 3): 1}, (2, 6): {(2, 5): 6, (1, 6): 1, (3, 6): 1}, (6, 6): {(5, 6): 1, (6, 7): 1, (6, 5): 1}, (5, 0): {(6, 0): 1, (4, 0): 1}, (7, 1): {(7, 0): 1, (7, 2): 1}, (4, 5): {(4, 4): 1, (4, 6): 1}, (2, 2): {(1, 2): 10, (2, 1): 1}, (5, 5): {(5, 6): 1, (6, 5): 10}, (1, 4): {(1, 5): 1, (1, 3): 1, (2, 4): 1, (0, 4): 1}, (6, 0): {(5, 0): 1}, (7, 5): {(7, 4): 1, (7, 6): 1}, (0, 5): {(0, 6): 1, (1, 5): 1, (0, 4): 1}, (2, 1): {(2, 0): 1, (3, 1): 1, (1, 1): 1, (2, 2): 1}, (4, 2): {(4, 3): 6}, (1, 0): {(2, 0): 1, (0, 0): 1, (1, 1): 1}, (6, 5): {(5, 5): 10, (6, 6): 1}, (3, 5): {(3, 4): 6}, (2, 7): {(3, 7): 1, (1, 7): 1}, (7, 0): {(7, 1): 1}, (4, 6): {(5, 6): 1, (4, 5): 1, (4, 7): 1}, (3, 4): {(4, 4): 1, (3, 3): 1, (3, 5): 6, (2, 4): 1}, (6, 1): {(5, 1): 1}, (3, 1): {(3, 0): 1, (3, 2): 1, (2, 1): 1}, (2, 4): {(2, 3): 1, (3, 4): 1, (1, 4): 1}, (7, 4): {(6, 4): 1, (7, 5): 1}, (2, 0): {(1, 0): 1, (2, 1): 1}, (6, 2): {(6, 3): 1, (5, 2): 1, (7, 2): 1}, (4, 3): {(4, 2): 6, (4, 4): 3, (3, 3): 1, (5, 3): 1}, (1, 7): {(2, 7): 1}, (2, 3): {(2, 4): 1}, (5, 2): {(5, 1): 6, (6, 2): 1}, (0, 2): {(0, 1): 1, (0, 3): 1}}
cheeses = [(7, 3), (0, 4), (6, 7), (1, 0), (5, 3), (2, 4), (7, 2), (0, 5), (4, 6), (7, 5), (1, 7), (3, 1), (0, 2), (6, 0), (1, 2), (6, 5), (5, 1), (2, 2), (2, 6), (5, 5)]

w, h = 8,8
player_origin = (7,0)

#mg.showNodes(cheeses, size=15)
engine = Engine(mazeMap, w, h)
engine.update((7,0), (0,7), 0, 0, cheeses, 3)
engine.maze.addNodeToMetagraph(player_origin, cheeses)


#d, p = engine.maze.getGloutonPath(player_origin, cheeses)
#p = engine.maze.convertMetaPathToRealPaths(p)
#print("Glouton dist : "+ str(d))

# dm = np.inf
# pm = []
#
# for j in range(1000):
#     if j % 10 == 0:
#         print("## " + str(j))
#     to = TwoOPT(engine.maze, cheeses + [player_origin])
#     to.process()
#     d, p = to.getResult(player_origin)
#     if d < dm:
#         dm, pm = d, p
#
# print("Best : " + str(dm))
# p = engine.maze.convertMetaPathToRealPaths(p)


# t = time.clock()
# f = Fourmis(engine.maze, player_origin, cheeses)
# p = f.process()
#
# print("time : " + str(time.clock() - t))
#
# p = engine.maze.convertMetaPathToRealPaths(p)
# d = 0
# for l in p:
#     for k in range(len(l) - 1):
#         d += engine.maze.getDistance(l[k], l[k + 1])
#
# print("dist : " + str(d))


km = K_Means(engine.maze, 4, cheeses)
km.process(None, 20)

m, S = km.m, km.S
print(m)
for i in range(len(m) - 1):
    mg = MazeViewer(mazeMap, w, h)
    mg.CURRENT_PATH_COLOR = 0
    for j in range(len(m[i])):
        print(m[i][j])
        mg.showNodes(S[i][j],  color=mg.PATH_COLOR[mg.CURRENT_PATH_COLOR], size=15)
        mg.showNodes([m[i][j]], color=mg.PATH_COLOR[mg.CURRENT_PATH_COLOR], size=25)
        mg.CURRENT_PATH_COLOR = (mg.CURRENT_PATH_COLOR + 1) % len(mg.PATH_COLOR)

    mg.show()



