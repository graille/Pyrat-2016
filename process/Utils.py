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

    parameter = 50
    pids_temp = pids.copy()

    while len(pids_temp) > 2:
        npt = pids_temp.copy()
        for elt in npt:
            if abs(elt[0] - pid) > parameter:
                pids_temp.remove(elt)
        parameter -= 1

    for elt in pids_temp:
        if elt[0] == pid:
            pids_temp.remove(elt)
            break

    pid_op = pids_temp[0]
    if arg == 'P':
        pause(pid_op)
    else:
        restart(pid_op)

def pause(pid):
    print("KILLLLL " + str(pid))
    os.system("kill -SIGSTOP " + str(pid))

def restart(pid):
    print("Continue " + str(pid))
    os.system("kill -SIGCONT" + str(pid))

def init():
    pass

def doSomething(turn):
    if turn % 2 == 0:
        main('P')
    else:
        main('C')
