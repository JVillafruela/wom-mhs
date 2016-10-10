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
    Créer une base d'url des listes de monuments historiques à partir d'une page Wikipédia:
    https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_par_département_français

    Attention : toutes les urls de cette liste ne renvoient pas vers la page liste des monuments historiques
            Il faut donc d'abord faire une recherche de ces url et puis rechercher la bonne url et
             complèter manuellement dans le fichier special.py
'''
from __future__ import unicode_literals
import begin
import requests,bs4
import urllib.parse
from bs4 import BeautifulSoup
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import paramSpecial


url_base ="https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_par_département_français"
dic_dep ={}

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('depts-cache', expire=7200)
def makeQuery(url):
    return requests.get(url)

def getData(url,dic_dep,gen_param):
    r = makeQuery(url)
    contenu = r.text
    main_page = BeautifulSoup(contenu,'html.parser')

    table =  main_page.find_all("table", "wikitable sortable")[0]
    for ligne in table.find_all('tr'):
        x = nb_mh = 0
        cell = code = name = url=  ''
        urls = []
        for cell in ligne.find_all('td'):
            #print(type(cell))
            if x == 0 :
                code = cell.get_text()
            elif x == 1 :
                url = urllib.parse.unquote(cell.find('a')['href'])
                #url1 = cell.find('a')['href']
                text = cell.find('a')['title'].split('historiques ')[1]
                name = cell.find('a').get_text()
            elif x == 2 :
                nb_mh = int(cell.get_text()[3:-1])
            x+=1
        #print(code, name, url1)
        if code != '':
            dic_dep[code]={}
            dic_dep[code]['code'] = code
            if name == "Rhône" :
                dic_dep[code]['name'] = ["Rhône", "Métropole de Lyon"]
            else :
                dic_dep[code]['name'] = [name]
            dic_dep[code]['text'] = text
        #########################
        # Si recherche manuelle des urls non standards des départements
            if not gen_param :
                dic_dep[code]['url_d'] = [url]
        #Correction des urls à partir du fichier special.py
            else :
                if code in paramSpecial.special :
                    for u in paramSpecial.special[code]['url']:
                        urls.append("/wiki/Liste_des_monuments_historiques_"+u)
                    dic_dep[code]['url_d'] = urls
                else :
                    dic_dep[code]['url_d'] = [url]
    return dic_dep

def is_table_url(url,dep):
    print("Test de la page :", url)
    r = makeQuery('https://fr.wikipedia.org'+url)
    contenu = r.text
    main_page = BeautifulSoup(contenu,'html.parser')
    #print(main_page.prettify())
    table =  main_page.find_all('table','wikitable sortable')
    #print (len(table))
    if len(table) == 1 :
        return table[0].find('th').get_text() == 'Monument'
    elif len(table) in [2,3]:
        return table[0].find('th').get_text() == 'Monument' or table[1].find('th').get_text() == 'Monument'
    else:
        return False

@begin.subcommand
def get_urls():
    ''' Recherche les urls non conformes'''
    # ### Recherche des départements pour lesquels l'url ne renvoie pas la table des monuments
    # et qui vont demander une recherche manuelle et une inscription dans le fichier paramSpecial.py
    # Attention : il faut commenter/décommenter des lignes de codes dans la fonction getData()
    # Attention : Il faudra ajouter à la liste trouvée le département 69 (Métropole de Lyon non détectée dans les départements)
    dic_dep = {}
    dic_dep = getData(url_base,dic_dep,gen_param = False)

    list_dep = []
    for k in dic_dep.keys():
        if not is_table_url(dic_dep[k]['url_d'], k):
            list_dep.append(k)
    print ("Liste des départements non conformes :", sorted(list_dep))


@begin.subcommand
def gen_param():
    ''' Genérer le fichier Param.py'''
    dic_dep = {}
    dic_dep = getData(url_base,dic_dep,gen_param = True)
    #Génération du fichier param.py
    filename="param.py"
    oF = open(filename,'w')
    oF.write('''#!/usr/bin/env python
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
# dictionnaire des départements
#
#     Ce fichier est généré par le programme param_gen.py après que le fichier paramSpecial.py est été complété manuellement.
#
''')
    oF.write('dic_dep = {')
    codes = list(range(96))[1:]
    codes.extend([971,972,973,974,975])
    #print(codes)
    for dep in codes:
        d= str(dep).zfill(2)
        if d=='20':
            d='2A'
            oF.write("'"+d +"' :" +str(dic_dep[d])+",\n")
            print(dic_dep[d])
            d='2B'
        oF.write("'" + d + "' :" +str(dic_dep[d]) +",\n")
        print(dic_dep[d])
    oF.write("}")
    oF.close()


@begin.start
def main():
    '''
        Attention : il faut d'abord rechercher les url non conformes !
        puis rechercher les urls correctes sur le web
        et complèter manuellement le fichier paramSpecial.py

        Après seulement on peut lancer la génération du fichier param.py
    '''
    print("Attention : Taper -h pour avoir les infos de la ligne de commande")

    pass
