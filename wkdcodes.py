#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 JeaRRo <jean.ph.navarro@gmail.com>
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
    Récupérer tous les wikidata codes Q de tous les item code Mérimée connus
    les mettre dans un dump json
    charger un dump json
    associer à chaque code mérimée un code wkd

    FIXME : si multiple Q pour un code mérimée : faire une liste pour ajout manuel (pas de lien josm)

'''
from __future__ import unicode_literals
import requests
import json
import os
import logging
from collections import OrderedDict


def charger_Q_codes(fichier):
    with open(fichier, 'r', encoding='utf-8') as file:
        return json.load(file)


def sauvegarder_Q_codes(filename, dico):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(dico, file, indent=4)


def get_Q_codes():
    filename = "wkdcodes.json"
    # dictionnaire des "wikidata codes contient pour chaque code Mhs (mérimée) une liste de code wikidata (Qxxxx)"
    wCodes = {}
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}"
    query = '''SELECT DISTINCT ?item ?codeMh WHERE {
      ?item wdt:P380 ?codeMh.
      ?item (wdt:P1435/wdt:P279*) wd:Q916475.
      ?item p:P1435 ?heritage_statement.
      FILTER(NOT EXISTS { ?heritage_statement pq:P582 ?end. })
    }
    '''
    query = ' '.join(query.replace("\n", "").split())
    # print (query)
    param = {"format": "json"}
    r = requests.get(url.format(query), params=param)
    # print(r.url)
    if r.status_code == 200:
        rep = r.json()
        for dico in rep['results']['bindings']:
            codeMh = dico['codeMh']['value']
            Q_Mh = dico['item']['value'].split('entity/')[1]
            # print(codeMh, '->', Q_Mh)
            if codeMh in wCodes:
                wCodes[codeMh].append(Q_Mh)
                # print(type(wCodes[codeMh]))
                # print(wCodes[codeMh])
                wCodes[codeMh] = sorted(wCodes[codeMh])
                # print(wCodes[codeMh])
            else:
                wCodes[codeMh] = [Q_Mh]

        OwCodes = OrderedDict(sorted(wCodes.items(), key=lambda t: t[0]))
        sauvegarder_Q_codes(filename, OwCodes)
        logging.info(" {} Codes Wikidata téléchargés.".format(len(OwCodes)))
    else:
        print("Réponse du serveur non valide : Code réponse = ", r.status_code)
        logging.debug("Réponse du serveur non valide : Code réponse = {}".format(r.status_code))
        if os.path.isfile(filename):
            OwCodes = charger_Q_codes(filename)
            logging.info(" {} Codes Wikidata chargés.".format(len(OwCodes)))
    return OwCodes


if __name__ == "__main__":

    wkdCodes = {}
    wkdCodes = get_Q_codes()
    print("Nombre de codes :", len(wkdCodes))

    # for codeMh in wkdCodes:
    #     print(codeMh, '->', wkdCodes[codeMh])
