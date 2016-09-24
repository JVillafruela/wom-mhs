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
    Récupérer le code wikidata d'un département, puis les codes wikidata de tous les MH de ce département


'''
from __future__ import unicode_literals
import requests
import ini, mohist

wkdCodesSansMh = {}

def get_Q_departement(dep):
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}"
    datas = '''SELECT DISTINCT ?itemLabel ?item WHERE {?item wdt:P31/wdt:P279* wd:Q6465. ?item p:P31 ?dep .
        FILTER NOT EXISTS { ?item p:P576 ?x } FILTER NOT EXISTS { ?item p:P582 ?x }
        FILTER NOT EXISTS { ?dep pq:P582 ?x } SERVICE wikibase:label { bd:serviceParam wikibase:language "fr". } }
        '''
    params = {'format' :'json'}
    r = requests.get(url.format(datas.replace('\n','')),params=params).json()
    return [ dico['item']['value'].split('entity/')[1] for dico in r['results']['bindings'] if dico['itemLabel']['value'] == dep][0]


def get_dic_QMh(Q_dep):
    wdCodes={}
    url = "https://query.wikidata.org/bigdata/namespace/wdq/sparql?query={}"
    datas = '''SELECT DISTINCT ?item ?codeMH WHERE { { ?item wdt:P1435 wd:Q10387575 . } UNION { ?item wdt:P1435 wd:Q10387684 . }
            ?item wdt:P131 ?locadmin . ?locadmin wdt:P131 wd:'''+Q_dep+''' . ?item wdt:P380 ?codeMH . }
            '''
    params = {'format' :'json'}
    r = requests.get(url.format(datas.replace('\n','')),params=params).json()

    #print(r)
    #print (len(r['results']['bindings']))
    for dico in r['results']['bindings'] :
        #print (dico)
        codeMh = dico['codeMH']['value']
        Q_Mh = dico['item']['value'].split('entity/')[1]
        #print(Q_Mh, '->', codeMh)
        wdCodes[codeMh]=Q_Mh
    return wdCodes

def get_wikidata_codes(dep, musee):
    wkdCodes={}
    for d in dep:
        if d == "Métropole de Lyon" :
            Q_dep="Q16665897"
        else :
            Q_dep = get_Q_departement(d)
        #print (d, ' -> ',Q_dep)
        wkdCodes = get_dic_QMh(Q_dep)
        for codeMh in wkdCodes:
            if musee.exist_Mh(codeMh):
                MH = musee.get_MH(codeMh)
                MH.add_infos_wkd(wkdCodes[codeMh])
            else:
                wkdCodesSansMh[codeMh] = wkdCodes[codeMh]
                #print(codeMh, ' -> ',wkdCodes[codeMh])
    return musee

if __name__ == "__main__":

    departement = '69'
    musee = mohist.Musee()
    musee = get_wikidata_codes(ini.dep[departement]['name'],musee)
    if musee.get_nb_MH('wkd') > 0 :
        print("Pour le département {}, il y a {} monuments dans la base wikiData.".format(departement,len(musee.collection)))
        print(musee)

        nb=musee.get_nb_MH('wkd')
        print(nb)
        
    for code in wkdCodesSansMh:
        print (code, '-> ', wkdCodesSansMh[code])
    print (len(wkdCodesSansMh))


###################################
# requete des monuments / departement
# SELECT DISTINCT ?item ?codeMH ?article
#
# WHERE {
#
#   { ?item wdt:P1435 wd:Q10387575 . } # qui sont MHs inscrits
#   UNION
#   { ?item wdt:P1435 wd:Q10387684 . } # ou qui sont MHs classés (ou les deux bien sûr)
#
#   ?item wdt:P131 ?locadmin . #localisation administrative
#
#   ?locadmin wdt:P131 wd:Q3083 . # localisation administrative est elle même dans l'Ain (Ambérieu > Ain) ; Q3083 représente l'Ain
#
#   #article sur wikipedia français
#   ?article schema:about ?item .
#   ?article schema:inLanguage "fr" .
#   ?article schema:isPartOf <https://fr.wikipedia.org/> .
#   ?item wdt:P380 ?codeMH .
#
# } ORDER BY DESC(?item)

########################################
