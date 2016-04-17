#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Lire le fichier csv de la base mérimée et extraire
    les codes mhs des monuments d'un département
    entrée : le code d'un département  = '01'
    sortie : un dictionnaire avec une clé par code MHS qui fournit une liste [le code insee commune,
            le nom de la commune, le nom du monument]

        FIXME : il faudrait ajouter un test sur l'âge de la source Mérimée :
        https://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/
        la version actuelle est datée du : 12 avril 2016
'''
from __future__ import unicode_literals
import csv

class Merimee(csv.excel):
    # Séparateur de champ
    delimiter = "|"

def get_merimee(dep):
    csv.register_dialect('merimee', Merimee())
    fname = "merimee-MH-valid.csv"
    file = open(fname, "r")
    dic_m ={}
    try:
        reader = csv.reader(file,'merimee')
        for row in reader:
            if row[3] == dep:
                #print (row[0],row[4],row[6])
                dic_m[row[0]]=[row[5],row[4],row[6]]
    finally:
        file.close()
    return dic_m


if __name__ == "__main__":
    dic_merimee = {}
    dep = '42'
    dic_merimee = get_merimee(dep)
    print("Pour le dépatement {}, il y a {} monuments dans la base Mérimée.".format(dep,len(dic_merimee)))
    #print(dic_merimee['PA01000038'])
