

def calculateFactors(maze, playerLocation, opponentLocation, nodes):
    a = BFS_P(maze)
    a.setNodes(nodes)
    a.setOrigin(playerLocation)
    a.process()

    playerWeight = a.nWeight

    a.setNodes(nodes)
    a.setOrigin(opponentLocation)
    a.process()

    opponentWeight = a.nWeight

    factors = {}

    for c in nodes:
        factors[c] = float(playerWeight[c] / opponentWeight[c])

    return factors


def returnUnderValue(factors, VAL_MAX):
    pass