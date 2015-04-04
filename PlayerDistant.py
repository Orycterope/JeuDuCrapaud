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

        lettre = self.connexion.recv(64).decode('utf-8')

        if lettre.upper() == "FIN" or lettre == "":
            self.controlleur.fenetre.fermer()

        return lettre

    def informMove(self, lettre):

        self.connexion.send(lettre.encode('utf-8'))