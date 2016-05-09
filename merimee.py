#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Lire le fichier csv de la base mérimée et extraire
    les codes mhs des monuments d'un département
    Entrée : le code d'un département  = '01'

    Sortie : un musee avec une clé par code MHS
        'ref:mhs1':[le code insee commune,le nom de la commune, adresse, le nom du monument, infos classement avec dates],


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
        Recherche sur le code département (01)
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
                MH=musee.add_Mh(mhs)
                #m.add_infos_mer('insee','commune','adresse','Nom mh', 'Infos classement')
                MH.add_infos_mer(row[5],row[4],row[7],row[6],row[-3])
    finally:
        file.close()
    return musee

if __name__ == "__main__":
    departement = '01'
    musee = mohist.Musee()
    musee = get_merimee(ini.dep[departement]['code'],musee)
    for mh,MH in musee.collection.items():
        print(mh, MH)
        for key,value in MH.description[mh]['mer'].items():
            print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(departement,len(musee.collection)))
    #print(dic_merimee['PA01000038'])
    musee.maj_salle()
    print(musee)

    nb=musee.get_nb_MH('mer')
    print(nb)
