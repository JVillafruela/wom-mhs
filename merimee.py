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
    Rechercher et lire le fichier .json de la base mérimée et extraire
    les codes mhs des monuments d'un département. Un test sur la date de version est effectué et la nouvelle version est
    téléchargée si nécéssaire.
    Entrée : le code d'un département  = '01'
    Sortie : un musee avec une clé par code MHS
        'ref:mhs':[le code insee commune,le nom de la commune, adresse, le nom du monument, infos classement avec dates]

'''
from __future__ import unicode_literals
from bs4 import BeautifulSoup
import requests
import json
import logging
import os

import mohist
import param

new_date = ''
datafile = 'merimee-MH.json'


def get_commune(code):
    '''
        Faire une requette sur http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=IA01000159
        pour récupérer le nom de la commune d'un monument s'il ne fait pas partie de la base ouverte
        FIXME pour la commune de Paris problème !!
    '''
    url = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1={}".format(code)
    # print(url)
    try:
        r = requests.get(url)
        # print(r.status_code)
        if r.status_code == 200:
            contenu = r.text
            page = BeautifulSoup(contenu, 'html.parser')
            error = (page.find("h2"))
            # print(error, '\n')
            if error is not None and "Aucun" in str(error):
                # print ("ref:mhs inconnu : ", code)
                return ""
            elif 'Désolé :' in str(error):
                # print('Erreur : la base Mérimée est momentanément inaccessible !')
                return ""
            else:
                tableau = page.find_all("td", attrs={"class": u"champ"})[2].text
                return tableau.split("; ")[-1]
        else:
            # print("ref:mhs inconnu : ", code)
            logging.debug("ref:mhs inconnu : {}".format(code))
            return ""
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print(e)
        logging.error("Base Mérimée inaccessible : {}".format(e))
        return ""


def conv_date(d):
    '''
    en entrée une date dans une liste ['24', 'mai', '2016']
    en sortie une date dans une chaine AAAAMMJJ '20160524' (permetre une comparaison)
    '''
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    # mois = ["Janvier", u"Février", "Mars", "Avril", "Mai", "Juin", "Juillet", u"Août", "Septembre", "Octobre", "Novembre", u"Décembre"]
    # return d[2] + str(mois.index(d[1].capitalize()) + 1).zfill(2) + d[0].zfill(2)
    return d[2] + str(month.index(d[1]) + 1).zfill(2) + d[0].zfill(2)


def get_date():
    ''' Télécharger la date "last-modified" du fichier merimee-MH.json
        Renvoie la date sous la forme YYYYMMJJ '''
    url = "http://data.culture.fr/entrepot/MERIMEE/merimee-MH.json"
    r = requests.head(url)
    date = r.headers['Last-Modified']
    return conv_date(date.strip().split(" ")[1:4])


def existe_nouvelle_version():
    if os.path.isfile("last_date.txt"):
        # print("il est là")
        old_date = open('last_date.txt', 'r').read()
        new_date = get_date()
        if new_date > old_date:
            open('last_date.txt', 'w').write(new_date)
            return True
        else:
            return False
    else:
        # print("pas de fichier")
        ''' Télécharger la date et l'écrire dans le fichier '''
        new_date = get_date()
        open('last_date.txt', 'w').write(new_date)
        return True


def Mise_A_Jour():
    if existe_nouvelle_version():
        ''' Téléchargement de la nouvele version '''
        url = "http://data.culture.fr/entrepot/MERIMEE/merimee-MH.json"
        r = requests.get(url, stream=True)
        with open("merimee-MH.json", 'wb') as fd:
            for chunk in r.iter_content(4096):
                fd.write(chunk)
        fd.close()


def get_merimee(dep, musee):
    '''
         Recherche sur le code département (01)
         Les champs du fichier json :
         REF|ETUD|REG|DPT|COM|INSEE|TICO|ADRS|STAT|AFFE|PPRO|DPRO|AUTR|SCLE
             REF (référence de l'édifice dans la base Mérimée)
             ETUD (type d'étude : recensement immeubles MH, avec éventuellement la mention label Xxe)
             LOCA OU REG + DEPT + COM (localisation de l'édifice)
             INSEE (code INSEE)
             TICO (appellation courante de l'édifice)
             ADRS (adresse, n° de la voie, type de voie, nom de la voie)
             STAT (statut propriété : type de propriétaire par catégorie ; pas de nom)
             AFFE (affectataire : utile pour les propriétés de l'Etat, mentionne le nom du ministère affectataire)
             PPRO (précisions sur la protection : article 1er de l'arrêté de protection + cadastre + nature et date de la protection)
             DPRO (date de protection)
             AUTR (architecte ou maître d'oeuvre)
             SCLE (période de construction)
         Renvoie un musee contenant des monuments par reférence mhs contenant la clé 'mer' avec la note 1
     '''
    global datafile
    url_locale = os.getcwd() + '/'

    with open(url_locale + datafile) as data_file:
        data = json.load(data_file)

    for mh in data[:-1]:
        if mh['DPT'] == dep:
            # print('mhs : ',mh['REF'])
            # print (' insee :',mh['INSEE'],'\n','commune :',mh['COM'],'\n',\
            # 	'adresse:',mh['ADRS'],'\n','nom monument :',mh['TICO'],'\n','Classement :',mh['DPRO'])
            MH = musee.add_Mh(mh['REF'])
            # m.add_infos_mer('insee','commune','adresse','Nom mh', 'Infos classement')
            MH.add_infos_mer(mh['INSEE'], mh['COM'], mh['ADRS'], mh['TICO'], mh['DPRO'], mh['SCLE'])
    return musee


def get_mh(ref):
    ''' rechercher un mh par son code mérimée dans la base ouverte '''

    global datafile
    url_locale = os.getcwd() + '/'

    with open(url_locale + datafile) as data_file:
        data = json.load(data_file)
    trouve = False
    for mh in data[:-1]:
        if mh['REF'] == ref:
            print(mh['REF'], mh['DPT'], mh['TICO'])
            trouve = True
    if not trouve:
        print("Le monument {} ne fait pas partie de la base mérimée.".format(ref))
    return trouve


if __name__ == "__main__":
    departement = '02'
    Mise_A_Jour()
    musee = mohist.Musee()
    musee = get_merimee(param.dic_dep[departement]['code'], musee)
    # for mh,MH in musee.collection.items():
    #     print(mh, MH)
    #     for key,value in MH.description[mh]['mer'].items():
    #         print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(departement, len(musee.collection)))
    musee.maj_salle()
    print(musee)

    # nb = musee.get_nb_MH('mer')
    # print(nb)

    # afficher le contenu d'un MH
    # ref = "PA00116375" # Donjon du temple à chazeys-bons n'existe pass dans mérimée 01
    # ref = "PA00116292"
    # ref = "PA00083624"
    # if get_mh(ref):
    #     print(musee.collection[ref])
