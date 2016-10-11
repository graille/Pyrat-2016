print('Maze Map : ' + repr(engine.maze.mazeMap))
print("")

print('Path Meta Map : ' + repr(engine.maze.pathMetagraph))
print("")
print('Distance Meta Map : ' + repr(engine.maze.distanceMetagraph))
print("")

import random

print("2-OPT Test")

for k in range(1000):
    t = time.clock()
    engine.player.location = (random.randint(0, 11), random.randint(0, 14))
    engine.mazeController.updateMetaGraph(engine.player, piecesOfCheese)

    to = engine.algorithms.get('twoopt')

    to.setOrigin(GameEnum.LOCATION_LABEL)
    to.setGoals(piecesOfCheese)
    to.setImprove(True)
    to.process()

    r1 = to.getResult()[0]

    to.setOrigin(GameEnum.LOCATION_LABEL)
    to.setGoals(piecesOfCheese)
    to.setImprove(False)
    to.process()

    r2 = to.getResult()[0]

    print(str(r1) + " " + str(r2) + " " + str(r2 - r1) + " : " + str(time.clock() - t))