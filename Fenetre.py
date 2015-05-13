import pygame
import sys
from Constantes import *
from Controlleur import *
from pygame.locals import *
import socket
from queue import Queue


class Fenetre:

    def __init__(self):

        self.closing = False

        pygame.display.set_icon(pygame.image.load("res/kf.png"))

        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.connexion = None
        self.isServer = False # utilisé pour déterminer qui commence

        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

        self.fond1 = pygame.image.load("res/fond1.png").convert_alpha()
        self.fond2 = pygame.image.load("res/fond2.png").convert_alpha()
        self.perso1 = pygame.image.load("res/perso.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso2.png").convert_alpha()
        self.victoire1 = pygame.image.load("res/victoirejaune.png").convert_alpha()
        self.victoire2 = pygame.image.load("res/victoirerouge.png").convert_alpha()
        self.bave = pygame.image.load("res/goutte.png").convert_alpha()
        self.point = pygame.image.load("res/point.png").convert_alpha()
        self.bgmenu = pygame.image.load("res/bgmenu.png").convert_alpha()
        self.bgvictoire = pygame.Surface(self.fenetre.get_size()).convert()
        self.bgvictoire.fill((0, 0, 0))
        self.position_perso1 = self.perso1.get_rect()
        self.position_perso2 = self.perso2.get_rect()

        # on initialise le texte du menu ici parcequ'il est suuuuuuper looooong à rendre si on doit le faire à chaque refreshMenu().
        self.texts = ["Partie Solo", "Partie Duo", "Partie en ligne", "Appuyez sur :", "S serveur", "C client", "En attente de client ...",
                      "Crapaud Jaune a gagné!", "Crapaud Rouge a gagné!", "Faites Entrée pour revenie au menu principal"]
        for i in range(len(self.texts)):
            if i < 3:
                myfont = pygame.font.SysFont("arial", 15) # une police sympa à proposer ?
                self.texts[i] = myfont.render(self.texts[i], 1, (i*100,0, 255/(i+1))) # le compteur génere les couleurs :)
            elif i > 6:
                myfont = pygame.font.SysFont("arial", 15)
                self.texts[i] = myfont.render(self.texts[i], 1, (255, 255, 255))
            else:
                myfont = pygame.font.SysFont("arial", 20)
                self.texts[i] = myfont.render(self.texts[i], 1, (0, 255, 0))
        self.afficheMenuPricipal()


    def afficheMenuPricipal(self):

        pygame.mixer.music.load("res/alex-f.mp3") # Menu le plus electro au monde xD
        pygame.mixer.music.set_volume(0.6) # Sinon les oreilles saignent
        pygame.mixer.music.play(-1)



        continuer = True
        highlightedBlock = PARTIE_DUO # correspond au type de partie qui sera sélectionné
        oldHighlightedBlock = PARTIE_DUO # pour l'animation
        self.refreshMenu(highlightedBlock, oldHighlightedBlock)
        while continuer:
            for e in pygame.event.get():
                if e.type == QUIT:
                    continuer = False
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_KP4 or e.key == K_LEFT:
                        highlightedBlock = (highlightedBlock - 1) % 3
                    if e.key == K_KP6 or e.key == K_RIGHT:
                        highlightedBlock = (highlightedBlock + 1) % 3
                    if e.key == K_KP_ENTER or e.key == K_RETURN or e.key == K_z:
                        continuer = False
                        break
                    self.refreshMenu(highlightedBlock, oldHighlightedBlock)
                    oldHighlightedBlock = highlightedBlock
                if e.type == MOUSEMOTION:
                    x = e.pos[0]
                    y = e.pos[1]
                    
                    newHighlightedBlock = self.getHighlightedBlock(x, y)
                        
                    if newHighlightedBlock != None:
                        highlightedBlock = newHighlightedBlock
                        self.refreshMenu(highlightedBlock, oldHighlightedBlock)
                        oldHighlightedBlock = highlightedBlock
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        x = e.pos[0]
                        y = e.pos[1]
                    
                        newHighlightedBlock = self.getHighlightedBlock(x, y)
                        
                        if newHighlightedBlock != None:
                            highlightedBlock = newHighlightedBlock
                            continuer = False
                            break

        if highlightedBlock == PARTIE_EN_LIGNE:
            self.afficheMenuMulti()

        if self.closing: #on vérifie qu'on est pas en train de quitter le jeu
            return

        self.lancePartie(highlightedBlock)
    
    def getHighlightedBlock(self, x, y):
        for i in range(3):
            x_min = (i + 1) * MARGE_BOUTON + i * TAILLE_HORIZONTALE_BOUTON
            y_min = HAUTEUR_BOUTON
            x_max = x_min + TAILLE_HORIZONTALE_BOUTON
            y_max = y_min + TAILLE_VERTCALE_BOUTON
            
            if x_min <= x <= x_max and y_min <= y <= y_max:
                return i
            
        return None
    
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
    
    
    def afficheMenuMulti(self):
        self.fenetre.blit(self.bgmenu, (0,0))
        self.fenetre.blit(self.texts[3], (LARGEUR_FENETRE//2 - self.texts[3].get_width()//2, HAUTEUR_FENETRE//3))
        self.fenetre.blit(self.texts[4], (LARGEUR_FENETRE//3 - self.texts[4].get_width()//2, HAUTEUR_FENETRE//3+TAILLE_VERTCALE_BOUTON))
        self.fenetre.blit(self.texts[5], (2*LARGEUR_FENETRE//3 - self.texts[5].get_width()//2, HAUTEUR_FENETRE//3+TAILLE_VERTCALE_BOUTON))
        pygame.display.flip()
        continuer = True
        while continuer and not self.closing:
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_s:
                        self.multiInitServeur()
                        continuer = False
                        break
                    if e.key == K_c:
                        self.multiInitClient()
                        continuer = False
                        break
                    if e.key == K_z:
                        break

    def multiInitServeur(self):

        self.fenetre.blit(self.texts[6], (LARGEUR_FENETRE//2 - self.texts[6].get_width()//2, HAUTEUR_FENETRE//3+3*TAILLE_VERTCALE_BOUTON))
        pygame.display.flip()

        self.isServer = True
        HOST = '127.0.0.1'

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

    def multiInitClient(self):

        HOST = '127.0.0.1'

        # 1) création du socket :
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) envoi d'une requête de connexion au serveur :
        try:
            self.connexion.connect((HOST, PORT))
        except socket.error:
            print("La connexion a échoué.")
            self.fermer()
        print("Connexion établie avec le serveur.")
    
    
    def lancePartie(self, typePartie):

        pygame.mixer.music.load("res/popcorn.mp3")
        pygame.mixer.music.set_volume(1) # on remet le volume à donf
        pygame.mixer.music.play(-1) # param -1 fait répéter à l'infini.

        Controlleur(typePartie, self)


    def refresh(self, plateau):

        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                case = plateau[i][j]
                if case == CASE_MOUVEMENT:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_BAVE:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.bave, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CRAPAUD_1:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.perso1,(i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CRAPAUD_2:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.perso2,(i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_POINT_EMPTY:
                    self.fenetre.blit(self.fond2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_POINT_GAINED:
                    self.fenetre.blit(self.fond2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.point, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
        pygame.display.flip()


    def afficheMenuVictoire(self, perdant):
        self.fenetre.blit(self.bgvictoire, (0,0))
        if perdant == CRAPAUD_1:
            texte = self.texts[8]
            victoire = self.victoire2
        else:
            texte = self.texts[7]
            victoire = self.victoire1
        self.fenetre.blit(texte, (LARGEUR_FENETRE//2 - texte.get_width()//2, HAUTEUR_FENETRE//6))
        self.fenetre.blit(self.texts[9], (LARGEUR_FENETRE//2 - self.texts[9].get_width()//2, HAUTEUR_FENETRE//3))
        self.fenetre.blit(victoire, (LARGEUR_FENETRE//2 - victoire.get_width()//2, HAUTEUR_FENETRE//1.5 - victoire.get_height()//2))
        pygame.display.flip()
        continuer = True
        while continuer and not self.closing:
            for e in pygame.event.get():
                if e.type == KEYDOWN:
                    if e.key == K_KP_ENTER or e.key == K_RETURN or e.key == K_z:
                        continuer = False
                        self.afficheMenuPricipal()


    def fermer(self):
        self.closing = True
        if self.connexion != None:
            try:
                self.connexion.send("Z".encode('ascii'))
            except socket.error:
                pass
            self.connexion.close()
        pygame.quit()
        sys.exit()




#Main

fen = Fenetre()
