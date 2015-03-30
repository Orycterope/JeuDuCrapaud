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

    def refresh(self, plateau):

        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                case = plateau[i][j]
                if case == CASE_MOUVEMENT:
                    self.fenetre.blit(self.fond1, (i * 32, j * 32))
                elif case == CASE_BAVE:
                    self.fenetre.blit(self.fond1, (i * 32, j * 32))
                    self.fenetre.blit(self.bave, (i * 32, j * 32))
                elif case == CRAPAUD_1:
                    self.fenetre.blit(self.fond1, (i * 32, j * 32))
                    self.fenetre.blit(self.perso1,(i * 32, j * 32))
                elif case == CRAPAUD_2:
                    self.fenetre.blit(self.fond1, (i * 32, j * 32))
                    self.fenetre.blit(self.perso2,(i * 32, j * 32))
                elif case == CASE_POINT_EMPTY:
                    self.fenetre.blit(self.fond2, (i * 32, j * 32))
                elif case == CASE_POINT_GAINED:
                    pass
                    #pointIcone
        pygame.display.flip()


    def afficheMenuPricipal(self):
        pass

    def lancePartie(self, typePartie):

        self.fond1 = pygame.image.load("res/background.png").convert()
        self.fond2 = pygame.image.load("res/background2.png").convert()
        self.perso1 = pygame.image.load("res/perso.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso2.png").convert_alpha()
        self.bave = pygame.image.load("res/goutte.png").convert_alpha()
        self.position_perso1 = self.perso1.get_rect()
        self.position_perso2 = self.perso2.get_rect()
        Controlleur(typePartie, self)

    def fermer(self):
        pygame.quit()




#Main
fen = Fenetre()
