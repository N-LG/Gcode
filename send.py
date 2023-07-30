
import sys
import serial #http://pyserial.readthedoc.io
import time

#iniatilse la connexion série
port = serial.Serial(sys.argv[1],115200)
port.bytesize = serial.EIGHTBITS
port.parity =serial.PARITY_NONE
port.stopbits = serial.STOPBITS_ONE
port.timeout = 2

#lit le contenu du fichier en une table de ligne de gcode
fichier= open(sys.argv[2],"r")
gcode = fichier.read().split("\n")

#purge les données
time.sleep(2)
port.read(port.inWaiting())

#envoie chaques lignes sur le port série
for i in gcode:
    #seulement si ce n'est pas une ligne vide ou un commentaire
    if i!="" and i[0]!=";":
        print(i)
        msg = i + "\n"
        time.sleep(0.1)
        port.read(port.inWaiting())       
        port.write(bytes(msg,'utf-8'))
        time.sleep(0.1)
        #si il y as une erreur dans le gcode on arrete
        if port.read(2)!=b'ok':
            print("erreur lors de l'execution de la commande")
            sys.exit(1)
        status="Run"
    #si c'est une ligne de commentaire avec attente touche
    if i!="" and i[0]==";" and i[1]=="!":
        print(i[2:len(i)])
        input("appuyez sur entrée pour continuer...")


    #attend que la machine soit "Idle"
    while status!=b'<Idle':
        time.sleep(0.1)
        port.read(port.inWaiting())       
        port.write(bytes("?\n",'utf-8'))       
        status = port.read(5)
        #print(status)        



print("programme Gcode executé") 
