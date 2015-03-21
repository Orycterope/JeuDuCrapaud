import pygame
import Constantes as C

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
        self.fenetre.blit(self.perso, self.position_perso)
        pygame.display.flip()

    def move(self, x, y):

        self.position_perso = self.position_perso.move(x * 32, y * 32)
        self.refresh()

    def afficheMenuPricipal(self):
        pass

    def lancePartie(self, typePartie):

        self.fond = pygame.image.load("res/background.png").convert()
        self.perso = pygame.image.load("res/perso.png").convert_alpha()
        self.position_perso = self.perso.get_rect()
        self.move(3, 3)
        while True:
            pass




#Main
fen = Fenetre()
