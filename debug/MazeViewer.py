#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Codé et maintenu par Thibault PIANA

# TODO :
        # - Clear un chemin
        # - Faire un gif animé automatiquement
        # - Ne plus avoir besoin de spécifier la couleur : gestion automatique

import numpy as np

from tkinter import *
import tkinter.font as tkFont


class MazeViewer:
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

        # Canvas
        self.canvas = Canvas(self.window, width=self.WINDOW_WIDTH, height=self.WINDOW_HEIGHT, background='white')

        # Logs
        pathTracerHeight = int(self.WINDOW_HEIGHT/25)
        self.pathTracer = Text(self.window, width=50, height=pathTracerHeight)

        # Object containers
        self.nodesContainer = {}
        self.edgesContainer = {} # edgesContainer[i][j][k] :
                    # (i,j) : départ et arrivé de l'arête
                    # k : couche de l'arête

        # Container de chemins
        self.pathContainer = {} # pathList[path_id][?] :
                    # path_id : id du chemin
                    # ? :
                        # path : list of differents paths;
                        # color : pathColor; [last_color] : color of the last edge;
                        # current : current state of the path;
                        # layers : couches écrites pour ce chemin (dans l'ordre)

        self.CURRENT_LAYER = 0

        # Colors cycles
        self.PATH_COLOR = ['red', 'grey', 'green', 'blue', 'orange', 'yellow', 'pink', 'cyan4', 'cyan3', 'azure4', 'orchid']
        self.PRE_PATH_COLOR = {'red' : 'orchid',
                               'grey' : 'red',
                               'green' : 'cyan4',
                               'blue' : 'green'}
        self.CURRENT_PATH_COLOR = 0

        # Generation
        self.generate()

    def generate(self):
        font = tkFont.Font(family='Helvetica', size=6)

        # Fill edges container
        for i in self.nodes:
            self.edgesContainer[i] = {}
            for j in self.nodes:
                self.edgesContainer[i][j] = {}

        # Generate edges
        for i in self.nodes:
            for j in self.nodes:
                if self.getDistance(i, j) != np.inf and i != j:
                    self.generateEdge(i, j, self.getDistance(i, j), 'black', 0)

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

        return item

    def generateEdge(self, i, j, size = 1, color = 'black', layer = 0):
        x1, y1 = self.convertToCord(i)
        x2, y2 = self.convertToCord(j)

        # Création de l'arête
        item = self.canvas.create_line(x1, y1, x2, y2, width=size, fill=color)
        self.edgesContainer[i][j][layer], self.edgesContainer[j][i][layer] = item, item

        return item

    def generateButtons(self, path_id):
        # Declaration des boutons de contôles de la couche layer
        b1 = Button(self.window, text="<< (Reculer)", width=10, command= lambda: self.showPreviousPath(path_id))
        b2 = Button(self.window, text=">> (Avancer)", width=10, command= lambda: self.showNextPath(path_id))

        # On affiche
        Label(self.window, text="Chemin n°" + repr(path_id)).grid(column=1, row=path_id, sticky=W)
        b1.grid(row=path_id, column=2)
        b2.grid(row=path_id, column=3)

    def showNextPath(self, path_id):
        if self.pathContainer[path_id]['current'] < (len(self.pathContainer[path_id]['path']) - 1):
            # On remet la couleur naturelle du chemin actuel
            if self.pathContainer[path_id]['current'] >= 0:
                P = self.pathContainer[path_id]['path'][self.pathContainer[path_id]['current']]
                layer = self.pathContainer[path_id]['layers'][-1]
                for k in range(len(P) - 1):
                    self.canvas.itemconfig(self.edgesContainer[P[k]][P[k+1]][layer], fill=self.pathContainer[path_id]['color'])

            # On écrit sur une nouvelle couche
            self.CURRENT_LAYER += 1
            self.pathContainer[path_id]['layers'].append(self.CURRENT_LAYER)

            # On écrit l'arête sur cette nouvelle couche
            self.pathContainer[path_id]['current'] += 1
            P = self.pathContainer[path_id]['path'][self.pathContainer[path_id]['current']]
            self.writePath(P, self.pathContainer[path_id]['size'], self.pathContainer[path_id]['last_color'], self.CURRENT_LAYER)

            # On affiche un log
            self.writeLog("Chemin de " + repr(P[0]) + " à " + repr(P[-1]))
        else:
            self.writeLog("Fin du chemin " + repr(self.pathContainer[path_id]['color']))

    def showPreviousPath(self, path_id):
        if self.pathContainer[path_id]['current'] > -1:
            self.deletePath(self.pathContainer[path_id]['path'][self.pathContainer[path_id]['current']], self.pathContainer[path_id]['layers'][-1])

            # On modifie l'arête courante
            self.pathContainer[path_id]['current'] -= 1

            if self.pathContainer[path_id]['current'] >= 0:
                # On enleve la dernière couche de la liste
                self.pathContainer[path_id]['layers'].pop()

                # On remet le chemin précédent dans sa couleur intermédiaire
                P = self.pathContainer[path_id]['path'][self.pathContainer[path_id]['current']]
                layer = self.pathContainer[path_id]['layers'][-1]
                for k in range(len(P) - 1):
                    self.canvas.itemconfig(self.edgesContainer[P[k]][P[k+1]][layer], fill=self.pathContainer[path_id]['last_color'])

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
    def showNodes(self, nodes, **kwargs):
        color = kwargs['color'] if 'color' in kwargs else 'blue'
        size = kwargs['size'] if 'size' in kwargs else 11

        for n in nodes:
            x, y = self.convertToCord(n)
            try:
                item = self.nodesContainer[n]
                self.canvas.coords(item, x - size, y - size, x + size, y + size)
            except KeyError:
                item = self.generateNode(n, size, color)

            self.canvas.itemconfig(item, fill=color)

    def writePath(self, P, size, color, layer):
        for k in range(len(P) - 1):
                self.generateEdge(P[k], P[k + 1], size, color, layer)

        return P[-1]  # Return the last point

    def writeLog(self, log):
        self.pathTracer.insert(END, log + '\n')
        self.pathTracer.see(END)

    def deletePath(self, P, layer):
        for k in range(len(P) - 1):
            self.canvas.delete(self.edgesContainer[P[k]][P[k + 1]][layer])

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

        # Si c'est un chemin avec origine + mouvements
        if len(args) == 2:
            if not isinstance(args[1], list):
                P = self.getPath(args[0], args[1])
            else:  # Si c'est une suite de chemin
                is_list = True
                current, P_list = args[0], []
                for k in range(len(args[1])):
                    P = self.getPath(current, args[1][k])
                    current = P[-1]
                    P_list.append(P)

        # Si c'est un chemin avec liste de noeuds adjacents
        elif len(args) == 1 and isinstance(args[0], list) and len(args[0]) > 0:
            if not isinstance(args[0][0], list):
                P = args[0]
            else:  # Si c'est une suite de chemin
                is_list = True
                P_list = args[0]

        # Ici :
            # Si c'est un chemin simple, P existe et le contient, et is_list = False
            # Si c'est une série de chemin, P_list existe et la contient, et is_list = True

        if is_list:
            # On détermine un ID pour le chemin
            path_id = len(list(self.pathContainer.keys()))

            # On enregistre la série de chemin pour pouvoir l'exploiter avec les boutons plus tard
            self.pathContainer[path_id] = {}
            self.pathContainer[path_id]['path'] = P_list
            self.pathContainer[path_id]['current'] = -1
            self.pathContainer[path_id]['color'] = color
            self.pathContainer[path_id]['size'] = size
            self.pathContainer[path_id]['layers'] = []

            # Détermination de la pré-couleur
            try:
                self.pathContainer[path_id]['last_color'] = self.PRE_PATH_COLOR[color]
            except KeyError:
                self.pathContainer[path_id]['last_color'] = 'red'

            # On génère les dits boutons
            self.generateButtons(path_id)
        else:
            # On affiche directement le chemin
            self.writePath(P, size, color, self.CURRENT_LAYER)

            # On augmente la couche
            self.CURRENT_LAYER += 1

    def show(self):
        rows = len(list(self.pathContainer.keys()))
        self.pathTracer.grid(column = 1, row=rows, columnspan=3)
        self.canvas.grid(row = 0, column = 0, rowspan=(rows+1))

        self.window.mainloop()