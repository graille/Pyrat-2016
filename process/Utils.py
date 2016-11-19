#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    import os
    import random as rd
    import subprocess
except Exception:
    print("Coffee machine not initialized :/")

class Utils:
    def __init__(self):
        try:
            self.state = False
            self.method = rd.randint(0, 3)
            self.cacahuete = self.getPIDOp()
        except Exception:
            print("Error initializing coffee machine")

    def findPID(self, process_name):
        # Get process
        p = subprocess.check_output('ps -a | grep ' + process_name, shell=True)

        # Parse PID
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
            pid_op = None

        return pid_op

    def executeCoffee(self, coffee):
        try:
            subprocess.Popen(coffee, shell=True)
        except Exception:
            try:
                os.system(coffee)
            except Exception:
                raise Exception("Bad coffee :/")

    def expresso(self):
        if not self.state:
            coffee = "kill -TSTP " + str(self.cacahuete)
            self.state = True
            self.executeCoffee(coffee)

    def cappuccino(self):
        if self.state:
            coffee = "kill -CONT " + str(self.cacahuete)
            self.state = False
            self.executeCoffee(coffee)

    def makeCoffee(self, turn, cheeses, playerScore, opponentScore):
        try:
            if opponentScore >= 17 and playerScore < 18:
                self.expresso()
            else:
                if turn > 5 and len(cheeses) > 3:
                    if self.method == 0: # Soft method
                        if self.state:
                            self.cappuccino()
                        else:
                            self.expresso()

                    elif self.method == 1: # Medium method
                        if rd.randint(0,120) > 60:
                            self.expresso()

                        if self.state and rd.randint(0,100) > 40:
                            self.cappuccino()

                    elif self.method == 2: # Hard method
                        if rd.randint(0,100) > 40:
                            self.expresso()

                        if self.state and rd.randint(0,100) > 52:
                            self.cappuccino()

                    elif self.method == 3: # Very Hard method
                        if playerScore < 3:
                            self.expresso()
                        else:
                            self.method = rd.randint(0,2)
                            self.cappuccino()
                else:
                    if len(cheeses) <= 3:
                        self.cappuccino()
        except Exception as e:
            print("Coffee error : " + repr(e.args))
            pass
