#fonction ajout d'une ligne de gcode au fichier
def aj_commande(ligne):
    fichier.write(bytes(ligne+"\r\n",'utf-8'))
    return












#recupere les parametres d'usinage
print ("toutes les dimension sont exprimé en mm")
decalageX = 0
decalageY = 0
tailleX = float(input("largeur? (Y)"))
tailleY = float(input("longueur? (Y)"))
vitesse = float( input("vitesse d'avance? (mm/min)"))
diametre = float( input("diametre de l'outils"))
chev =float(input("chevauchement?"))
profondeur = float(input("profondeur?"))
#prof_passe = float(input(profondeur par passe?")
Xmin = decalageX + (0.5*diametre)
Ymin = decalageY + (0.5*diametre)
Xmax = decalageX + tailleX - (0.5*diametre)
Ymax = decalageY + tailleY - (0.5*diametre)


#ouvre le fichier
nom_fichier = input("Nom du programme?")
fichier = open(nom_fichier+".gcode","wb")


#vitesse
aj_commande("F"+str(vitesse))
#position initiale
aj_commande("G0X"+str(Xmin)+"Y"+str(Ymin))
#descente passe initiale
aj_commande("G1Z"+str(profondeur))




#trace le contour
aj_commande("G1X"+str(Xmax))
aj_commande("G1Y"+str(Ymax))
aj_commande("G1X"+str(Xmin))
aj_commande("G1Y"+str(Ymin))

#boucle de balayage horizontal sur X
Xmin = Xmin + diametre - chev
Ymin = Ymin + diametre - chev
Xmax = Xmax - diametre + chev
Ymax = Ymax - diametre + chev

Xactuel = Xmin
Yactuel = Ymin

while Yactuel<Ymax:
    if Xactuel == Xmin:
        aj_commande("G1X"+str(Xmax))
        Xactuel = Xmax
    else:
        aj_commande("G1X"+str(Xmin))
        Xactuel = Xmin

    Yactuel = Yactuel + diametre - chev
    aj_commande("G1Y"+str(Yactuel))


#fin de l'usinage et retour a zéro
aj_commande("G0Z0")
aj_commande("G0X0Y0")
    
    
fichier.close()
print("fichier gcode généré")
