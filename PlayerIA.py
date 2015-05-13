__author__ = 'Anis'

import time
from random import randint

class PlayerIA:
    
    def __init__(self, controlleur):
        self.controlleur = controlleur
        
    
    def waitForPlay(self):
        time.sleep(.3)
        
        moves = self.controlleur.listMoves()
        
        return moves[randint(0, len(moves) - 1)]

    def informMove(self, lettre):

        pass