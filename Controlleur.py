__author__ = 'thomas'

import PlayerLocal
from Constantes import *

class Controlleur:

    def __init__(self, typeDePartie, fenetre):

        self.typeDePartie = typeDePartie
        self.fenetre = fenetre
        self.plateau = [None] * LARGEUR_PLATEAU

        for i in range(0, LARGEUR_PLATEAU):
            self.plateau[i] = [None] * HAUTEUR_PLATEAU
            for j in range(0, HAUTEUR_PLATEAU):
                if (i + j)%2 == 0:
                    self.plateau[i][j] = CASE_MOUVEMENT
                else:
                    self.plateau[i][j] = CASE_POINT_EMPTY

        self.joueur1 = PlayerLocal.PlayerLocal(self)
        if typeDePartie == PARTIE_DUO:
            self.joueur2 = PlayerLocal.PlayerLocal(self)
            self.tour = 1
            self.tourPlayer = self.joueur1
        else:
            pass

        self.joueur1.position = [0,0]
        self.joueur2.position = [20,20]

        while True:
            self.faireJouer()


    def faireJouer(self):
        hasPlayed = False
        while hasPlayed != True:
            moveAttempt = self.tourPlayer.waitForPlay()
            if self.checkMoveAllowed(moveAttempt) == True:
                self.tourPlayer.position[0] += moveAttempt[0]
                self.tourPlayer.position[1] += moveAttempt[1]
                self.fenetre.move(self.tour, moveAttempt[0], moveAttempt[1])
                hasPlayed = True
        self.changeTour()

    def changeTour(self):
        if self.tour == CRAPAUD_1:
            self.tourPlayer = self.joueur2
            self.tour = CRAPAUD_2
        else:
            self.tourPlayer = self.joueur1
            self.tour = CRAPAUD_1

    def checkMoveAllowed(self, moveAttempt):
        x = moveAttempt[0]
        y = moveAttempt[1]
        return True