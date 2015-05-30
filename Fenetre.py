import pygame
import sys
from Controlleur import *
from pygame.locals import *
import socket
import time


class Fenetre:

    def __init__(self):

        self.closing = False # utilisé pour arreter les boucles d'event
        self.mute = False

        pygame.display.set_icon(pygame.image.load("res/icon.png"))

        pygame.init()
        pygame.display.set_caption('Jeu du Crapaud')

        self.connexion = None
        self.isServer = False # utilisé pour déterminer qui commence et qui génère les bombes

        self.fenetre = pygame.display.set_mode((LARGEUR_FENETRE, HAUTEUR_FENETRE))

        self.fond1 = pygame.image.load("res/fond1.png").convert_alpha()
        self.fond2 = pygame.image.load("res/fond2.png").convert_alpha()
        self.perso1 = pygame.image.load("res/perso1.png").convert_alpha()
        self.perso2 = pygame.image.load("res/perso2.png").convert_alpha()
        self.victoire1 = pygame.image.load("res/victoirejaune.png").convert_alpha()
        self.victoire2 = pygame.image.load("res/victoirerouge.png").convert_alpha()
        self.bave1 = pygame.image.load("res/bave1.png").convert_alpha()
        self.bave2 = pygame.image.load("res/bave2.png").convert_alpha()
        self.bgmenu = pygame.image.load("res/bgmenu.png").convert_alpha()
        self.explosion = pygame.image.load("res/explosion.png").convert_alpha()
        self.bomb = pygame.image.load("res/bomb.png").convert_alpha()
        self.bomb.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
        self.bgvictoire = pygame.Surface(self.fenetre.get_size()).convert()
        self.bgvictoire.fill((0, 0, 0))

        # on prépare les textes du menu ici parcequ'il sont suuuuuuper looooong à rendre si on doit le faire à chaque refreshMenu().
        self.texts = ["Partie Solo", "Partie Duo", "Partie en ligne", "Appuyez sur :", "S serveur", "C client", "En attente de client ...",
                      "Crapaud Vert a gagné!", "Crapaud Rouge a gagné!", "Faites Entrée pour revenie au menu principal"]
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

        self.afficheMenuPricipal() # et on balance le menu

    def afficheMenuPricipal(self):

        self.playMusic(MUSIC_MENU)

        continuer = True # controle la boucle

        highlightedBlock = PARTIE_DUO # correspond au bouton sur lequel se trouve le curseur
        oldHighlightedBlock = PARTIE_DUO # pour l'animation
        self.refreshMenu(highlightedBlock, oldHighlightedBlock)
        while continuer:
            for e in pygame.event.get():
                if e.type == QUIT:
                    continuer = False
                    self.fermer()
                if e.type == KEYDOWN:
                    if e.key == K_KP4 or e.key == K_LEFT:
                        highlightedBlock = (highlightedBlock - 1) % 3
                    if e.key == K_KP6 or e.key == K_RIGHT:
                        highlightedBlock = (highlightedBlock + 1) % 3
                    if e.key == K_KP_ENTER or e.key == K_RETURN:
                        continuer = False
                        break
                    if e.key == K_SPACE:
                        self.toggleMusic()
                    self.refreshMenu(highlightedBlock, oldHighlightedBlock)
                    oldHighlightedBlock = highlightedBlock
                if e.type == MOUSEMOTION:
                    x = e.pos[0]
                    y = e.pos[1]
                    
                    newHighlightedBlock = self.getBlockAt(x, y)
                        
                    if newHighlightedBlock != None:
                        highlightedBlock = newHighlightedBlock
                        self.refreshMenu(highlightedBlock, oldHighlightedBlock)
                        oldHighlightedBlock = highlightedBlock
                if e.type == MOUSEBUTTONDOWN:
                    if e.button == 1:
                        x = e.pos[0]
                        y = e.pos[1]
                    
                        newHighlightedBlock = self.getBlockAt(x, y)
                        
                        if newHighlightedBlock != None:
                            highlightedBlock = newHighlightedBlock
                            continuer = False
                            break

        if highlightedBlock == PARTIE_EN_LIGNE:
            self.afficheMenuMulti()

        if self.closing: #on vérifie qu'on est pas en train de quitter le jeu
            return

        self.lancePartie(highlightedBlock)
    
    def getBlockAt(self, x, y):
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

        while True: #calcul du dégradé
            r= 255 - (min(255, (oldx1 - MARGE_BOUTON) * 255 / (MARGE_BOUTON + TAILLE_HORIZONTALE_BOUTON)))
            b= max(0, (oldx1 - (2 * MARGE_BOUTON + TAILLE_HORIZONTALE_BOUTON)) * 255 / (MARGE_BOUTON + TAILLE_HORIZONTALE_BOUTON))
            v= 255 - ( r + b )

            self.refreshMenuBackground()
            pygame.draw.lines(self.fenetre, (r,v,b), False, [(oldx1,y1), (oldx2, y1)], 2)
            pygame.draw.lines(self.fenetre, (r,v,b), False, [(oldx1,y1), (oldx1, y2)], 2)
            pygame.draw.lines(self.fenetre, (r,v,b), False, [(oldx1,y2), (oldx2, y2)], 2)
            pygame.draw.lines(self.fenetre, (r,v,b), False, [(oldx2,y1), (oldx2, y2)], 2)
            oldx1 += sens
            oldx2 += sens
            pygame.display.flip()
            if (sens == -1 and oldx1 < newx1) or (sens == 1 and oldx1 > newx1):
                break

    def afficheMenuMulti(self):
        self.fenetre.blit(self.bgmenu, (0,0))
        self.fenetre.blit(self.texts[3], (LARGEUR_FENETRE//2 - self.texts[3].get_width()//2, HAUTEUR_FENETRE//3))
        self.fenetre.blit(self.texts[4], (LARGEUR_FENETRE//3 - self.texts[4].get_width()//2, HAUTEUR_FENETRE//3+TAILLE_VERTCALE_BOUTON))
        self.fenetre.blit(self.texts[5], (2*LARGEUR_FENETRE//3 - self.texts[5].get_width()//2, HAUTEUR_FENETRE//3+TAILLE_VERTCALE_BOUTON))
        pygame.display.flip()
        continuer = True
        while continuer and not self.closing:
            for e in pygame.event.get():
                if e.type == QUIT:
                    continuer = False
                    sys.exit()
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
                    if e.key == K_SPACE:
                        self.toggleMusic()

    def multiInitServeur(self):

        self.fenetre.blit(self.texts[6], (LARGEUR_FENETRE//2 - self.texts[6].get_width()//2, HAUTEUR_FENETRE//3+3*TAILLE_VERTCALE_BOUTON))
        pygame.display.flip()

        self.isServer = True

        # 1) création du socket :
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) liaison du socket à une adresse précise :
        try:
            mySocket.bind((ADRESSE_LOCAL, PORT))
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

        # 1) création du socket :
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2) envoi d'une requête de connexion au serveur :
        try:
            self.connexion.connect((ADRESSE_FOREIGN, PORT))
        except socket.error:
            print("La connexion a échoué.")
            self.fermer()
        print("Connexion établie avec le serveur.")

    def lancePartie(self, typePartie):

        self.playMusic(MUSIC_PARTIE)
        Controlleur(typePartie, self)

    def refresh(self, plateau):

        for i in range(LARGEUR_PLATEAU):
            for j in range(HAUTEUR_PLATEAU):
                case = plateau[i][j]
                if case == CASE_MOUVEMENT:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_BAVE_1:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.bave1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_BAVE_2:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.bave2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CRAPAUD_1:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.perso1,(i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CRAPAUD_2:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.perso2,(i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_BOMB_EMPTY or case == CASE_BOMB:
                    self.fenetre.blit(self.fond2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_EXPLOSION:
                    self.fenetre.blit(self.fond2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                    self.fenetre.blit(self.explosion, (i * LARGEUR_CASE, j * HAUTEUR_CASE))

        pygame.display.flip()

    def displayBombPosition(self, plateau):

        for i in range(LARGEUR_PLATEAU): #on parcours le plateau à la recherche des bombes
            for j in range(HAUTEUR_PLATEAU):
                case = plateau[i][j]
                if case == CASE_MOUVEMENT or case == CRAPAUD_1 or case == CRAPAUD_2 or case == CASE_BAVE_1 or case == CASE_BAVE_2:
                    self.fenetre.blit(self.fond1, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                elif case == CASE_BOMB_EMPTY or case == CASE_BOMB:
                    self.fenetre.blit(self.fond2, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
                if case == CASE_BOMB:
                    self.fenetre.blit(self.bomb, (i * LARGEUR_CASE, j * HAUTEUR_CASE))
        pygame.display.flip()

        #On attend 5 secondes :
        timeStart = time.time()
        while time.time() < timeStart + 5:
            pass

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
                if e.type == QUIT:
                    continuer = False
                    sys.exit()
                if e.type == KEYDOWN:
                    if e.key == K_KP_ENTER or e.key == K_RETURN or e.key == K_z:
                        continuer = False
                        self.afficheMenuPricipal()

    def playMusic(self, musique):
        if musique == MUSIC_MENU:
            pygame.mixer.music.load("res/alex-f.mp3") # Menu le plus electro au monde xD
            pygame.mixer.music.set_volume(0.6) # Sinon les oreilles saignent
            pygame.mixer.music.play(-1)
        elif musique == MUSIC_PARTIE:
            pygame.mixer.music.load("res/popcorn.mp3")
            pygame.mixer.music.set_volume(1) # on remet le volume à donf
            pygame.mixer.music.play(-1) # param -1 fait répéter à l'infini.
        if self.mute:
            pygame.mixer.music.set_volume(0)

    def toggleMusic(self):
        self.mute = not self.mute
        if pygame.mixer.music.get_volume() == 0:
            pygame.mixer.music.set_volume(1)
        else:
            pygame.mixer.music.set_volume(0)

    def fermer(self):
        self.closing = True
        if self.connexion != None:
            try:
                self.connexion.send("Z".encode('ascii')) #on envoi un caractère pour débloquer l'attente du client, et le Z l'informe qu'on arrete.
            except socket.error:
                pass
            self.connexion.close()
        pygame.quit()
        sys.exit()




#Main

fen = Fenetre()
