#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 JeaRRo <jean.navarro@laposte.net>
#  http://wiki.openstreetmap.org/wiki/User:JeaRRo
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
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
import csv, os
#from unidecode import unidecode

class Insee(csv.excel):
    # Séparateur de champ = tabulation
    delimiter = str("\t")

def get_insee(commune):
    ''' Renvoie le code insee d'une commune'''
    if commune[:2] in ["La",'Le',"L'"]:
        commune = commune[3:]
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
