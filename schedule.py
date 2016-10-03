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


'''
    Chaque jour ( mise à jour complète - 101 départements - sur une semaine )
            lancer la maj des pages départemenst visités dans la journée -> get_log()
            lancer la maj d'une série de 15 départments en fonction de la date du jour

            Trouver les numéros des jours de la semaine
            Lundi = 1 .... dimanche = 7
            merci à :
            http://python.jpvweb.com/mesrecettespython/doku.php?id=calcul_de_dates
            dont je reprends deux fonctions numjoursem(D) et numjouran(D)
'''
from __future__ import unicode_literals
import datetime
import requests,re,ini_mdp


def get_date(separateur):
    return datetime.datetime.now().strftime('%d{}%m{}%Y'.format(separateur,separateur))

def get_log():
    '''
        Se connecter sur ovh pour récupérer les logs du serveur
        puis analyser les logs pour connaitre les pages départements qui ont été vues aujourd'hui
        et faire la maj de seulement ces départements

        url_exemple = https://logs.ovh.net/jearro.fr/osl/jearro.fr-27-09-2016.log

        Renvoie une liste des départements qui ont été vus sur le web (http://jearro.fr/wom/) aujourd'hui

    '''
    dep_vus=[]
    date = get_date('-')
    url = 'https://logs.ovh.net/{}/osl/{}-{}.log'.format(ini_mdp.domain,ini_mdp.domain,date)
    try :
        r = requests.get(url, auth=(ini_mdp.login,ini_mdp.mdp))
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
        #FIXME attention la fonction s'appelle elle même risque de boucle infinie !
        print ('SSLEOFError : Problème de connexion au serveur. Ré-essayer plus tard.')
        dep_vus = get_log()
    #print ("Les pages accédées aujourd'hui : ", dep_vus)
    return dep_vus

def numjouran(D):
    """Donne le numéro du jour dans l'année de la date D='j/m/a' (1er janvier = 1, ...)"""
    L=D.split('/')
    #print (L)
    #j, m, a = L
    j = int(L[0])
    m = int(L[1])
    a = int(L[2])
    if ((a%4==0 and a%100!=0) or a%400==0):  # bissextile?
        return (0,31,60,91,121,152,182,213,244,274,305,335,366)[m-1] + j
    else:
        return (0,31,59,90,120,151,181,212,243,273,304,334,365)[m-1] + j

def numjoursem(D):
    """numjoursem(D): donne le numéro du jour de la semaine d'une date D 'j/m/a' (lundi=1, ...)"""
    L=D.split('/')
    an=int(L[2])-1
    j=(an+(an//4)-(an//100)+(an//400)+numjouran(D)) % 7
    if j==0: j=7
    return j

def get_depToMaj():
    '''
        Renvoie la liste des départements à mettre à jour.
    '''
    depToMaj = []
    sequences = [[1,15],[16,29],[30,44],[45,59],[60,74],[75,89],[90,101]]
    #aujourdhui = get_date('/')
    date_test ="09/10/2016"
    N = numjoursem(date_test)
    #N = numjoursem(aujourdhui)
    #print (aujourdhui, ' ', N)
    #print(sequences[N])
    if N == 7 :
        depToMaj = ['90','91','92','93','94','95','971','972','973','974','975']
    elif N == 2 :
        for i in range(sequences[N-1][0], sequences[N-1][1]+1):
            if i == 20 :
                depToMaj.extend(['2A','2B'])
            else:
                depToMaj.append(str(i).zfill(2))
    else:
        for i in range(sequences[N-1][0], sequences[N-1][1]+1):
            depToMaj.append(str(i).zfill(2))
    #print (len(depToMaj), depToMaj)
    #vus_web = get_log()
    vus_web =[]
    #print ("Départements web vus", vus_web)
    for d in vus_web:
        if d not in depToMaj:
            depToMaj.append(d)
    return depToMaj

if __name__ == "__main__":
    print(get_log())
    depToMaj = get_depToMaj()
    print(" {} Départements à mettre à jour : {}".format(len(depToMaj),depToMaj))
