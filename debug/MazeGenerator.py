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
        self.MARGIN = 40
        self.DEFAULT_NODE_SIZE = 8
        self.DEFAULT_EDGE_SIZE = 1

        self.WINDOW_WIDTH = int((self.window.winfo_screenheight()) * (1 - 10/100))
        self.WINDOW_HEIGHT = self.WINDOW_WIDTH

        # Add Canvas
        self.canvas = Canvas(self.window, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, background='white')
        self.canvas.pack(side = LEFT, padx = 5, pady = 5)

        pathTracerHeight = int(self.WINDOW_HEIGHT/25)
        self.pathTracer = Text(self.window, width=50, height=pathTracerHeight)
        self.pathTracer.pack(side=RIGHT, pady=5)

        # Object containers
        self.nodesContainer = {}
        self.edgesContainer = {}

        # Colors cycles
        self.PATH_COLOR = ['red', 'grey', 'green', 'blue', 'orange', 'yellow', 'pink', 'cyan4', 'cyan3', 'azure4', 'orchid']
        self.CURRENT_PATH_COLOR = 0

        # List of paths
        self.LIST_WAITING_PATHS = []
        self.LIST_CURRENT_PATHS = []
        self.LIST_COLORS_PATH = []

        # Generation
        self.generate()

    def generate(self):
        font = tkFont.Font(family='Helvetica', size=6)

        # Fill edges container
        for n in self.nodes:
            self.edgesContainer[n] = {}

        # Generate edges
        for i in self.nodes:
            for j in self.nodes:
                if self.getDistance(i, j) != np.inf and i != j:
                    self.generateEdge(i, j, self.getDistance(i, j))

        # Generate nodes
        for n in self.nodes:
            self.generateNode(n)
            x,y = self.convertToCord(n)
            self.canvas.create_text(x - 20, y - 15, text=repr(n), font=font)

    def generateNode(self, pos, size = 8, color = 'black'):
        x, y = self.convertToCord(pos)

        # Create Item
        item = self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color)
        self.nodesContainer[pos] = item


    def generateEdge(self, i, j, size = 1, color = 'black'):
        x1, y1 = self.convertToCord(i)
        x2, y2 = self.convertToCord(j)

        # Create item
        item = self.canvas.create_line(x1, y1, x2, y2, width=size, fill=color)
        self.edgesContainer[i][j], self.edgesContainer[j][i] = item, item

    def generateButtons(self, i):

        b1 = Button(self.window, text="<", command= lambda: self.showPreviousPath(i))
        b2 = Button(self.window, text=">", command= lambda: self.showNextPath(i))

        b1.pack()
        b2.pack()

    def showNextPath(self, i):
        print(self.LIST_COLORS_PATH[i])
        if self.LIST_CURRENT_PATHS[i] < (len(self.LIST_WAITING_PATHS[i]) - 1):
            self.LIST_CURRENT_PATHS[i] += 1
            self.showPath(self.LIST_WAITING_PATHS[i][self.LIST_CURRENT_PATHS[i]], color = self.LIST_COLORS_PATH[i])

    def showPreviousPath(self, i):
        if self.LIST_CURRENT_PATHS[i] > -1:
            self.unshowPath(self.LIST_WAITING_PATHS[i][self.LIST_CURRENT_PATHS[i]])
            self.LIST_CURRENT_PATHS[i] -= 1

    def getDistance(self, from_location, to_location):
        try:
            return self.mazeMap[from_location][to_location]
        except KeyError:
            if to_location == from_location:
                return 0
            else:
                return np.inf

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

        gap_h = (h - 2 * self.MARGIN) / (self.mazeHeight - 1)
        gap_w = (w - 2 * self.MARGIN) / (self.mazeWidth - 1)

        x = x * gap_h + self.MARGIN
        y = y * gap_w + self.MARGIN

        return (y,x)

    # Items writer
    def showNodes(self, nodes, color = "blue", size = 11):
        for n in nodes:
            x, y = self.convertToCord(n)

            self.canvas.coords(self.nodesContainer[n], x - size, y - size, x + size, y + size)
            self.canvas.itemconfig(self.nodesContainer[n], fill=color)

    def showPath(self, *args, **kwargs):
        """
        Ecrit un chemin sur le graph
        :param args: 1 a 2 argument : soit une liste de points, soit une origine et un chemin littéral
        :param kwargs: 2 arguments : color et size
        :return: La destination du chemin
        """

        color = kwargs['color'] if 'color' in kwargs else 'red'
        size = kwargs['size'] if 'size' in kwargs else 10

        # List case
        is_list = False

        if len(args) == 2:
            if not isinstance(args[1], list):
                P = self.getPath(args[0], args[1])
            else: # Si c'est une suite de chemin
                is_list = True
                current, P_list = args[0], []
                for k in range(len(args[1])):
                    P = self.getPath(current, args[1][k])
                    current = P[-1]
                    P_list.append(P)

        elif len(args) == 1 and isinstance(args[0], list) and len(args[0]) > 0:
            if not isinstance(args[0][0], list):
                P = args[0]
            else:
                is_list = True
                P_list = args[0]

        if is_list:
            self.LIST_WAITING_PATHS.append(P_list)
            self.LIST_CURRENT_PATHS.append(-1)
            self.LIST_COLORS_PATH.append(color)

            self.generateButtons(len(self.LIST_WAITING_PATHS) - 1)
        else:
            for k in range(len(P) - 1):
                self.canvas.itemconfig(self.edgesContainer[P[k]][P[k + 1]], width=size, fill=color)

            self.pathTracer.insert(END, "From " + repr(P[0]) + " to " + repr(P[-1]) + " (" + color + ")"'\n')
            return P[-1] # Return the last point

    def unshowPath(self, path):
        for k in range(len(path) - 1):
            self.canvas.itemconfig(self.edgesContainer[path[k]][path[k + 1]], width=self.DEFAULT_EDGE_SIZE, fill='black')

    def show(self):
        self.window.mainloop()