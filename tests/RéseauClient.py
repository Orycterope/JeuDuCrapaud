# Définition d'un client réseau rudimentaire
# Ce client dialogue avec un serveur ad hoc

import socket, sys

HOST = '127.0.0.1'
PORT = 4545

# 1) création du socket :
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2) envoi d'une requête de connexion au serveur :
try:
    mySocket.connect((HOST, PORT))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()    
print("Connexion établie avec le serveur.")

# 3) Dialogue avec le serveur :
msgServeur = mySocket.recv(1024).decode('utf-8')

while 1:
    if msgServeur.upper() == "FIN" or msgServeur =="":
        break
    print("S>", msgServeur)
    msgClient = input("C> ").encode('ascii')
    mySocket.send(msgClient)
    msgServeur = mySocket.recv(1024).decode('utf-8')

# 4) Fermeture de la connexion :
print("Connexion interrompue.")
mySocket.close()