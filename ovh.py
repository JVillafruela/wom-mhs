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
    Se connecter sur ovh pour récupérer les logs du serveur
    puis analyser les logs pour connaitre les pages départements qui ont été vues aujourd'hui
    et faire la maj de seulement ces départements

    url_exemple = https://logs.ovh.net/jearro.fr/osl/jearro.fr-27-09-2016.log

    Renvoie une liste des départements qui ont été vus sur le web (http://jearro.fr/wom/) aujourd'hui

'''
from __future__ import unicode_literals
import requests,json,re,datetime,ini

def get_date():
    return datetime.datetime.now().strftime('%d-%m-%Y')

def get_log():
    dep_vus=[]
    date = get_date()
    url = 'https://logs.ovh.net/{}/osl/{}-{}.log'.format(ini.domain,ini.domain,date)
    try :
        r = requests.get(url, auth=(ini.login,ini.mdp))
        lines = r.text.split('\n')
        reg1 = re.compile('"GET /wom/[0-9]*_pages')
        reg2 = re.compile('"GET /wom/')
        reg3 = re.compile('_pages')
        for line in lines:
            if reg1.search(line):
                n1 = reg2.search(line).end()
                n2 = reg3.search(line).start()
                #print ('Département : ', line[n1:n2])
                if line[n1:n2] not in dep_vus :
                    dep_vus.append(line[n1:n2])
    except requests.exceptions.SSLError :
        print ('SSLEOFError : Problème de connexion au serveur. Ré-essayer plus tard.')
        dep_vus = get_log()
    return dep_vus

if __name__ == "__main__":

    departement_vus = get_log()
    print("Les pages accédées aujourd'hui : ", departement_vus)
