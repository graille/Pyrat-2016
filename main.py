#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###################################################################################################################################################################################################################################
############################################# PRE-DEFINED CONSTANTS ############################################# ############################################ CONSTANTES PRÉ-DÉFINIES ############################################
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    In this section, you will find some pre-defined constants that are needed for the game                      #    Dans cette section, vous trouvez des constantes pré-définies nécessaires pour la partie                     #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################
#                                                                                                                #                                                                                                                #
#    TEAM_NAME : string                                                                                          #    TEAM_NAME : string                                                                                          #
#    ------------------                                                                                          #    ------------------                                                                                          #
#                                                                                                                #                                                                                                                #
#        This constant represents your name as a team                                                            #        Cette constante représente le nom de votre équipe                                                       #
#        Please change the default value to a string of your choice                                              #        Veuillez en changer la valeur par une chaîne de caractères de votre choix                               #
#                                                                                                                #                                                                                                                #
#    MOVE_XXX : char                                                                                             #    MOVE_XXX : char                                                                                             #
#    ---------------                                                                                             #    ---------------                                                                                             #
#                                                                                                                #                                                                                                                #
#        The four MOVE_XXX constants represent the possible directions where to move                             #        Les quatre constantes MOVE_XXX représentent les directions possibles où se déplacer                     #
#        The "turn" function should always return one of these constants                                         #        La fonction "turn" doit toujours renvoyer l'une d'entre elles                                           #
#        Please do not edit them (any other value will be considered incorrect and thus ignored)                 #        Merci de ne pas les éditer (toute autre valeur sera considérée comme incorrecte et sera ignorée)        #
#                                                                                                                #                                                                                                                #
###################################################################################################################################################################################################################################

TEAM_NAME = "DreamTeam"

MOVE_DOWN = 'D'
MOVE_LEFT = 'L'
MOVE_RIGHT = 'R'
MOVE_UP = 'U'

class Maze():
    def __init__(location):
        self.location = location
    def canMove(this, mazeMap, dest):
        pass
        
class Graph():
    def __init__(mazeMap):
        pass
    def convertToMatrix(mazeMap):
        return matrixMap



def preprocessing (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, piecesOfCheese, timeAllowed) :
    print("<b>[mazeMap]</b> " + repr(mazeMap))
    print("<b>[mazeWidth]</b> " + repr(mazeWidth))
    print("<b>[mazeHeight]</b> " + repr(mazeHeight))
    print("<b>[playerLocation]</b> " + repr(playerLocation))
    print("<b>[opponentLocation]</b> " + repr(opponentLocation))
    print("<b>[piecesOfCheese]</b> " + repr(piecesOfCheese))
    print("<b>[timeAllowed]</b> " + repr(timeAllowed))

def turn (mazeMap, mazeWidth, mazeHeight, playerLocation, opponentLocation, playerScore, opponentScore, piecesOfCheese, timeAllowed) :
    
    # Example print that appears in the shell at every turn
    print("Move: [" + MOVE_UP + "]")
    
    # We always go up
    return MOVE_UP

###################################################################################################################################################################################################################################
###################################################################################################################################################################################################################################