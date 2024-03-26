import tkinter
import sys
import serial #http://pyserial.readthedoc.io
import time
from tkinter import *


def dep0():
    global posx
    global posy
    global posz
    posx=0
    posy=0
    posz=0
    envoiecommande('G0X'+str(posx)+'Y'+str(posy)+'Z'+str(posz))

def deppos():
    global posx
    global posy
    global posz
    global consx
    global consy
    global consz
    posx=float(consx.get())
    posy=float(consy.get())
    posz=float(consz.get())
    envoiecommande('G0X'+str(posx)+'Y'+str(posy)+'Z'+str(posz))

def depxp():
    global posx
    global pas
    posx = posx + float(pas.get())
    envoiecommande('G0X'+str(posx))
def depxm():
    global posx
    global pas
    posx = posx - float(pas.get())
    envoiecommande('G0X'+str(posx))
def depyp():
    global posy
    global pas
    posy = posy + float(pas.get())
    envoiecommande('G0Y'+str(posy))
def depym():
    global posy
    global pas
    posy = posy - float(pas.get())
    envoiecommande('G0Y'+str(posy))
def depzp():
    global posz
    global pas
    posz = posz + float(pas.get())
    envoiecommande('G0Z'+str(posz))
def depzm():
    global posz
    global pas
    posz = posz - float(pas.get())
    envoiecommande('G0Z'+str(posz))



def envoiecommande(texte):
    status="runs"
    print(texte)
    time.sleep(0.1)
    port.read(port.inWaiting())       
    port.write(bytes(texte+"\n",'utf-8'))
    time.sleep(0.5)
    print(port.read(port.inWaiting()))

    #attend que la machine soit "Idle"
    while status!=b'<Idle':
        time.sleep(0.1)
        port.read(port.inWaiting())       
        port.write(bytes("?\n",'utf-8'))       
        status = port.read(5)
        #print(status)        



def exec1():
    global commande1
    envoiecommande(commande1.get())

def exec2():
    global commande2
    envoiecommande(commande2.get())

def script():
    global nomscript
    fichier= open(nomscript.get(),"r")
    gcode = fichier.read().split("\n")
    for i in gcode:
        status="Run"
        #seulement si ce n'est pas une ligne vide ou un commentaire
        if i!="" and i[0]!=";" and i[0]!="(" and i[0]!="%" :
            envoiecommande(i)



#initalise l'ecran
fen = Tk()
fen.title("Pilotage carte GRBL 3 axes")
fen.geometry("300x400")



panel = Frame(fen)
bouton0 = Button (panel, text = "0", command=dep0)
boutonxp = Button (panel, text = "+X", command=depxp)
boutonxm = Button (panel, text = "-X", command=depxm)
boutonyp = Button (panel, text = "+Y", command=depyp)
boutonym = Button (panel, text = "-Y", command=depym)
boutonzp = Button (panel, text = "+Z", command=depzp)
boutonzm = Button (panel, text = "-Z", command=depzm)
bouton0.grid(row=1, column=1)
boutonxp.grid(row=1, column=2)
boutonxm.grid(row=1, column=0)
boutonyp.grid(row=0, column=1)
boutonym.grid(row=2, column=1)
boutonzp.grid(row=0, column=2)
boutonzm.grid(row=2, column=0)
panel.place(x=10,y=50)

texte1 = Label (fen, text = "pas:")
pas= Entry(fen,width=5)
texte1.place(x = 200, y = 50)
pas.place(x = 200, y = 76)

texte2 = Label (fen, text = "port:")
port= Entry(fen)
texte2.place(x = 0, y = 0)
port.place(x = 80, y = 0)

boutonscript= Button (fen, text = "script", command=script)
nomscript= Entry(fen)
boutonscript.place(x = 0, y =200)
nomscript.place(x = 80, y =204)


boutongo = Button (fen, text = "go:", command=deppos)
consx= Entry(fen,width=5)
consy= Entry(fen,width=5)
consz= Entry(fen,width=5)
boutongo.place(x = 0, y =160)
consx.place(x = 80, y =164)
consy.place(x = 140, y =164)
consz.place(x = 200, y =164)


boutonex1 = Button (fen, text = "ex", command=exec1)
boutonex2 = Button (fen, text = "ex", command=exec2)
commande1= Entry(fen)
commande2= Entry(fen)
boutonex1.place(x = 0, y = 240)
boutonex2.place(x = 0, y = 280)
commande1.place(x =80, y = 244)
commande2.place(x =80, y = 284)




#initalise les variables globales
posx = float(0)
posy = float(0)
posz = float(0)
pas.insert(0, "5")
consx.insert(0, "0")
consy.insert(0, "0")
consz.insert(0, "0")
port.insert(0, sys.argv[1])
nomscript.insert(0, sys.argv[2])


#iniatilse la connexion série
port = serial.Serial(sys.argv[1],115200)
port.bytesize = serial.EIGHTBITS
port.parity =serial.PARITY_NONE
port.stopbits = serial.STOPBITS_ONE
port.timeout = 10
time.sleep(2)
port.read(port.inWaiting())


#démarre l'ecran
fen.mainloop() # Affichage de la fenêtre


























