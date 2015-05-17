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
        print("sending :")
        for i in range(0,2):
            code = str(bombLocation[i])
            if bombLocation[i] < 10:
                code = '0' + code
            self.connexion.send(code.encode('ascii'))
            print(" -"+str(i)+": " + code)



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
            print("bomb " + str(i) + " :\n -x: " + str(bombs[i][0]) + "\n -y: " + str(bombs[i][1]))

        return bombs