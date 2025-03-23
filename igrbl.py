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
    envoiecommande('G0X'+str(posx)+'Y'+str(posy)+'Z'+str(posz),TRUE)

def deppos1():
    global posx
    global posy
    global posz
    global consx1
    global consy1
    global consz1
    posx=float(consx1.get())
    posy=float(consy1.get())
    posz=float(consz1.get())
    envoiecommande('G0X'+str(posx)+'Y'+str(posy)+'Z'+str(posz),TRUE)

def deppos2():
    global posx
    global posy
    global posz
    global consx2
    global consy2
    global consz2
    posx=float(consx2.get())
    posy=float(consy2.get())
    posz=float(consz2.get())
    envoiecommande('G0X'+str(posx)+'Y'+str(posy)+'Z'+str(posz),TRUE)

def depxp():
    global posx
    global pas
    posx = posx + float(pas.get())
    envoiecommande('G0X'+str(posx),TRUE)
def depxm():
    global posx
    global pas
    posx = posx - float(pas.get())
    envoiecommande('G0X'+str(posx),TRUE)
def depyp():
    global posy
    global pas
    posy = posy + float(pas.get())
    envoiecommande('G0Y'+str(posy),TRUE)
def depym():
    global posy
    global pas
    posy = posy - float(pas.get())
    envoiecommande('G0Y'+str(posy),TRUE)
def depzp():
    global posz
    global pas
    posz = posz + float(pas.get())
    envoiecommande('G0Z'+str(posz),TRUE)
def depzm():
    global posz
    global pas
    posz = posz - float(pas.get())
    envoiecommande('G0Z'+str(posz),TRUE)



def envoiecommande(texte,fin):
    status="runs"
    print(texte)
    print(str(fin))
    time.sleep(0.1)
    port.read(port.inWaiting())       
    port.write(bytes(texte+"\n",'utf-8'))
    time.sleep(0.5)
    print(port.read(port.inWaiting()))

    #attend que la machine soit "Idle" ou Alarm
    while (status!=b'<Idle' and status!=b'<Alar' and fin):
        time.sleep(0.1)
        port.read(port.inWaiting())       
        port.write(bytes("?\n",'utf-8'))       
        status = port.read(5)
        #print(status)        



def exec1():
    global commande1
    envoiecommande(commande1.get(),TRUE)

def exec2():
    global commande2
    envoiecommande(commande2.get(),TRUE)

def script():
    global nomscript
    global okpause
    fichier= open(nomscript.get(),"r")
    gcode = fichier.read().split("\n")
    for i in gcode:
        status="Run"
        #seulement si ce n'est pas une ligne vide ou un commentaire
        if i!="" and i[0]!=";" and i[0]!="(" and i[0]!="%" :
            envoiecommande(i,okpause)
        #si c'est un commentaire simple'
        if i!="" and i[0]==";" and i[1]!="!" :
            print(i)
        #si c'est une zone d'arret'
        if i!="" and i[0]==";" and i[1]=="!" :
            print(i)


def reset():
    global port
    port.close()
    init_com()
    envoiecommande("?",TRUE)

def init_com():
    global port
    port = serial.Serial(nomport.get(),115200)
    port.bytesize = serial.EIGHTBITS
    port.parity =serial.PARITY_NONE
    port.stopbits = serial.STOPBITS_ONE
    port.timeout = 10
    time.sleep(1)
    port.read(port.inWaiting())


def rep():
    global nbrepx
    global nbrepy
    global direpx
    global direpy
    retourzeroX = str(int(direpx.get())*(int(nbrepx.get())-1))
    retourzeroY = str(int(direpy.get())*(int(nbrepy.get())-1))
    j=0
    while j<int(nbrepy.get()):
    
        i=0
        while i<int(nbrepx.get()):
            reset()
            #print("script ici")
            script()
            i=i+1
            #print("G0X"+str(direpx.get())+"Y0") 
            envoiecommande("G0X"+str(direpx.get())+"Y0",TRUE)
        j=j+1
        #print("G0X-"+retourzeroX+"Y"+str(direpy.get())) 
        envoiecommande("G0X-"+retourzeroX+"Y"+str(direpy.get()),TRUE)
    #print("G0X-"+retourzeroX+"Y-"+retourzeroY) 
    envoiecommande("G0X-"+retourzeroX+"Y-"+retourzeroY,TRUE)
        


