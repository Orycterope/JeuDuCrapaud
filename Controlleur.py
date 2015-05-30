__author__ = 'thomas'

import PlayerLocal
import PlayerDistant
import PlayerIA
from Constantes import *
from random import randint

class Controlleur:

    def __init__(self, typeDePartie, fenetre):

        self.typeDePartie = typeDePartie
        self.fenetre = fenetre
        self.end = False
        # on génère le plateau
        self.plateau = [None] * LARGEUR_PLATEAU
        for i in range(0, LARGEUR_PLATEAU):
            self.plateau[i] = [None] * HAUTEUR_PLATEAU
            for j in range(0, HAUTEUR_PLATEAU):
                if (i + j) % 2 == 0:
                    self.plateau[i][j] = CASE_MOUVEMENT
                else:
                    self.plateau[i][j] = CASE_BOMB_EMPTY
        # on instancie les objets player
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
            self.joueur1 = PlayerLocal.PlayerLocal(self)
            self.joueur2 = PlayerIA.PlayerIA(self)
        # on détermine celui qui commence
        self.tour = CRAPAUD_1
        self.tourPlayer = self.joueur1
        #on place les joueurs sur le plateau
        self.plateau[SPAWN_1[0]][SPAWN_1[1]] = CRAPAUD_1
        self.plateau[SPAWN_2[0]][SPAWN_2[1]] = CRAPAUD_2
        #on crée les bombes
        if typeDePartie != PARTIE_EN_LIGNE or fenetre.isServer: # c'est le toujours le serveur qui génère les bombes
            bombcount = 0
            while bombcount < BOMB_AMOUNT: # on place les bombes aléatoirement en parcourant le plateau case par case, plusieurs fois si il faut
                for i in range(0, LARGEUR_PLATEAU):
                    for j in range(0, HAUTEUR_PLATEAU):
                        if self.plateau[i][j] == CASE_BOMB_EMPTY:
                            if randint(1, 100) == 42 and bombcount < BOMB_AMOUNT:
                                self.plateau[i][j] = CASE_BOMB
                                if typeDePartie == PARTIE_EN_LIGNE:
                                    self.joueur2.sendBomb([i, j])
                                bombcount +=1
        else:
            bombs = self.joueur1.receiveBombs()
            for i in range(len(bombs)):
                self.plateau[bombs[i][0]][bombs[i][1]] = CASE_BOMB
        # on lance la phase d'affichage des bombes
        self.fenetre.displayBombPosition(self.plateau)
        self.fenetre.refresh(self.plateau)
        # on joue :)
        while not self.end:
            if self.fenetre.closing:
                return
            self.faireJouer()
        
        fenetre.afficheMenuVictoire(self.tour)

    def faireJouer(self):
        if self.checkLose():
            return
        hasPlayed = False
        while hasPlayed != True:
            moveAttemptLetter = self.tourPlayer.waitForPlay()
            if moveAttemptLetter == "Z":
                return
            moveAttempt = MOVECODE[moveAttemptLetter]
            if self.checkMoveAllowed(moveAttempt) == True:
                self.move(self.tour, moveAttempt[0], moveAttempt[1])
                if self.isNextToBomb(self.tour) != False:
                    self.kill(self.tour, self.isNextToBomb(self.tour))
                self.informOtherPlayer(moveAttemptLetter)
                hasPlayed = True
                if self.checkLose():
                    return
        self.changeTour()

    def move(self, crapaud, dx, dy):

        coord = self.getCoordCrapaud(crapaud)

        if crapaud == CRAPAUD_1:
            self.plateau[coord[0]][coord[1]] = CASE_BAVE_1
        else:
            self.plateau[coord[0]][coord[1]] = CASE_BAVE_2
        self.plateau[coord[0]+dx][coord[1]+dy] = crapaud
        self.fenetre.refresh(self.plateau)

    def getCoordCrapaud(self, crapaud):

        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                if self.plateau[i][j] == crapaud:
                    return [i, j]

    def getCaseContent(self, coord):
        if not 0 <= coord[0] < LARGEUR_PLATEAU:
            return False
        elif not 0 <= coord[1] < HAUTEUR_PLATEAU:
            return False
        else:
          return self.plateau[coord[0]][coord[1]]

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

    def isNextToBomb(self, crapaud):
        coord = self.getCoordCrapaud(crapaud)
        x = coord[0]
        y = coord[1]
        if self.getCaseContent([x,y + 1]) == CASE_BOMB:
            return [x,y + 1]
        elif self.getCaseContent([x,y - 1]) == CASE_BOMB :
            return [x,y - 1]
        elif self.getCaseContent([x + 1,y]) == CASE_BOMB :
            return [x + 1,y]
        elif self.getCaseContent([x - 1,y]) == CASE_BOMB :
            return [x - 1,y]
        else:
            return False

    def kill(self, crapaud, bombCoord):
        if crapaud == CRAPAUD_1:
            bave = CASE_BAVE_1
            spawn = SPAWN_1
        else:
            bave = CASE_BAVE_2
            spawn = SPAWN_2

        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                if self.plateau[i][j] == crapaud or self.plateau[i][j] == bave:
                    self.plateau[i][j] = CASE_MOUVEMENT

        self.plateau[spawn[0]][spawn[1]] = crapaud
        self.plateau[bombCoord[0]][bombCoord[1]] = CASE_EXPLOSION
        self.fenetre.refresh(self.plateau)

    def changeTour(self):
        if self.tour == CRAPAUD_1:
            self.tourPlayer = self.joueur2
            self.tour = CRAPAUD_2
        else:
            self.tourPlayer = self.joueur1
            self.tour = CRAPAUD_1

    def informOtherPlayer(self, lettre):
        if self.tour == CRAPAUD_1:
            self.joueur2.informMove(lettre)
        else:
            self.joueur1.informMove(lettre)
            
    def listMoves(self):
        moves = list()
        
        for letter, move in MOVECODE.items():
            if self.checkMoveAllowed(move):
                moves.append(letter)
            
        return moves
    
    def canMove(self):
        return len(self.listMoves()) != 0
    
    def checkLose(self):
        if self.canMove() == False:
            self.end = True
            return True
        return False