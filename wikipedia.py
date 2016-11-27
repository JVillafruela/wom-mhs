#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2016 JeaRRo <jean.ph.navarro@gmail.com>
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
    Faire une requette sur les pages wikipédia "Liste_des_monuments_historiques_de_l'Ain". chaque département semble avoir une page de ce type.
    en entrée : un code département = '01' pris dans la table des départements (ini.py)
    en sortie : un dictionnaire dic_wp avec une clé par code mhs ou une clé ERR-Numéro pour les monuments qui n'ont pas de code mhs
            PA01000033' : ['Le Café français', 'Bourg-en-Bresse', 'https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse','Cafe_francais']
            'ERR-0023' :[[nom,commune,url_ville,identifiant],[....]]
            (l'identifiant est l'id, ancre de la page web)
    tester avec le rhône pour avoir des erreurs cde mhs absents

    '''
from __future__ import unicode_literals
import requests,bs4,re
from bs4 import BeautifulSoup
import ini,insee,mohist,param
import logging
import urllib.parse
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

url_base ="https://fr.wikipedia.org"
#compteur de monument sans code mhs
ctr_no_mhs=0

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('query-wip-cache', expire=7200)
def makeQuery(url):
    try:
        #rep = requests.get(url)
        return requests.get(url)
    except requests.exceptions.ConnectionError as e:
        message = 'Connection to {0} failed. \n {1}'
        #print (message.format(url, e.args[0].args[1].args[1]))
        print(message.format(url, e))
        #logging.debug(message.format(url, e.args[0].args[1].args[1]))
        #sys.exit(0)
        return url

def getData(url):
    #print(makeQuery(url).status_code)
    r = makeQuery(url)
    if r.status_code == 200 and r != url:
        contenu = r.text
        #contenu = open("wiki.html", "r").read()
        main_page = BeautifulSoup(contenu,'html.parser')
        #print(main_page.prettify())
        return  main_page
    else :
        return url

def normalise(td, commune=None):
    ''' Normalise les champs de wikipédia pour faciliter l'analyse '''
    list_champs=[]
    # list_champs= [nom,commune,adresse,geoloc,code_mhs,image]
    list_champs.append(td[0])
    if len(td) == 8 :
        for n in [1,2,3,4,7] :
            list_champs.append(td[n])
    else:
        list_champs.append(commune)
        for n in [1,2,3,6] :
            list_champs.append(td[n])
    #print(len(list_champs), list_champs)
    return list_champs

def extrait_commune(url):
    ''' Récupère le nom de la commune dans une Url '''
    if "Paris" in url :
        commune = url.split('_')[-4]
    else:
        commune = url.split('_')[-1]
    #correction encodage nom de commune
    if "%C3%A9" in commune:
        commune=commune.replace("%C3%A9","é")
    if "%C3%B4" in commune:
        commune=commune.replace("%C3%B4","ô")
    if "%C3%89" in commune:
        commune=commune.replace("%C3%89","É")
    #print (commune)
    return commune


