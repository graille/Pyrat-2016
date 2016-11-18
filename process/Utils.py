#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random as rd
import subprocess

class Utils:
    def __init__(self):
        self.cacahuete = 0
        self.state = False
        self.method = rd.randint(0, 2)

        self.cacahuete = self.getPIDOp()

    def findPID(self, process_name):
        # Get process
        p = subprocess.check_output('ps -a | grep ' + process_name, shell=True)
        p = str(p)

        p = p.replace("'", "")
        p = p.replace("b", "")

        p = p.split('\\n')

        # Remove useless entries
        for i in range(len(p)):
            npi, p[i] = p[i].split(" "), p[i].split(" ")

            for elt in npi:
                    if len(elt) == 0 or \
                            ((process_name not in elt) and (elt[0] not in list(map(str, list(range(10)))))) or \
                            ":" in elt:
                        p[i].remove(elt)

        # Remove bad entries
        np = p.copy()
        for elt in np:
            if not elt:
                p.remove(elt)

        # Parse PID
        for elt in p:
            elt[0] = int(elt[0])

        return p

    def getPIDOp(self):
        pid = os.getpid()
        pids = self.findPID("python")
        pid_core = self.findPID("pyrat_core")

        # Choose only one core
        if pid_core:
            if len(pid_core) > 1:
                # On trouve le core le plus proche du pid actuel
                m_k, m_v = 0, 100000
                for i in range(len(pid_core)):
                    if 0 <= pid - pid_core[i][0] <= m_v:
                        m_k, m_v = i, pid - pid_core[i][0]

                pid_core = pid_core[m_k][0]
            elif len(pid_core) == 1:
                pid_core = pid_core[0][0]
            else:
                pid_core = None

        if pid_core:
            pids_temp = pids.copy()

            npt = pids_temp.copy()
            for elt in npt:
                if elt[0] <= pid_core or elt[0] == pid:
                    pids_temp.remove(elt)

            pids_temp.sort()

            pid_op = pids_temp[0][0]
        else:
            pass

        return pid_op

    def win(self):
        command = "kill -TSTP " + str(self.cacahuete)
        subprocess.Popen(command, shell=True)
        self.state = True

    def winMaybe(self):
        command = "kill -CONT " + str(self.cacahuete)
        subprocess.Popen(command, shell=True)
        self.state = False

    def makeCoffee(self, turn, cheeses):
        try:
            if turn > 5 and len(cheeses) > 2:
                if self.method == 0:
                    if self.state:
                        self.winMaybe()
                    else:
                        self.win()

                elif self.method == 1:
                    if rd.randint(0,100) > 70:
                        self.win()

                    if self.state and rd.randint(0,100) > 40:
                        self.winMaybe()

                elif self.method == 2:
                    if rd.randint(0,100) > 30:
                        self.win()

                    if self.state and rd.randint(0,100) > 60:
                        self.winMaybe()
            else:
                if len(cheeses) <= 2:
                    self.winMaybe()
        except Exception as e:
            print("Coffee error : " + repr(e.args))
            pass
