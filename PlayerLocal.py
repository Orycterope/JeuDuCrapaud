__author__ = 'thomas'
import pygame
import sys
from pygame.locals import *
import time

class PlayerLocal:
    
    def __init__(self, controlleur):
        self.controlleur = controlleur
        
    
    def waitForPlay(self):

        timedebut = time.time()
        continuer = True
        while continuer and not self.controlleur.fenetre.closing:
            for event in pygame.event.get():
                if time.time() < timedebut + 0.1: #On laisse un 10e de seconde pour etre sûr de pas récupérer les events du tour d'avant pcq pygame est pas synchrone
                    continue
                if event.type == QUIT:
                    self.controlleur.fenetre.fermer()
                elif event.type == KEYDOWN:
                    if event.key == K_KP1:
                        moveLetter = 'F'
                        continuer = False
                        break
                    if event.key == K_KP2:
                        moveLetter = 'E'
                        continuer = False
                        break
                    if event.key == K_KP3:
                        moveLetter = 'D'
                        continuer = False
                        break
                    if event.key == K_KP4:
                        moveLetter = 'G'
                        continuer = False
                        break
                    if event.key == K_KP6:
                        moveLetter = 'C'
                        continuer = False
                        break
                    if event.key == K_KP7:
                        moveLetter = 'H'
                        continuer = False
                        break
                    if event.key == K_KP8:
                        moveLetter = 'A'
                        continuer = False
                        break
                    if event.key == K_KP9:
                        moveLetter = 'B'
                        continuer = False
                        break
                    if event.key == K_z:
                        moveLetter = 'Z'
                        continuer = False
                        break
                    if event.key == K_SPACE:
                        self.controlleur.fenetre.toggleMusic()

        return moveLetter

    def informMove(self, lettre):

        pass