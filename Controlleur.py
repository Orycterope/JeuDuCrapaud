__author__ = 'thomas'

import PlayerLocal
import PlayerDistant
from Constantes import *

class Controlleur:

    def __init__(self, typeDePartie, fenetre):

        self.typeDePartie = typeDePartie
        self.fenetre = fenetre
        self.plateau = [None] * LARGEUR_PLATEAU

        for i in range(0, LARGEUR_PLATEAU):
            self.plateau[i] = [None] * HAUTEUR_PLATEAU
            for j in range(0, HAUTEUR_PLATEAU):
                if (i + j) % 2 == 0:
                    self.plateau[i][j] = CASE_MOUVEMENT
                else:
                    self.plateau[i][j] = CASE_POINT_EMPTY


        if typeDePartie == PARTIE_DUO:
            self.joueur1 = PlayerLocal.PlayerLocal(self)
            self.joueur2 = PlayerLocal.PlayerLocal(self)
        elif typeDePartie == PARTIE_EN_LIGNE:
            if fenetre.isServer:
                self.joueur1 = PlayerLocal.PlayerLocal(self)
                self.joueur2 = PlayerDistant.PlayerDistant(self, self.fenetre.connexion)
            else:
                self.joueur2 = PlayerLocal.PlayerLocal(self)
                self.joueur1 = PlayerDistant.PlayerDistant(self, self.fenetre.connexion)
        else:
            pass

        self.tour = CRAPAUD_1
        self.tourPlayer = self.joueur1

        self.plateau[0][0] = CRAPAUD_1
        self.plateau[10][10] = CRAPAUD_2
        self.fenetre.refresh(self.plateau)

        while True:
            self.faireJouer()


    def getCoordCrapaud(self, crapaud):
        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                if self.plateau[i][j] == crapaud:
                    return [i, j]

    def faireJouer(self):
        hasPlayed = False
        while hasPlayed != True:
            moveAttemptLetter = self.tourPlayer.waitForPlay()
            moveAttempt = MOVECODE[moveAttemptLetter]
            if self.checkMoveAllowed(moveAttempt) == True:
                self.move(self.tour, moveAttempt[0], moveAttempt[1])
                self.joueur1.informMove(moveAttemptLetter)
                self.joueur2.informMove(moveAttemptLetter)
                hasPlayed = True
        self.changeTour()

    def changeTour(self):
        if self.tour == CRAPAUD_1:
            self.tourPlayer = self.joueur2
            self.tour = CRAPAUD_2
        else:
            self.tourPlayer = self.joueur1
            self.tour = CRAPAUD_1

    def move(self, crapaud, dx, dy):

        coord = self.getCoordCrapaud(crapaud)
        self.plateau[coord[0]][coord[1]] = CASE_BAVE
        self.plateau[coord[0]+dx][coord[1]+dy] = crapaud
        self.fenetre.refresh(self.plateau)


    def checkMoveAllowed(self, moveAttempt):
        dx = moveAttempt[0]
        dy = moveAttempt[1]
        coord = self.getCoordCrapaud(self.tour)
        x = coord[0] + dx
        y = coord[1] + dy
        if x < 0:
            return False
        if y < 0:
            return False
        if y >= HAUTEUR_PLATEAU:
            return False
        if x >= LARGEUR_PLATEAU:
            return False
        if self.plateau[x][y] != CASE_MOUVEMENT:
            return False

        return True