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
    Créer une base d'url des listed de monuments historiques à partir d'une page Wikipédia:
        https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_par_département_français

'''
from __future__ import unicode_literals
import requests,bs4
import urllib.parse
from bs4 import BeautifulSoup
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
import special


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

def getData(url,dic_dep):
    r = makeQuery(url)
    contenu = r.text
    main_page = BeautifulSoup(contenu,'html.parser')

    table =  main_page.find_all("table", "wikitable sortable")[0]
    for ligne in table.find_all('tr'):
        x = nb_mh = 0
        cell = code = name = url1 = ''
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
            dic_dep[code]['name'] = name
            dic_dep[code]['text'] = text
            if code in special.special :
                dic_dep[code]['url'] = special.special[code]['url']
            else :
                dic_dep[code]['url'] = url
            dic_dep[code]['nb_mh'] = nb_mh
    return dic_dep

def is_table_url(url,dep):
    print(url)
    r = makeQuery('https://fr.wikipedia.org'+url)
    contenu = r.text
    main_page = BeautifulSoup(contenu,'html.parser')
    #print(main_page.prettify())
    table =  main_page.find('table','wikitable')
    #print (table)
    if isinstance(table,bs4.element.Tag):
        titre = table.find('th')
        # print(type(titre))
        # print(titre.get_text())
        if titre.get_text() == 'Monument' :
            #print('OK')
            return True
        else:
            #print('Non OK')
            return False
    else:
        return False

def get_all_url(url):
    arr=[]
    r = makeQuery('https://fr.wikipedia.org'+url)
    contenu = r.text
    page = BeautifulSoup(contenu,'html.parser')
    for link in page.find_all('a'):
        if isinstance(link.get('title'),str) and "Liste des monuments historiques de l'arrondissement de" in link.get('title') :
            arr.append(link.get('title'))
    print(arr)


if __name__ == "__main__":
    dic_dep = getData(url_base,dic_dep)
    #dep='67'
    #print(dic_dep[dep])
    #print(len(dic_dep))

    ##########################
    #       tests divers
    # url ="/wiki/Liste_des_monuments_historiques_de_la_Gironde"
    # get_all_url(url)
    # list_dep=[]
    # #make_control(dic_dep[dep]['url1'],dep)
    # #test si l'url renvoie la table des mh
    # for k in dic_dep.keys():
    #     if not is_table_url(dic_dep[k]['url1'], k):
    #         list_dep.append(k)
    # print (sorted(list_dep))
    ##########################

    codes = list(range(96))[1:]
    codes.extend([971,972,973,974,975])
    #print(codes)
    for dep in codes:
        d= str(dep).zfill(2)
        if d=='20':
            d='2A'
            print(dic_dep[d])
            d='2B'
        print(dic_dep[d])
