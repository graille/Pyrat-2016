#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from tkinter import *

class MazeGenerator:
    def __init__(self, maze):
        self.maze = maze

        self.NODE_SIZE = 8
        self.MARGE = 40

        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 1000

        self.fenetre = Tk()
        self.canvas = Canvas(self.fenetre, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, background='white')
        self.canvas.pack()

    def generate(self):
        for n in self.maze.nodes:
            self.generateNode(n)

        for i in self.maze.nodes:
            for j in self.maze.nodes:
                if self.maze.getDistance(i, j) != np.inf and i != j:
                    self.generateEdge(i, j, self.maze.getDistance(i, j))

    def generateNode(self, pos, size = None, color = 'black'):
        if not size:
            size = self.NODE_SIZE

        x, y = self.convertToCord(pos)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color)

    def generateEdge(self, i, j, width = 1, color = 'black'):
        x1, y1 = self.convertToCord(i)
        x2, y2 = self.convertToCord(j)
        self.canvas.create_line(x1, y1, x2, y2, width=width, fill=color)

    def getPath(self, origin, pathNodes):
        L = [origin]

        x, y = origin
        for elt in pathNodes:
            if elt == 'L':
                y -= 1
            if elt == 'U':
                x -= 1
            if elt == 'D':
                x += 1
            if elt == 'R':
                y += 1
            L.append((x, y))

        return L

    def showPath(self, origin, path, size = 10, color = 'red'):
        P = self.getPath(origin, path)

        for k in range(len(P) - 1):
            self.generateEdge(P[k], P[k + 1], size, color)

        return P[-1] # Return the last point

    def showPaths(self, origin, paths, color = 'red'):
        size = 10
        current = origin
        for path in paths:
            current = self.showPath(current, path, size, color)
            size += 1

    def convertToCord(self, pos):
        x, y = pos
        w, h = self.WINDOW_WIDTH, self.WINDOW_HEIGHT

        gap_h = (h - 2 * self.MARGE) / (self.maze.mazeHeight - 1)
        gap_w = (w - 2 * self.MARGE) / (self.maze.mazeWidth - 1)

        x = x * gap_h + self.MARGE
        y = y * gap_w + self.MARGE

        return (y,x)

    def showNodes(self, nodes):
        for n in nodes:
            self.generateNode(n, self.NODE_SIZE + 3, 'blue')

    def show(self):
        self.fenetre.mainloop()