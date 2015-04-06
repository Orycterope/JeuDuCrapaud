import pygame
import sys
from Constantes import *
from Controlleur import *
from pygame.locals import *
import socket
from queue import Queue
from EventThread import *


class Fenetre:

    def __init__(self):

        self.closing = False

        pygame.display.set_icon(pygame.image.load("res/kf.png"))

        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.connexion = None
        self.isServer = False # utilisé pour déterminer qui commence

        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

        self.eventQueue = Queue(maxsize=20)
        self.eventThread = EventThread(self, self.eventQueue)
        self.eventThread.setDaemon(True)
        self.eventThread.start()

        self.fond1 = pygame.image.load("res/background.png").convert_alpha()
        self.fond2 = pygame.image.load("res/background2.png").convert()
        self.perso1 = pygame.image.load("res/perso.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso2.png").convert_alpha()
        self.bave = pygame.image.load("res/goutte.png").convert_alpha()
        self.point = pygame.image.load("res/point.png").convert_alpha()
        self.bgmenu = pygame.image.load("res/bgmenu.png").convert_alpha()
        self.position_perso1 = self.perso1.get_rect()
        self.position_perso2 = self.perso2.get_rect()

        # on initialise le texte du menu ici parcequ'il est suuuuuuper looooong à rendre si on doit le faire à chaque refreshMenu().
        self.texts = ["Partie Solo", "Partie Duo", "Partie en ligne"]
        for i in range(3):
            myfont = pygame.font.SysFont("arial", 15) # une police sympa à proposer ?
            self.texts[i] = myfont.render(self.texts[i], 1, (i*100,0, 255/(i+1))) # le compteur génere les couleurs :)

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
                    self.fenetre.blit(self.fond2, (i * 32, j * 32))
                    self.fenetre.blit(self.point, (i * 32, j * 32))
        pygame.display.flip()


    def refreshMenuBackground(self):

        self.fenetre.blit(self.bgmenu, (0, 0))

        for i in range(3):

            x = (i + 1) * MARGE_BOUTON + i * TAILLE_HORIZONTALE_BOUTON
            y = HAUTEUR_BOUTON
            pygame.draw.rect (self.fenetre, (0, 255, 0), Rect(x,y, TAILLE_HORIZONTALE_BOUTON,TAILLE_VERTCALE_BOUTON), 0)

            text = self.texts[i]
            xt = int((TAILLE_HORIZONTALE_BOUTON - text.get_width()) / 2)
            yt = int((TAILLE_VERTCALE_BOUTON - text.get_height()) / 2)

            self.fenetre.blit(text, (x + xt, y + yt))

    def refreshMenu(self, hlBlock, oldHlBlock):
        y1 = HAUTEUR_BOUTON
        y2 = y1 + TAILLE_VERTCALE_BOUTON

        oldx1 = (oldHlBlock + 1) * MARGE_BOUTON + oldHlBlock * TAILLE_HORIZONTALE_BOUTON
        oldx2 = oldx1 + TAILLE_HORIZONTALE_BOUTON

        newx1 = (hlBlock + 1) * MARGE_BOUTON + hlBlock * TAILLE_HORIZONTALE_BOUTON
        newx2 = newx1 + TAILLE_HORIZONTALE_BOUTON

        if(oldx1 < newx1):
            sens = 1
        else:
            sens = -1

        while oldx1 != newx1:

            self.refreshMenuBackground()
            pygame.draw.lines(self.fenetre, (255,0,0), False, [(oldx1, y1), (oldx2, y1)], 2)
            pygame.draw.lines(self.fenetre, (0,0,255), False, [(oldx1,y1), (oldx1, y2)], 2)
            pygame.draw.lines(self.fenetre, (255,0,255), False, [(oldx1,y2), (oldx2, y2)], 2)
            pygame.draw.lines(self.fenetre, (255,255,0), False, [(oldx2,y1), (oldx2, y2)], 2)
            oldx1 += sens
            oldx2 += sens
            pygame.display.flip()

        # On le fait un dernière fois avec les valeurs finales pour que tout soit bien à la fin, notamment si on a refresh sans changer la place du curseur
        self.refreshMenuBackground()
        pygame.draw.lines(self.fenetre, (255,0,0), False, [(newx1, y1), (newx2, y1)], 2)
        pygame.draw.lines(self.fenetre, (0,0,255), False, [(newx1,y1), (newx1, y2)], 2)
        pygame.draw.lines(self.fenetre, (255,0,255), False, [(newx1,y2), (newx2, y2)], 2)
        pygame.draw.lines(self.fenetre, (255,255,0), False, [(newx2,y1), (newx2, y2)], 2)
        pygame.display.flip()




    def afficheMenuPricipal(self):

        pygame.mixer.music.load("res/alex-f.mp3") # Menu le plus electro au monde xD
        pygame.mixer.music.set_volume(0.6) # Sinon les oreilles saignent
        pygame.mixer.music.play(-1)



        continuer = True
        highlightedBlock = PARTIE_DUO # correspond au type de partie qui sera sélectionné
        oldHighlightedBlock = PARTIE_DUO # pour l'animation
        self.refreshMenu(highlightedBlock, oldHighlightedBlock)
        while True:
            e = self.eventQueue.get()
            if e.type == KEYDOWN:
                if e.key == K_KP4 or e.key == K_LEFT:
                    highlightedBlock = (highlightedBlock - 1) % 3
                if e.key == K_KP6 or e.key == K_RIGHT:
                    highlightedBlock = (highlightedBlock + 1) % 3
                if e.key == K_KP_ENTER or e.key == K_RETURN or e.key == K_z:
                    break
                self.refreshMenu(highlightedBlock, oldHighlightedBlock)
                oldHighlightedBlock = highlightedBlock


        if highlightedBlock == PARTIE_EN_LIGNE:
            self.afficheMenuMulti()

        if self.closing: #on vérifie qu'on est pas en train de quitter le jeu
            return

        self.lancePartie(highlightedBlock)

    def lancePartie(self, typePartie):

        pygame.mixer.music.load("res/popcorn.mp3")
        pygame.mixer.music.set_volume(1) # on remet le volume à donf
        pygame.mixer.music.play(-1) # param -1 fait répéter à l'infini.

        Controlleur(typePartie, self)


    def afficheMenuMulti(self):
        while True and not self.closing:
            e = self.eventQueue.get()
            if e.type == KEYDOWN:
                if e.key == K_s:
                    self.multiServeur()
                    break
                if e.key == K_c:
                    self.multiClient()
                    break
                if e.key == K_z:
                    break

    def multiServeur(self):

        self.isServer = True
        HOST = '192.168.1.28'

        # 1) création du socket :
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) liaison du socket à une adresse précise :
        try:
            mySocket.bind((HOST, PORT))
        except socket.error:
            print("La liaison du socket à l'adresse choisie a échoué.")
            sys.exit()
        # 3) Attente de la requête de connexion d'un client :
        print("Serveur prêt, en attente de requêtes ...")
        mySocket.listen(1) # 1 ou 2 ?

        # 4) Etablissement de la connexion :
        self.connexion, adresse = mySocket.accept()
        print("Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1]))

    def multiClient(self):

        HOST = '192.168.1.28'

        # 1) création du socket :
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) envoi d'une requête de connexion au serveur :
        try:
            self.connexion.connect((HOST, PORT))
        except socket.error:
            print("La connexion a échoué.")
            self.fermer()
        print("Connexion établie avec le serveur.")


    def fermer(self):
        self.closing = True
        if self.connexion != None:
            try:
                self.connexion.send("Z".encode('ascii'))
            except socket.error:
                pass
            self.connexion.close()
        if not self.eventThread.closing:
            self.eventThread.stop()
        #self.eventThread.join()
        pygame.quit()
        sys.exit()




#Main
fen = Fenetre()
