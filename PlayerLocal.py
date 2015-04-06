__author__ = 'thomas'
import pygame
import sys
from pygame.locals import *
import time

class PlayerLocal:
    
    def __init__(self, controlleur):
        self.controlleur = controlleur
        self.queue = self.controlleur.fenetre.eventQueue
        
    
    def waitForPlay(self):

        timedebut = time.time()
        self.queue.empty()
        while True and not self.controlleur.fenetre.closing:
            event = self.queue.get()
            if time.time() < timedebut + 0.1: #On laisse un 10e de seconde pour etre sûr de pas récupérer les events du tour d'avant pcq pygame est pas synchrone
                continue
            if event.type == QUIT:
               self.controlleur.fenetre.fermer()
            elif event.type == KEYDOWN:
                if event.key == K_KP1:
                    moveLetter = 'F'
                    break
                if event.key == K_KP2:
                    moveLetter = 'E'
                    break
                if event.key == K_KP3:
                    moveLetter = 'D'
                    break
                if event.key == K_KP4:
                    moveLetter = 'G'
                    break
                if event.key == K_KP6:
                    moveLetter = 'C'
                    break
                if event.key == K_KP7:
                    moveLetter = 'H'
                    break
                if event.key == K_KP8:
                    moveLetter = 'A'
                    break
                if event.key == K_KP9:
                    moveLetter = 'B'
                    break
                if event.key == K_z:
                    moveLetter = 'Z'
                    break

        return moveLetter

    def informMove(self, lettre):

        pass