#initalise l'ecran
fen = Tk()
fen.title("Pilotage carte GRBL 3 axes")
fen.geometry("300x500")



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
panel.place(x=10,y=40)

texte1 = Label (fen, text = "pas:")
pas= Entry(fen,width=8)
texte1.place(x = 200, y = 40)
pas.place(x = 200, y = 56)

texte3 = Label (fen, text = "vitesse:")
vitesse= Entry(fen,width=8)
texte3.place(x = 200, y = 76)
vitesse.place(x = 200, y = 92)

texte2 = Label (fen, text = "port:")
nomport= Entry(fen)
boutonreset = Button (fen, text = "raz", command=reset)
texte2.place(x = 0, y = 4)
nomport.place(x = 40, y = 4)
boutonreset.place(x =220, y = 0)


boutongo1 = Button (fen, text = "go:", command=deppos1)
consx1= Entry(fen,width=5)
consy1= Entry(fen,width=5)
consz1= Entry(fen,width=5)
boutongo1.place(x = 0, y =160)
consx1.place(x = 80, y =164)
consy1.place(x = 140, y =164)
consz1.place(x = 200, y =164)

boutongo2 = Button (fen, text = "go:", command=deppos2)
consx2= Entry(fen,width=5)
consy2= Entry(fen,width=5)
consz2= Entry(fen,width=5)
boutongo2.place(x = 0, y =200)
consx2.place(x = 80, y =204)
consy2.place(x = 140, y =204)
consz2.place(x = 200, y =204)



#excution d'un script
boutonscript= Button (fen, text = "script", command=script)
nomscript= Entry(fen)
okpause = tkinter.IntVar()
checkpause= Checkbutton (fen, variable=okpause, onvalue=TRUE, offvalue=FALSE)
boutonscript.place(x = 0, y =240)
nomscript.place(x = 80, y =244)
checkpause.place(x = 240, y =244)


#execution d'une commande simple'
boutonex1 = Button (fen, text = "ex", command=exec1)
boutonex2 = Button (fen, text = "ex", command=exec2)
commande1= Entry(fen)
commande2= Entry(fen)
boutonex1.place(x = 0, y = 280)
boutonex2.place(x = 0, y = 320)
commande1.place(x =80, y = 284)
commande2.place(x =80, y = 324)

#repetition d'un script
repetition = Frame(fen)
boutonrep = Button (fen, text = "repetition", command=rep)
texte_repas = Label (repetition, text = "distance")
texte_repnb = Label (repetition, text = "nombre")
texte_repx = Label (repetition, text = "X")
texte_repy = Label (repetition, text = "Y")

nbrepx= Entry(repetition,width=6)
nbrepy= Entry(repetition,width=6)
direpx= Entry(repetition,width=6)
direpy= Entry(repetition,width=6)
boutonrep.place(x = 0, y = 380)
texte_repnb.grid(row=0, column=1)
texte_repas.grid(row=0, column=2)


texte_repx.grid(row=1, column=0)
texte_repy.grid(row=2, column=0)
nbrepx.grid(row=1, column=1)
nbrepy.grid(row=2, column=1)
direpx.grid(row=1, column=2)
direpy.grid(row=2, column=2)
repetition.place(x=100,y=380)

#-------------------------------------------------------------
#initalise les variables globales
posx = float(0)
posy = float(0)
posz = float(0)
pas.insert(0, "5")
vitesse.insert(0,"1000")
consx1.insert(0, "0")
consy1.insert(0, "0")
consz1.insert(0, "0")
consx2.insert(0, "100")
consy2.insert(0, "100")
consz2.insert(0, "100")
nomport.insert(0, sys.argv[1])
#nomscript.insert(0, sys.argv[2])


#iniatilse la connexion série
init_com()


#démarre l'ecran
fen.mainloop() # Affichage de la fenêtre


























