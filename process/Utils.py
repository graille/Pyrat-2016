#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, time

def findPID(process_name):
    try:
        import subprocess

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
    except ImportError:
        raise Exception("Erreur d'importation")

def main(arg):
    pid = os.getpid()
    pids = findPID("python")
    pid_core = findPID("pyrat_core")

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
        parameter = 30
        pids_temp = pids.copy()

        npt = pids_temp.copy()
        for elt in npt:
            if elt[0] <= pid_core or elt[0] == pid:
                pids_temp.remove(elt)

        pids_temp.sort()

        pid_op = pids_temp[0][0]
        print(pid_op)
    else:
        pass

    if arg == 'P':
        pause(pid_op)
    else:
        restart(pid_op)

def pause(pid):
    print("Pause " + str(pid))
    os.popen(["kill", "-TSTP " + str(pid)])

def restart(pid):
    print("Continue " + str(pid))
    os.popen(["kill", "-CONT " + str(pid)])

def init():
    pass

def doSomething(turn):
    try:
        if turn % 2 == 0:
            main('P')
        else:
            main('C')
    except Exception:
        pass
