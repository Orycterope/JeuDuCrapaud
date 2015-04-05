PARTIE_SOLO = 0
PARTIE_DUO = 1
PARTIE_EN_LIGNE = 2

PORT = 4545

LARGEUR_PLATEAU = 20
HAUTEUR_PLATEAU = 15

LARGEUR_FENETRE = LARGEUR_PLATEAU * 32
HAUTEUR_FENETRE = HAUTEUR_PLATEAU * 32

HAUTEUR_BOUTON = int(HAUTEUR_FENETRE*2/3)
TAILLE_HORIZONTALE_BOUTON = 100
TAILLE_VERTCALE_BOUTON = 50
MARGE_BOUTON = 80

CRAPAUD_1 = 1
CRAPAUD_2 = 2

CASE_MOUVEMENT = "M"
CASE_POINT_EMPTY = "P"
CASE_POINT_GAINED = "G"
CASE_BAVE = "B"
CASE_CRAPAUD = "C"

MOVECODE = {'A': [0,-2], 'B': [1,-1], 'C': [2,0], 'D': [1,1], 'E': [0,2], 'F': [-1,1], 'G': [-2,0], 'H': [-1,-1]}