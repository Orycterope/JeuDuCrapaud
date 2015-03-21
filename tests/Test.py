# -*- coding: utf8 -*-

'''
Created on 26 févr. 2015

@author: Anis
'''

import pygame
from pygame.locals import *

def move():
    global position_perso
    position_perso = position_perso.move(-1, 0)

def refresh():
    fenetre.blit(fond, (0,0))   
    fenetre.blit(perso, position_perso)
    pygame.display.flip()

print("Hello World!")

pygame.init()
pygame.key.set_repeat(1, 1)
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
            if event.key == K_UP:
                position_perso = position_perso.move(0, -1)
                refresh()
            if event.key == K_DOWN:
                position_perso = position_perso.move(0, 1)
                refresh()
            if event.key == K_LEFT:
                position_perso = position_perso.move(-1, 0)
                refresh()
            if event.key == K_RIGHT:
                position_perso = position_perso.move(1, 0)
                refresh()