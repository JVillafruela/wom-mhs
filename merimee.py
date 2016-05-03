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
import mohist,ini

class Merimee(csv.excel):
    # Séparateur de champ
    delimiter = "|"

def get_merimee(dep,musee):
    '''
        recherche sur le code département (01)
        les champs du fichier csv :
        REF|ETUD|REG|DPT|COM|INSEE|TICO|ADRS|STAT|AFFE|PPRO|DPRO|AUTR|SCLE
         0    1   2   3   4    5     6   7     8    9    10   11  12   13
         Renvoie un musee contenant des monuments par reférence mhs contenant la clé 'mer' avec la note 1
    '''
    csv.register_dialect('merimee', Merimee())
    fname = "merimee-MH-valid.csv"
    file = open(fname, "r")
    dic_m ={}
    print(dep)
    try:
        reader = csv.reader(file,'merimee')
        for row in reader:
            if dep in row[3]:
                mhs=row[0]
                if mhs not in musee.collection:
                    m=mohist.MoHist(mhs)
                    musee.collection[mhs]=m
                musee.collection[mhs].description[mhs]["mer"]['insee']=row[5]
                musee.collection[mhs].description[mhs]['mer']['commune']=row[4]
                musee.collection[mhs].description[mhs]['mer']['adresse']=row[7]
                musee.collection[mhs].description[mhs]['mer']['nom']=row[6]
                musee.collection[mhs].description[mhs]['mer']['classement']=row[-3]
                musee.collection[mhs].note = 1
    finally:
        file.close()
    return musee

if __name__ == "__main__":
    departement = '69'
    musee = mohist.Musee()
    musee = get_merimee(ini.dep[departement]['code'],musee)
    for mh,MH in musee.collection.items():
        print(mh, MH)
        for key,value in MH.description[mh]['mer'].items():
            print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(departement,len(musee.collection)))
    #print(dic_merimee['PA01000038'])
