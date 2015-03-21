__author__ = 'thomas'

import PlayerLocal
import Constantes as C

class Controlleur:

    def __init__(self, typeDePartie, fenetre):

        self.typeDePartie = typeDePartie
        self.fenetre = fenetre
        self.plateau = []

        self.joueur1 = PlayerLocal.PlayerLocal(self)
        if typeDePartie == C.PARTIE_DUO:
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
                self.fenetre.move(self.tour, self.tourPlayer.position[0], self.tourPlayer.position[1])
                hasPlayed = True
        self.changeTour()

    def changeTour(self):
        if self.tour == C.CRAPAUD_1:
            self.tourPlayer = self.joueur2
            self.tour = C.CRAPAUD_2
        else:
            self.tourPlayer = self.joueur1
            self.tour = C.CRAPAUD_1

    def checkMoveAllowed(self, moveAttempt):
        return True