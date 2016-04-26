#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Lire le fichier csv de la base mérimée et extraire
    les codes mhs des monuments d'un département
    entrée : le code d'un département  = '01'
             le code insee d'une commune = '01053' pour Bourg-en-Bresse (paramètre facultatif)
    sortie : un dictionnaire avec une clé par code MHS qui fournit une liste
        dic= { 'ref:mhs1':[le code insee commune,le nom de la commune, le nom du monument, infos classement avec dates],
               'ref:mhs2':[le code insee commune,le nom de la commune, le nom du monument, infos classement avec dates]}

        FIXME : il faudrait ajouter un test sur l'âge de la source Mérimée :
        https://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/
        la version actuelle est datée du : 12 avril 2016
'''
from __future__ import unicode_literals
import csv
from collections import OrderedDict

class Merimee(csv.excel):
    # Séparateur de champ
    delimiter = "|"

def get_merimee(dep,inseeCom=None):
    csv.register_dialect('merimee', Merimee())
    fname = "merimee-MH-valid.csv"
    file = open(fname, "r")
    dic_m ={}
    try:
        reader = csv.reader(file,'merimee')
        for row in reader:
            if inseeCom :
                if dep in row[3] and inseeCom in row[5] :
                    dic_m[row[0]]=[row[5],row[4],row[6],row[-3]]
            elif dep in row[3]:
                # ref:mhs = N°insee commune, Nom commune, Nom monument,infos classement avec dates
                dic_m[row[0]]=[row[5],row[4],row[6],row[-3]]
    finally:
        file.close()
    dic_m = OrderedDict(sorted(dic_m.items(), key=lambda t: t[0]))
    return dic_m


if __name__ == "__main__":
    dic_merimee = {}
    dep = '01'
    # insee ='01053'  #Bourg-en-Bresse
    # dic_merimee = get_merimee(dep,insee)
    dic_merimee = get_merimee(dep)
    for key,value in dic_merimee.items():
        print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(dep,len(dic_merimee)))
    #print(dic_merimee['PA01000038'])