def extrait_infos(datas):
    global ctr_no_mhs
    infos_manquantes=[]
    toCreateWp = False
    # nom - datas[0]
    #print(datas[0].find('a',href=re.compile('^#cite_note')))
    if isinstance(datas[0].find('a'),bs4.element.Tag) and datas[0].find('a',href=re.compile('^#cite_note')) == None:
        nom = datas[0].find('a').text
        #print(nom)
        #texte du tag wikipédia pour osm
        tag_wk = datas[0].find('a').attrs['title']
        # Rechercher si page WP du monument existe
        if "page inexistante" in tag_wk:
            #print(datas[0].find('a').attrs['title'])
            #print(datas[0].find('a').attrs['href'])
            # Ajoute le lien vers la page à créer
            infos_manquantes.append(datas[0].find('a').attrs['href'])
            toCreateWp = True
            #enlever le texte page inexistante pour le tag wikipédia
            #tag_wk = tag_wk.split(' (')[0]
            #pas de tag_wk pour les pages inexistantes
            tag_wk = ''
    elif datas[0].find('a') == None or datas[0].find('a',href=re.compile('^#cite_note')) != None:
        nom = datas[0].text
        if nom in ini.no_name:
            nom = ''
        infos_manquantes.append("Page monument absente")
        toCreateWp = True
        ''' Suppression proposition de nom pour un tag wikipédia:fr vers une page qui n'existe pas '''
        #tag_wk = nom
        tag_wk = ''
    else :
        nom =''
        tag_wk = ''
    #print (nom)
    #print(tag_wk)

    # Commune - datas[1]
    if isinstance(datas[1].find('a'),bs4.element.Tag):
        #print(datas[1].find('a').text, type(datas[1].find('a').text))
        if 'arrondissement' in datas[1].find('a').text:
            commune ="Lyon_"+datas[1].find('a').text[0]
        else:
            commune = datas[1].find('a').text
    else :
        commune = datas[1]
    #print ('commune =', commune)
    # print('commune url = ', "/wiki/"+commune)
    #recherche code_insee
    #c_insee=insee.get_insee(commune)
    #print ('commune =', commune, "code insee =",c_insee)
    c_insee=""
    # Adresse - datas[2]

    # Geoloc - datas[3]
    rep = datas[3].find('span', {'class':'h-geo geo-dms'})
    #rep = datas[3].find('data', {'class':'p-latitude'})
    #print (type(rep))
    if isinstance(rep,bs4.element.Tag) :
        #print(rep['value'])
        lat= rep.find('data',{'class':'p-latitude'})['value']
        #print(lat)
        lon= rep.find('data',{'class':'p-longitude'})['value']
        #print (lon)
        geo= lat+', '+lon
        #print (geo)
        #geo = datas[3].find('span', {'class':'geo-dec'}).get_text().strip()
        #lat =  geo.split(', ')[0]
        #lon =  geo.split(', ')[1]
    else:
        #print ("Erreur : "+nom+" à "+commune+' -> Pas de Géolocalisation\n')
        geo=""
        infos_manquantes.append("Géolocalisation absente")
        #lat=lon=''
    #print(geo)

    # Code_Mhs - datas[4]
    rep = datas[4].find('cite', {'style':'font-style: normal'})
    # print(rep)
    if isinstance(rep,bs4.element.Tag) :
        code_mhs = rep.get_text().strip()
        #print ('Mhs : ', code_mhs)
        # mhs_url = datas[4].find('a').attrs['href']
        # print(mhs_url)
    else :
        #print ("Erreur : Pas de code MHS pour "+nom+" à "+commune+'\n')
        code_mhs = "ERR-"+str(ctr_no_mhs).zfill(4)
        infos_manquantes.append("Code MHS absent")
        ctr_no_mhs+=1
    #print(code_mhs)

    # image - datas[5]
    # analyse présence image
    if "Image manquante" in datas[5].text:
        #print(nom,"  Pas d'image")
        infos_manquantes.append("Image absente")

    return [code_mhs,c_insee,commune,nom,geo,infos_manquantes,tag_wk,toCreateWp]

def ajoute_infos(infos, musee):
    '''infos=[code_mhs,c_insee,commune,nom,geo,infos_manquantes,tag_wk,toCreateWp,url,identifiant]
                0          1        2   3    4         5            6         7    8   9 '''
    if (infos[0] in musee.collection) and (infos[0] in musee.collection[infos[0]].description) and (musee.collection[infos[0]].description[infos[0]]['wip'] !={}):
        # code identique sur deux/trois objets WIP :
        if 'mhs_bis' in  musee.collection[infos[0]].description[infos[0]]['wip'] :
            musee.collection[infos[0]].description[infos[0]]['wip']['mhs_ter']={'insee': infos[1],
                                                     'commune': infos[2],
                                                     'nom':infos[3],
                                                     'geoloc' : infos[4],
                                                     'url': infos[8],
                                                     'id': infos[9],
                                                     'infos_manquantes':infos[5],
                                                     'tag_wk':infos[6],
                                                     'toCreateWp' : infos[7]  }
        else :
            musee.collection[infos[0]].description[infos[0]]['wip']['mhs_bis']={'insee': infos[1],
                                                 'commune': infos[2],
                                                 'nom': infos[3],
                                                 'geoloc' : infos[4],
                                                 'url': infos[8],
                                                 'id': infos[9],
                                                 'infos_manquantes': infos[5],
                                                 'tag_wk':infos[6],
                                                 'toCreateWp':infos[7] }
        #print (musee.collection[code].description[code]['wip'])
    else:
        #enregistrement d'un momument si le code mhs existe
        MH=musee.add_Mh(infos[0])
        #def add_infos_wip(self, insee, commune, nom, geo, url, ident, infos_manquantes, tag_wk, toCreateWp):
        MH.add_infos_wip(infos[1],infos[2],infos[3],infos[4],infos[8],infos[9],infos[5],infos[6],infos[7])
    return musee

