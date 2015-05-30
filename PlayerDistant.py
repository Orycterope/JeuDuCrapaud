__author__ = 'thomas'
import pygame
import sys
import socket
from pygame.locals import *
from Constantes import *

class PlayerDistant:

    def __init__(self, controlleur, connexion):
        self.controlleur = controlleur
        self.connexion = connexion


    def waitForPlay(self):

        lettre = self.connexion.recv(1).decode('ascii')

        if lettre.upper() == "Z" or lettre == "":
            print("Connexion fermée par le programme distant")
            self.controlleur.fenetre.fermer()
        return lettre

    def informMove(self, lettre):

        self.connexion.send(lettre.encode('ascii'))


    def sendBomb(self, bombLocation):
        for i in range(0,2):
            code = str(bombLocation[i]) #on envoit le nombre en caractère ascii pcq envoyer un int brut ne marche pas -_-
            if bombLocation[i] < 10: # on envoit toujours deux caractères
                code = '0' + code
            self.connexion.send(code.encode('ascii'))



    def receiveBombs(self):
        bombCounter = 0
        bombs = [None] * BOMB_AMOUNT
        for i in range(0, BOMB_AMOUNT):
            bombs[i] = [None] * 2
            for j in range(0,2):
                coord = int(self.connexion.recv(2).decode('ascii'))
                if coord == "":
                    print("Connexion fermée par le programme distant")
                    self.controlleur.fenetre.fermer()
                else:
                    bombs[i][j] = coord

        return bombs