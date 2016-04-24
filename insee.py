#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Extraire à partir du fichier txt des N° de commune INSEE, le code insee d'une commune

    source : http://www.insee.fr/fr/methodes/nomenclatures/cog/telechargement.asp?annee=2016
     FIXME => les noms ne doivent pas avoir d'espace => remplacement par "-"   ---(OK)
     FIXME => le fichier source est encodé : Europe occidentale (ISO-8859-1) ou
                Europe occidentale (Windows-1252/WinLatin1).
                Cet encodage est donné par LO.classeur à l'ouverture du fichier .txt
            =>  conversion manuelle par : $iconv -f ISO-8859-1 -t UTF-8 source > cible ---(OK)
                mais pas de traitement sans conversion ?

'''
from __future__ import unicode_literals
import csv, os, chardet
from unidecode import unidecode

class Insee(csv.excel):
    # Séparateur de champ = tabulation
    delimiter = str("\t")

def get_insee(commune):
    ''' Renvoie le code insee d'une commune'''

    commune=commune.replace(" ","-")
    csv.register_dialect('insee', Insee())
    fname = "comsimp2015_utf8.txt"
    file = open(fname, "r")

    try:
        reader = csv.reader(file,'insee')
        for line in reader:
            #print (commune, line)
            if commune in line[11]:
                code = line[3]+line[4]
                return code
                break
    finally:
        file.close()



if __name__ == "__main__":

    com = ('Lyon')
    insee = get_insee(com)
    print(com, " : ",insee)
