__author__ = 'thomas'
import pygame
from pygame.locals import *

class PlayerLocal:
    
    def __init__(self, controlleur):
        return
        
    
    def waitForPlay(self):
        
        move = [0, 0]
        continuer = True
        while continuer:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continuer = False
                elif event.type == KEYDOWN:
                    if event.key == K_KP1:
                        move = [-1, 1]
                    if event.key == K_KP2:
                        move = [0, 2]
                    if event.key == K_KP3:
                        move = [1, 1]
                    if event.key == K_KP4:
                        move = [-2, 0]
                    if event.key == K_KP6:
                        move = [2, 0]
                    if event.key == K_KP7:
                        move = [-1, -1]
                    if event.key == K_KP8:
                        move = [0, -2]
                    if event.key == K_KP9:
                        move = [1, -1]
        return move