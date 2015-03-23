import pygame
from Constantes import *
from Controlleur import *

class Fenetre:


    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

        #TODO : afficher le menu principal et lancer la partie en conséquence

        self.lancePartie(PARTIE_DUO)


    def refreshBackground(self):
        for i in range (0, LARGEUR_FENETRE // 32):
            for j in range (0, HAUTEUR_FENETRE // 32):
                if (i + j)%2 == 0:
                    self.fenetre.blit(self.fond1, (i * 32, j * 32))
                else:
                    self.fenetre.blit(self.fond2, (i * 32, j * 32))

    def refresh(self):
        self.refreshBackground()
        self.fenetre.blit(self.perso1, self.position_perso1)
        self.fenetre.blit(self.perso2, self.position_perso2)
        pygame.display.flip()

    def move(self, crapaud, x, y):

        if crapaud == CRAPAUD_1:
            self.position_perso1 = self.position_perso1.move(x * 32, y * 32)
        else:
            self.position_perso2 = self.position_perso2.move(x * 32, y * 32)
        self.refresh()

    def afficheMenuPricipal(self):
        pass

    def lancePartie(self, typePartie):

        self.fond1 = pygame.image.load("res/background.png").convert()
        self.fond2 = pygame.image.load("res/background2.png").convert()
        self.perso1 = pygame.image.load("res/perso.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso2.png").convert_alpha()
        self.position_perso1 = self.perso1.get_rect()
        self.position_perso2 = self.perso2.get_rect()
        self.move(CRAPAUD_1, 3, 3)
        self.move(CRAPAUD_2, 10, 10)
        Controlleur(typePartie, self)

    def fermer(self):
        pygame.quit()




#Main
fen = Fenetre()
