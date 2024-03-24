import tkinter
import sys
import serial #http://pyserial.readthedoc.io
import time

from tkinter import *

fen = Tk()
posx = float(0)
posy = float(0)
posz = float(0)
pas= Entry(fen)
pas.insert(0, "5")


#iniatilse la connexion série
port = serial.Serial(sys.argv[1],115200)
port.bytesize = serial.EIGHTBITS
port.parity =serial.PARITY_NONE
port.stopbits = serial.STOPBITS_ONE
port.timeout = 10
time.sleep(2)
port.read(port.inWaiting())

def initecran():

    fen.title("Pilotage carte GRBL 3 axes")

    bouton0 = Button (fen, text = "0", command=dep0)
    boutonxp = Button (fen, text = "X+", command=depxp)
    boutonxm = Button (fen, text = "X-", command=depxm)
    boutonyp = Button (fen, text = "Y+", command=depyp)
    boutonym = Button (fen, text = "Y-", command=depym)
    boutonzp = Button (fen, text = "Z+", command=depzp)
    boutonzm = Button (fen, text = "Z-", command=depzm)
    bouton0.grid(row=0, column=0)
    boutonxp.grid(row=1, column=2)
    boutonxm.grid(row=1, column=0)
    boutonyp.grid(row=0, column=1)
    boutonym.grid(row=2, column=1)
    boutonzp.grid(row=0, column=2)
    boutonzm.grid(row=2, column=0)

    texte1 = Label (fen, text = "pas:")

    texte1.grid(row=0,column=4)
    pas.grid(row=0,column=5)


    fen.mainloop() # Affichage de la fenêtre



def dep0():
    global posx
    global posy
    global posz
    posx=0
    posy=0
    posz=0
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
    print(texte)
    time.sleep(0.1)
    port.read(port.inWaiting())       
    port.write(bytes(texte+"\n",'utf-8'))
    time.sleep(0.5)
    print(port.read(port.inWaiting()))






initecran()

















