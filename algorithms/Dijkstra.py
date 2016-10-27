# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 18:07:45 2016

@author: Thibault/Clément
"""

import numpy as np
import heapq


class PriorityQueue(object):
    def __init__(self, heap = []):
        heapq.heapify(heap)
        self.heap = heap

    def insert(self, node, priority = 0):
        heapq.heappush(self.heap, (priority, node))

    def pop(self):
        return heapq.heappop(self.heap)[1]

class Dijkstra:
    def __init__(self, maze, origin = None, goal = None):
        self.graph = maze
        self.setOrigin(origin)
        self.setGoal(goal)

    def setOrigin(self, n):
        if n:
            self.origin = n

    def setGoal(self, n):
        if isinstance(n, list):
            self.goal = n.copy()
        else:
            self.goal = n

    def clear(self):
        self.pathArray = {}
        self.dist = {}
        self.Q = PriorityQueue()

        self.dist[self.origin] = 0

        for node in self.graph.nodes:
            if node != self.origin:
                self.pathArray[node] = None
                self.dist[node] = np.inf

        self.Q.insert(self.origin, self.dist[self.origin])

    def process(self):
        self.algorithm()

    def algorithm(self):
        if self.origin != self.goal:
            self.clear()

            while self.Q.heap:
                u = self.Q.pop()
                for v in self.graph.getNeighbors(u):
                    alt = self.dist[u] + self.graph.getDistance(u, v)
                    if alt < self.dist[v]:
                        self.dist[v] = alt
                        self.pathArray[v] = u
                        self.Q.insert(v, alt)
        else:
            pass

    def reconstructPath(self, node):
        #litteral_path = ""
        total_distance = 0
        current = node
        real_path = []
        while current != self.origin:
            new = self.pathArray[current]

            #litteral_path += self.graph.getMove(new, current)
            total_distance += self.graph.getDistance(current, new)
            real_path.append(current)

            current = new

        real_path.append(current)
        return (total_distance, real_path[::-1])

    def getResult(self, node = None):
        if self.goal != self.origin:
            if (not node) and (self.goal):
                return self.reconstructPath(self.goal)
            else:
                return self.reconstructPath(node)
        else:
            return (0, [])