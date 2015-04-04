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