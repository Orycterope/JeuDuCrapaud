# -*- coding: utf8 -*-

'''
Created on 26 févr. 2015

@author: Anis
'''

import pygame
from pygame.locals import *

def move(x, y):
    global position_perso
    position_perso = position_perso.move(x * 16, y * 16)
    refresh()

def refresh():
    fenetre.blit(fond, (0,0))   
    fenetre.blit(perso, position_perso)
    pygame.display.flip()

print("Hello World!")

pygame.init()
#pygame.key.set_repeat(1, 1)
pygame.display.set_caption('Tests')
fenetre = pygame.display.set_mode((640, 480))

fond = pygame.image.load("background.jpg").convert()
fenetre.blit(fond, (0,0))

perso = pygame.image.load("perso.png").convert_alpha()
position_perso = perso.get_rect()
position_perso = position_perso.move(300, 200)
fenetre.blit(perso, position_perso)

pygame.display.flip()

# Boucle des évènements
continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = False
        elif event.type == KEYDOWN:
            if event.key == K_KP1:
                move(-1, 1)
            if event.key == K_KP2:
                move(0, 2)
            if event.key == K_KP3:
                move(1, 1)
            if event.key == K_KP4:
                move(-2, 0)
            if event.key == K_KP6:
                move(2, 0)
            if event.key == K_KP7:
                move(-1, -1)
            if event.key == K_KP8:
                move(0, -2)
            if event.key == K_KP9:
                move(1, -1)