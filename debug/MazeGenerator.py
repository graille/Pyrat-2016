#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from tkinter import *
import tkinter.font as tkFont

class MazeGenerator():
    def __init__(self, mazeMap, mazeWidth, mazeHeight):
        self.window = Tk()
        self.window.title("Maze viewer")

        # Save Maze
        self.mazeMap = mazeMap
        self.mazeHeight = mazeHeight
        self.mazeWidth = mazeWidth

        self.nodes = list(self.mazeMap.keys())

        # Configuration
        self.NODE_SIZE = 8
        self.MARGE = 40

        self.WINDOW_WIDTH = int((self.window.winfo_screenwidth() / 2) * (1 - 5/100))
        self.WINDOW_HEIGHT = self.WINDOW_WIDTH

        # Add Canvas
        self.canvas = Canvas(self.window, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, background='white')
        self.canvas.pack(side = LEFT, padx = 5, pady = 5)

        pathTracerHeight = int(self.WINDOW_HEIGHT/25)
        self.pathTracer = Text(self.window, width=50, height=pathTracerHeight)
        self.pathTracer.pack(side=RIGHT, pady=5)

        # Generation
        self.generate()

    def generate(self):
        font = tkFont.Font(family='Helvetica', size=6)

        for n in self.nodes:
            self.generateNode(n)
            x,y = self.convertToCord(n)
            self.canvas.create_text(x - 20, y - 15, text=repr(n), font=font)

        for i in self.nodes:
            for j in self.nodes:
                if self.getDistance(i, j) != np.inf and i != j:
                    self.generateEdge(i, j, self.getDistance(i, j))

    def getDistance(self, from_location, to_location):
        try:
            return self.mazeMap[from_location][to_location]
        except KeyError:
            if to_location == from_location:
                return 0
            else:
                return np.inf

    def generateNode(self, pos, size = 8, color = 'black'):
        if not size:
            size = self.NODE_SIZE

        x, y = self.convertToCord(pos)
        self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color)

    def generateEdge(self, i, j, size = 1, color = 'black'):
        x1, y1 = self.convertToCord(i)
        x2, y2 = self.convertToCord(j)
        self.canvas.create_line(x1, y1, x2, y2, width=size, fill=color)

    def showNodes(self, nodes, color = "blue", size = 11):
        for n in nodes:
            self.generateNode(n, size, color)

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

    def convertToCord(self, pos):
        x, y = pos

        w, h = self.WINDOW_WIDTH, self.WINDOW_HEIGHT

        gap_h = (h - 2 * self.MARGE) / (self.mazeHeight - 1)
        gap_w = (w - 2 * self.MARGE) / (self.mazeWidth - 1)

        x = x * gap_h + self.MARGE
        y = y * gap_w + self.MARGE

        return (y,x)

    # Path writer
    def showPath(self, *args, **kwargs):
        """
        Ecrit un chemin sur le graph
        :param args: 1 a 2 argument : soit une liste de points, soit une origine et un chemin littéral
        :param kwargs: 2 arguments : color et size
        :return: La destination du chemin
        """

        color = kwargs['color'] if 'color' in kwargs else 'red'
        size = kwargs['size'] if 'size' in kwargs else 10

        if len(args) == 2:
            P = self.getPath(args[0], args[1])
        elif len(args) == 1:
            P = args[0]

        for k in range(len(P) - 1):
            self.generateEdge(P[k], P[k + 1], size, color)

        self.pathTracer.insert(END, "From " + repr(P[0]) + " to " + repr(P[-1]) + " (" + color + ")"'\n')
        return P[-1] # Return the last point

    def show(self):
        self.window.mainloop()