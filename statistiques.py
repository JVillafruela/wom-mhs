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
from collections import OrderedDict
import ini


class Statistiques:
    '''
        Un objet qui enregistre les comptages des musées par département et par salle
        qui est sauvegardé dans un fichier et rechargé à chaque fois que l'on lance la maj des pages Wom

        Stats =  { date1:{'01':[[0,0,0,0],[0,0,0,0,0,0]],
                          '02':[[0,0,0,0],[0,0,0,0,0,0]],
                            ,
                            ,
                         'total':[[0,0,0,0],[0,0,0,0,0,0]]
                            },
                  date2:{'01':[[[0,0,0,0],[0,0,0,0,0,0]],
                         '02':[[0,0,0,0],[0,0,0,0,0,0]],
                         ,
                         ,
                         'total':[[0,0,0,0],[0,0,0,0,0,0]]
                         },
                  date3:{ 'departement': [[nbMer,nbOsm,NbWip,PageACreer],[NbMer,NbOsm,NbMerOsm,NbWip,NbMerWip,NbOsmwip,NbMerOsmWip]]}

                }

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
        #self.stats[self.date] = {}
        # ordonnées par date
        self.data = OrderedDict(sorted(self.stats.items(), key=lambda t: t[0]))

    def __repr__(self):
        #pprint.pprint(self.stats)
        #pprint.pprint(self.data)
        for date in self.data:
            print (" {} - Nb OSM : {}".format(date,self.data[date]['total'][1][6]))
        return "Nombre de jours de stats : {}".format( len(self.stats))

    def totalStats(self):
        ''' totalise les colonnes de stats d'un jour'''
        self.stats[self.date]['total'] = [[0,0,0,0],[0,0,0,0,0,0,0]]
        #print(self.stats[self.date])
        for k in self.stats[self.date]:
            if k != 'total':
                for i in range(0,4):
                    self.stats[self.date]['total'][0][i] += self.stats[self.date][k][0][i]
                for i in range(0,7):
                    self.stats[self.date]['total'][1][i] += self.stats[self.date][k][1][i]
                #self.stats[self.date]['total'][0][1] += self.stats[self.date][k][0][1]
                #self.stats[self.date]['total'][0][2] += self.stats[self.date][k][0][2]


    def addzero(self) :
        ''' nécéssaire pour changement de format des stats déjà existantes (ajout d'une colonne)'''
        for date in self.stats:
            for key in self.stats[date]:
                self.stats[date][key][0].append(0)
        self.saveStats()

    def addStats(self, D, stats, pageToCreate, statsSalles):
        ''' ajoute les stats d'un département base et salles (liste de liste)'''
        self.stats[self.date][D] =  [ [stats['mer'], stats['osm'], stats['wip'], pageToCreate] ]
        self.stats[self.date][D].append(statsSalles)

    def loadStats(self):
        ''' charge le fichier stats existant'''
        with open(self.fname, 'r',encoding='utf-8') as file:
            return json.load(file)

    def saveStats(self):
        ''' réécrit le fichier stats'''
        with open(self.fname, 'w',encoding='utf-8') as file:
            json.dump(self.stats, file, indent=4)

    def get_series(self):
        ''' renvoie les valeurs de stats en serie pour permettre le graphe'''
        serieDate = []
        serieMerosmwip = []
        serieMerwip = []
        serieOsm = []
        #print (self.data['20161020']['total'])
        for dat in self.data :
            #print (dat)
            ''' liste des dates'''
            grapheDate = "{}-{}-{}".format(dat[6:8],dat[4:6],dat[0:4])
            serieDate.append(grapheDate)
            ''' liste du nombre de monuments OSM'''
            serieOsm.append(str(self.data[dat]['total'][0][1]))
            ''' liste des monuments Merimée wikipédia'''
            serieMerwip.append(str(self.data[dat]['total'][1][4]))
            ''' liste des monumenst présents dans les trois bases'''
            serieMerosmwip.append(str(self.data[dat]['total'][1][6]))
            #print (dat,self.data[dat]['total'])
        return [serieDate,serieOsm,serieMerwip,serieMerosmwip]


def gen_graphe(series):
    ''' Génère la page html avec le graphe de stats'''
    #Créer le fichier Wom/graphe.html
    if ini.prod :
        filename=ini.url_prod+"/Wom/D/graphe.html"
    else :
        filename=ini.url_dev+"/Wom/D/graphe.html"
    #print(filename)
    oF = open(filename,"w")

    # écrire l'entête
    content =''' <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title> Statistiques de Wom </title>
    <script src="../js/jquery.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    '''
    content +='''<script type="text/javascript">
        $(document).ready ( function() {
            $('#container').highcharts({
                title: {
                    text: 'Statistiques de Wom',
                    x: -20 //center
                        },
                subtitle: {
                    text: 'Source: Mérimée, Wikipédia, OpenStreetMap',
                    x: -20
                        },
                xAxis: {
                    categories: ['''+','.join(series[0])
    #print(series[1])
    content +=''']
                        },
                yAxis: {
                    title: { text: 'Nombre de monuments historiques'},
                    plotLines: [{value: 0,width: 1,color: '#808080'}]
                        },
                legend: {layout: 'vertical',align: 'right',verticalAlign: 'middle', borderWidth: 0},
                series: [{
                    name: 'Osm',
                    data: [''' + ','.join(series[1])

    content += ''']},{
                    name: 'Mer Osm Wp',
                    data: ['''+ ','.join(series[3])
    content +=''' ]}
                ]
                })
            });
    </script>'''

    content += '''</head>
    <body>
    <div id="container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
    </body>
    </html>
    '''
    oF.write(content)
    oF.close()


if __name__ == "__main__":

    #print(get_date())
    #return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))
    stats = Statistiques()
    stats.fname = './stats.json'
    #print (stats)
    #print (stats.data)
    series = stats.get_series()
    print (series)
    #
    # gen_graphe(series)
    #stats.addzero()
    #pprint.pprint (stats.data)