def analyse(data,url,musee,commune=None):
    # print("Commune = ", commune)
    #print("Url = ", urllib.parse.unquote(url))
    logging.debug("log : Url : {}".format(urllib.parse.unquote(url)))
    '''Attention : pour le finistère il y a plusieurs tableau !! '''
    #print(len(data.find_all("table", "wikitable sortable",style = re.compile('^width:100%;'))))
    table =  data.find_all("table", "wikitable sortable",style = re.compile('^width:100%;'))
    for tableau in table:
        for i, tr in enumerate(tableau):
            #print (i, type(tr), tr)

            if isinstance(tr,bs4.element.Tag):
                #l'id du monument permet de le retrouver dans la page
                if 'id' in tr.attrs:
                    identifiant = tr.attrs['id']
                    #print('Id = ',tr.attrs['id'])
                else:
                    identifiant= ''
                td = tr.find_all('td')
                #print(len(td))
                # pages des départements et ville de Lyon (8colonnes), grandes communes (7colonnes)
                if len(td) in [7,8]:
                    if len(td) == 7:
                        commune = extrait_commune(url)
                    datas=normalise(td,commune)
                    # obtenir les infos utilisables dans le musée
                    infos= extrait_infos(datas)
                    #Ajout de l'url et de l'identifiant dans les infos
                    infos.extend([url,identifiant])
                    #print(infos)
                    # Créer le musée
                    musee= ajoute_infos(infos, musee)
                # lien vers pages des grandes communes dans une page département
                elif len(td) == 3 :
                    url_gc = td[2].find('a')['href']
                    url_gc = url_base+url_gc
                    commune = extrait_commune(url_gc)
                    #print ('url_grande_commune = ',url_gc)
                    dat = getData(url_gc)
                    if dat != url_gc:
                        analyse(dat,url_gc,musee,commune)
                    else:
                        logging.debug("log : Url non accessible : {}".format(url_gc))

    return musee

def get_wikipedia(url_list,musee):
    ''' Faire la requette puis l'analyse du résultat '''
    for url in url_list:
        main_page = getData(url_base+url)
        if main_page != url_base+url :
            musee = analyse(main_page,url_base+url,musee)
        else:
            logging.debug("log : Url non accessible : {}".format(url_base+url))
    return musee


if __name__ == "__main__":
    #import pprint
    departement = '12'
    # dic_wp = {}
    # Nb_noMHS=0
    musee = mohist.Musee()
    musee = get_wikipedia(param.dic_dep[departement]['url_d'],musee)
    # for mh,MH in musee.collection.items():
    #     print(mh, MH)
    #     for key,value in MH.description[mh]['wip'].items():
    #         print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans Wikipédia.".format(departement,len(musee.collection)))
    #print(dic_merimee['PA01000038'])
    musee.maj_salle()
    print(musee)

    nb=musee.get_nb_MH('wip')
    print(nb)

    print(ctr_no_mhs)
    # print ("il y a {} Monuments du département {} dans Wikipédia.".format(len(dic_wp),ini.dep[departement]['text']))
    # print ("Monuments du département {} sans code MH : {}".format(ini.dep[departement][('text')],Nb_noMHS))

    # affichier le contenu d'un MH
    # mh = "PA00094109"
    # print (musee.collection[mh])
    # mh = "PA00094198"
    # print (musee.collection[mh])
