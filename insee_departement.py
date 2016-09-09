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
    Extraire à partir d'un code département le nom du département.

    Source : http://www.insee.fr/fr/methodes/nomenclatures/cog/telechargement/2016/txt/depts2016.txt

    FIXME => le fichier source est encodé : Europe occidentale (ISO-8859-1) ou
               Europe occidentale (Windows-1252/WinLatin1).
               Cet encodage est donné par LibreOffice.classeur à l'ouverture du fichier .txt
           =>  conversion manuelle par : $iconv -f ISO-8859-1 -t UTF-8 source > cible ---(OK)
               pas de traitement sans conversion ? NON après téléchargeement il faut convertir le fichier

    Dessin du fichier « Départements » et liste des variables
    millésime 2016
    Dessin du fichier Départements
    Longueur	   Nom	       Désignation en clair
    2	          REGION	       Code région
    3	          DEP	           Code département
    5	          CHEFLIEU	       Code de la commune chef-lieu
    1	          TNCC	           Type de nom en clair
    70	          NCC	           Libellé en lettres majuscules
    70	          NCCENR	       Libellé enrichi


'''
from __future__ import unicode_literals
import csv, os
import requests,bs4
import urllib.parse
from bs4 import BeautifulSoup
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

url_base ="https://fr.wikipedia.org/wiki/Catégorie:Monument_historique_par_département"


class Insee(csv.excel):
    # Séparateur de champ = tabulation
    delimiter = str("\t")

def get_nom(code):
    csv.register_dialect('insee', Insee())
    fname = "depts2016_utf8.txt"
    file = open(fname, "r")
    try:
        reader = csv.reader(file,'insee')
        for line in reader:
            #print (commune, line)
            if code in line[1]:
                nom = line[5]
                return nom
                break
    finally:
        file.close()

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('wikipedia-cache', expire=7200)
def makeQuery(url):
    return requests.get(url)

def getData(url):
    r = makeQuery(url)
    contenu = r.text
    #contenu = open("wiki.html", "r").read()
    main_page = BeautifulSoup(contenu,'html.parser')
    #print(main_page.prettify())
    return main_page

def get_url(main_page, nom_dep):
    '''
        rechercher l'url des pages MH du dep donné en entrée

        <a class="CategoryTreeLabel CategoryTreeLabelNs14 CategoryTreeLabelCategory" href="/wiki/Cat%C3%A9gorie:Monument_historique_du_Var">
                       Monument historique du Var
    '''
#    for link in main_page.find_all('a',"CategoryTreeLabel"):
    #    print(link.get('href'), link.get_text())
    for link in main_page.find_all('a',"CategoryTreeLabel"):
        if nom_dep in link.get_text():
            #print(link.get('href'))
            url = "https://fr.wikipedia.org"+link.get('href')
            #print(url)
            return url
            break

def get_url_suivante(page):
    '''
         <div class="mw-category">
         <div class="mw-category-group">
          <h3>
           *
          </h3>
          <ul>
           <li>
            <a href="/wiki/Liste_des_monuments_historiques_du_Doubs" title="Liste des monuments historiques du Doubs">
             Liste des monuments historiques du Doubs
            </a>
           </li>
          </ul>
         </div>

    '''
    table = page.find('div','mw-category-group')
    T = table.find_all('a')
    for link in T:
        print(link)


if __name__ == "__main__":
    code = '12'
    nom_dep= get_nom(code)
    print(code, " : ",nom_dep)
    main_page = getData(url_base)
    url2 = get_url(main_page,nom_dep)
    #print(urllib.parse.unquote(url2))
    second_page = getData(urllib.parse.unquote(url2))
    get_url_suivante(second_page)
    #print(second_page.prettify())
