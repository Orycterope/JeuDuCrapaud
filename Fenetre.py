import pygame
from Constantes import *
from Controlleur import *
from pygame.locals import *


class Fenetre:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

        self.afficheMenuPricipal()


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


    def refreshMenu(self, hlBlock):

        self.fenetre.blit(self.bgmenu, (10,10))
        pass

    def afficheMenuPricipal(self):

        pygame.mixer.music.load("res/alex-f.mp3")
        pygame.mixer.music.play(-1)
        self.bgmenu = pygame.image.load("res/bgmenu.jpg").convert()

        continuer = True
        highlightedBlock = 2
        while continuer == True:
            self.refreshMenu(highlightedBlock)
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.fermer()
                if e.type == KEYDOWN:
                    if e.key == K_KP4 or e.key == K_LEFT:
                        highlightedBlock = (highlightedBlock - 1) % 3
                    if e.key == K_KP6 or e.key == K_RIGHT:
                        highlightedBlock = (highlightedBlock + 1) % 3
                    if e.key == K_KP_ENTER or e.key == K_RETURN:
                        print("enter")
                        continuer = False

        self.lancePartie(highlightedBlock)

    def lancePartie(self, typePartie):

        pygame.mixer.music.load("res/popcorn.mp3")
        pygame.mixer.music.play(-1) # param -1 fait répéter à l'infini.

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
