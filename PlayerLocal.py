__author__ = 'thomas'
import pygame
import sys
from pygame.locals import *

class PlayerLocal:
    
    def __init__(self, controlleur):
        self.controlleur = controlleur
        
    
    def waitForPlay(self):

        continuer = True
        pygame.event.clear()
        while continuer:
            for event in pygame.event.get():

                if event.type == QUIT:
                   self.controlleur.fenetre.fermer()
                elif event.type == KEYDOWN:
                    if event.key == K_KP1:
                        moveLetter = 'F'
                        continuer = False
                    if event.key == K_KP2:
                        moveLetter = 'E'
                        continuer = False
                    if event.key == K_KP3:
                        moveLetter = 'D'
                        continuer = False
                    if event.key == K_KP4:
                        moveLetter = 'G'
                        continuer = False
                    if event.key == K_KP6:
                        moveLetter = 'C'
                        continuer = False
                    if event.key == K_KP7:
                        moveLetter = 'H'
                        continuer = False
                    if event.key == K_KP8:
                        moveLetter = 'A'
                        continuer = False
                    if event.key == K_KP9:
                        moveLetter = 'B'
                        continuer = False

        return moveLetter

    def informMove(self, lettre):

        pass