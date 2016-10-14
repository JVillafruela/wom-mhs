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
    Faire des statistiques dans les bases
    créer une date et une rotation par jour
    les enregistrer en json dans un fichier
    générer un page html/jquery d'affichage à partir du json
'''

from __future__ import unicode_literals
import json
import os
import datetime
import pprint


class Statistiques:
    '''
        Un objet qui enregistre les comptages des musées par département et par salle
        qui est sauvegardé dans un fichier et rechargé à chaque fois que l'on lance la maj des pages Wom
    '''
    def __init__(self, fname = None):
        ''' la date du jour '''
        formatDate = '%Y%m%d'
        formatDateTest = '%Y%m%d%H%M'
        self.date = datetime.datetime.now().strftime(formatDate)
        if fname == None :
            self.fname = "./stats.json"
        else :
            self.fname = fname
        self.stats = {}
        if os.path.isfile(self.fname) :
            self.stats = self.loadStats()
        else :
            self.saveStats()
        self.stats[self.date] = {}

    def totalStats(self):
        ''' totalise les colonnes de stats d'un jour'''
        self.stats[self.date]['total'] = [[0,0,0],[0,0,0,0,0,0,0]]
        #print(self.stats[self.date])
        for k in self.stats[self.date]:
            if k != 'total':
                for i in range(0,3):
                    self.stats[self.date]['total'][0][i] += self.stats[self.date][k][0][i]
                for i in range(0,7):
                    self.stats[self.date]['total'][1][i] += self.stats[self.date][k][1][i]
                #self.stats[self.date]['total'][0][1] += self.stats[self.date][k][0][1]
                #self.stats[self.date]['total'][0][2] += self.stats[self.date][k][0][2]

    def addStats(self, D, stats, statsSalles):
        ''' ajoute les stats d'un département base et salles (liste de liste)'''
        self.stats[self.date][D] =  [ [stats['mer'], stats['osm'], stats['wip']] ]
        self.stats[self.date][D].append(statsSalles)

    def loadStats(self):
        ''' charge le fichier stats existant'''
        with open(self.fname, 'r',encoding='utf-8') as file:
            return json.load(file)

    def saveStats(self):
        ''' réécrit le fichier stats'''
        with open(self.fname, 'w',encoding='utf-8') as file:
            json.dump(self.stats, file, indent=4)

    def __repr__(self):
        #pprint.pprint(self.stats)
        for date in self.stats:
            print ("Mer, Osm, Wp : {}, {}".format(date,self.stats[date]['total'][1][6]))
        return "Nombre de jours de stats : {}".format( len(self.stats))

# def total(dic_stat[date]):
#     nbMer = NbOsm = nbWip = 0
#     for k,v in dic_stat[date].items():
#         nbMer +=  v[0]
#         nbOsm +=  v[1]
#         nbWip +=  v[2]
#     dic_stat[date]['tout'] = [nbMer, nbOsm, nbWip]
#     return dic_stat[date]
#
# def composeStat(date, D, museeStats, dic_stat):
#     for k,v in museeStats:
#         dic_stat[date][D].append(v)
#     return dic_stat

if __name__ == "__main__":

    #print(get_date())

    stats = Statistiques()
    stats.fname = './stats.json'
    stat_01 = { 'mer':145, 'osm':25, 'wip':56}
    stat_02 = { 'mer':545, 'osm':125, 'wip':256}
    stat_03 = {'mer':55, 'osm':15, 'wip':26}
    stat_04 = {'mer':553, 'osm':155, 'wip':426}
    stats.addStats('01', stat_01)
    stats.addStats('02', stat_02)
    stats.addStats('03', stat_03)
    stats.addStats('04', stat_04)
    stats.totalStats()
    print(stats)
    stats.saveStats()

'''
pour chaque département (musee) il faut récupérer les stats
Faire une série par date du jour
    dans la série
        - par base ['mer','osm','wip'] -> 'DText':[nbMer,nbOsm,NbWip],
    stats=  { date1:{'01':[0,0,0],
                    '02':[0,0,0],
                            ,
                            ,
                            'tout':[0,0,0]
                            },
                  date2:{'01':[0,0,0],
                         '02':[0,0,0],
                         ,
                         ,
                         'tout':[0,0,0]
                         },
                }

            un total par departement
            un total général
        - par salle         ->              {'01':{'merosmwip':0},{'merosm':0},{'merwip':0},
                                            '02':{'mer':0},{'osm':0},{'wip':0},
                                            '03':{'mer':0},{'osm':0},{'wip':0},
                                            '04':{'mer':0},{'osm':0},{'wip':0},
                                            'tout':{'mer':0},{'osm':0},{'wip':0} }
            total par departement
            total général


'''
