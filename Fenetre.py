import pygame
import Constantes as C
import Controlleur

class Fenetre:


    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.fenetre = pygame.display.set_mode((C.LARGEUR_FENETRE, C.HAUTEUR_FENETRE))

        #TODO : afficher le menu principal et lancer la partie en conséquence

        self.lancePartie(C.PARTIE_DUO)


    def refreshBackground(self):
        for i in range (0, C.LARGEUR_FENETRE // 32):
            for j in range (0, C.HAUTEUR_FENETRE // 32):
                self.fenetre.blit(self.fond, (i * 32, j * 32))

    def refresh(self):
        self.refreshBackground()
        self.fenetre.blit(self.perso1, self.position_perso1)
        self.fenetre.blit(self.perso2, self.position_perso2)
        pygame.display.flip()

    def move(self, crapaud, x, y):

        if crapaud == C.CRAPAUD_1:
            self.position_perso1 = self.position_perso1.move(x * 32, y * 32)
        else:
            self.position_perso2 = self.position_perso2.move(x * 32, y * 32)
        self.refresh()

    def afficheMenuPricipal(self):
        pass

    def lancePartie(self, typePartie):

        self.fond = pygame.image.load("res/background.png").convert()
        self.perso1 = pygame.image.load("res/perso.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso.png").convert_alpha()
        self.position_perso1 = self.perso1.get_rect()
        self.position_perso2 = self.perso2.get_rect()
        self.move(C.CRAPAUD_1, 3, 3)
        self.move(C.CRAPAUD_2, 10, 10)
        Controlleur.Controlleur(typePartie, self)




#Main
fen = Fenetre()
