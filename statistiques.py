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
    créer une date
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
        #formatDateTest = '%Y%m%d%H%M'
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
        ''' Attention : nécéssaire pour changement de format des stats déjà existantes (ajout d'une colonne  - nov 2016)'''
        for date in self.stats:
            for key in self.stats[date]:
                self.stats[date][key][0].append(0)
        self.saveStats()

    def addStats(self, D, stats, pageToCreate, statsSalles):
        ''' ajoute les stats d'un département base et salles (liste de liste)'''
        if self.date not in self.stats.keys() :
            self.stats[self.date] = {}
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

    def getStatsDep(self,dep,date=None):
        '''Renvoie les %Osm et %Wp d'un département pour une date'''
        if date == None :
            date = self.date
        #pprint.pprint(self.stats)
        s = self.stats[date][dep]
        # ((NbMerOsmWip + NbMerOsm - NbOsm )/nbMer)*100
        pCentOsm = round(((int(s[1][6]) + int(s[1][2] - int(s[1][2])))/int(s[0][0]))*100,2)
        # ((NbMerOsmWip + NbMerWip -NbWip - PageACreer )/nbMer)*100
        pCentWp = round(((int(s[1][6]) + int(s[1][4] -int(s[1][3]) - int(s[0][3])))/int(s[0][0]))*100,2)
        return pCentOsm, pCentWp

    def LastDate(self):
        '''Renvoie la dernière date des statistiques'''
        return max(self.data.keys())

    def FirstDate(self):
        ''' Renvoie la première date des statistiques'''
        return min(self.data.keys())

    def getSeriePourCent(self,date=None):
        ''' Renvoie les séries de pourcentage par départements pour une date'''
        serieDep = []
        serieOsm = []
        SerieWp = []
        if date == None :
            date = self.date
        data = OrderedDict(sorted(self.stats[date].items(), key=lambda t: t[0]))
        for departement in data :
            if departement != 'total':
                pcOsm, pcWp = self.getStatsDep(departement,date)
                serieDep.append("'"+departement+"'")
                serieOsm.append(str(pcOsm))
                SerieWp.append(str(pcWp))
        return [serieDep,serieOsm,SerieWp]

    def get_series(self):
        ''' renvoie les valeurs de stats pour permettre le graphe.
            Obsolète.
        '''
        serieDate = []
        serieMerosmwip = []
        serieMerwip = []
        serieOsm = []
        #print (self.data['20161020']['total'])
        for dat in self.data :
            #print (dat)
            ''' liste des dates : réécrit le format date : de 20161025 en 25-10-2016'''
            grapheDate = "'{}-{}-{}'".format(dat[6:8],dat[4:6],dat[0:4])
            serieDate.append(grapheDate)
            ''' liste du nombre de monuments OSM'''
            serieOsm.append(str(self.data[dat]['total'][0][1]))
            ''' liste des monuments ayant une page sur WP '''
            #serieWp.append(str(self.data[dat]['total'][0][3]))
            ''' liste des monuments Merimée wikipédia'''
            serieMerwip.append(str(self.data[dat]['total'][1][4]))
            ''' liste des monumenst présents dans les trois bases'''
            serieMerosmwip.append(str(self.data[dat]['total'][1][6]))
            #print (dat,self.data[dat]['total'])
        return [serieDate,serieOsm,serieMerwip,serieMerosmwip]

    def getPcSeries(self):
        ''' Renvoie les pourcentages de monuments dans osm et wp en fonction du temps.
            calcul avec suppression des pages inexistantes dans WP
        '''
        serieDate = []
        seriePcOsm = []
        seriePcWp = []
        for dat in self.data :
            #print (dat)
            ''' liste des dates : réécrit le format date : de 20161025 en 25-10-2016'''
            grapheDate = "'{}-{}-{}'".format(dat[6:8],dat[4:6],dat[0:4])
            serieDate.append(grapheDate)
            pcosm, pcwp = self.getStatsDep('total',dat)
            seriePcOsm.append(str(pcosm))
            seriePcWp.append(str(pcwp))
        return [serieDate,seriePcOsm,seriePcWp]

    def CalculeAugmentation(self):
        ''' Retourne les valeurs de l'augmentation du nombre total de monuments intégrés sur le dernier jour.
            pour Osm et Wp
        '''
        seriedate = []
        serieosm = []
        seriewp = []


        firstdate = [self.FirstDate()]
        listdate = list(self.data.keys())
        last = self.data[listdate[0]]
        for x in range(1,len(listdate)):
            #print (x, listdate[x], self.data[listdate[x]]['total'])
            #print (x, listdate[x])
            if listdate[x] == '20161128':
                seriedate.append('')
                serieosm.append('0')
                seriewp.append('0')
                last = self.data[listdate[x]]
            else :
                # ''' liste des dates : réécrit le format date : de 20161025 en 25-10-2016'''
                graphedate = "'{}-{}-{}'".format(listdate[x][6:8],listdate[x][4:6],listdate[x][0:4])
                seriedate.append(graphedate)
                osm = self.data[listdate[x]]['total'][1][6] - self.data[listdate[x-1]]['total'][1][6]
                serieosm.append(str(osm))
                wp = (self.data[listdate[x]]['total'][0][2] - self.data[listdate[x]]['total'][0][3]) - (last['total'][0][2] - last['total'][0][3])
                last = self.data[listdate[x]]
                seriewp.append(str(wp))
        return [seriedate,serieosm,seriewp]

def genGraphes(serie1,serie2,serie3):
    ''' Génère la page html avec deux graphes de stats
            serie1 = graphe des départements
            serie2 = graphe de la progression globale
            serie3 = graphe des ajouts de monumenst par jour
    '''
    #Créer le fichier Wom/graphes.html
    if ini.prod :
        filename=ini.url_prod+"/Wom/D/graphes.html"
    else :
        filename=ini.url_dev+"/Wom/D/graphes.html"
    #print(filename)
    oF = open(filename,"w")
    # écrire l'entête
    content =''' <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title> Statistiques de Wom </title>
    <link rel="stylesheet" type="text/css" href="../css/style.css" />
    <script src="../js/jquery.js"></script>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
    '''
    content +='''<script type="text/javascript">
        $(document).ready ( function() {
            $('#container1').highcharts({
                chart: {
                        type: 'column'
                        },
                title: {
                    text: "Intégration par département",
                    x: -20 //center
                        },
                subtitle: {
                    text: 'Source: Mérimée, Wikipédia, OpenStreetMap',
                    x: -20
                        },
                xAxis: {
                    categories: ['''+ ','.join(serie1[0])
    content +='''],
                 crosshair: true,
                 title: {
                        text: 'Départements par code'
                        }
                        },
                yAxis: {
                    title: { text: 'Pourcentage de monuments historiques intégrés dans ... '},
                    min :0,
                    max : 100,
                        },
                tooltip: {
                    headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
                    pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
                    '<td style="padding:0"><b>{point.y:.1f} %</b></td></tr>',
                    footerFormat: '</table>',
                    shared: true,
                    useHTML: true
                        },
                plotOptions: {
                    column: {
                        pointPadding: 0.1,
                        borderWidth: 0
                            }
                        },

                series: [{
                    name: 'Osm',
                    data: [''' + ','.join(serie1[1])
    content += ''']},{
                    name: 'Wp',
                    data: ['''+ ','.join(serie1[2])
    content +=''' ]}
                ]
                })
            });
    </script>'''
    content+='''<script type="text/javascript">
    $(document).ready ( function() {
         Highcharts.chart('container2', {
            chart: { zoomType: 'xy' },
            title: { text: 'Intégration globale et contributions par jour' },
            subtitle: { text: 'Source: Mérimée, OpenStreetMap, Wikipédia' },
            xAxis: [{
                categories: ['''+ ','.join(serie2[0])
    content+='''],
                crosshair: true
                }],
            yAxis: [{ // Primary yAxis : graphe % d\'intégration max
                labels: {
                    format: '{value} %',
                    style: { color: Highcharts.getOptions().colors[1] },
                        },
                title: {
                    text: '% intégration globale des ref:mhs ',
                    style: { color: Highcharts.getOptions().colors[1] }
                        },
            },{ // Secondary yAxis : Graphe par jour :
                gridLineWidth: 0,
                title: {
                    text: 'Nouveaux monuments ce jour',
                    style: { color: Highcharts.getOptions().colors[1] }
                        },
                labels: {
                    format: '{value} Mh',
                style: { color: Highcharts.getOptions().colors[1] }
                        },
                opposite: true,
            }],
            tooltip: { shared: true },
            legend: {
                layout: 'vertical',
                align: 'left',
                x: 80,
                verticalAlign: 'top',
                y: 155,
                floating: true,
                backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
                    },
            series: [{
                name: "% Ref:mhs dans Osm",
                type: 'spline',
                style: { color: Highcharts.getOptions().colors[0] },
                yAxis: 0,
                data: ['''+','.join(serie2[1])
    content+='''],
                tooltip: { valueSuffix: ' %' },
                    },{
                name: '% Ref:mhs dans Wp',
                type: 'spline',
                style: { color: Highcharts.getOptions().colors[6] },
                yAxis: 0,
                data: ['''+','.join(serie2[2])
    content+='''],
                tooltip: { valueSuffix: ' %' },
                },{
                name: 'Contrib Osm du jour ',
                type: 'spline',
                yAxis: 1,
                data: ['''+','.join(serie3[1])
    content+='''],
                tooltip: { valueSuffix: ' mh' }
                    },{
                name: 'Contrib Wp du jour',
                type: 'spline',
                yAxis: 1,
                data: ['''+','.join(serie3[2])
    content+='''],
                tooltip: { valueSuffix: ' mh' }
                    },
                ]
         });
    });
    </script>
    '''
    content += '''</head>
    <body>
    <div id="container1" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
    <br>
    <div id="container2" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
    <div class='message'>
    <p>
    <b>Attention :</b> La chute sur la courbe noire (intégration globale des monuments historiques dans Wikipédia) est due à un changement de mode de calcul le 27 novembre 2016.
    A partir de cette date, les monuments référencés dans les pages départementales mais ayant l'étiquette "page monument inexistante" ne sont plus comptés.
    </p>
    </div>
    </body>
    </html>
    '''
    oF.write(content)
    oF.close()


if __name__ == "__main__":

    stats = Statistiques()
    stats.fname = './stats.json'
    #print (stats)
    #print (stats.data)
    # series = stats.get_series()
    # print (series)
    #
    # date = "20161119"
    # dep ="70"
    # print(stats.getStatsDep(date,dep))

    ''' générer les graphes de prod '''
    genGraphes(stats.getSeriePourCent(stats.LastDate()),stats.getPcSeries(),stats.CalculeAugmentation())

    '''Supprimer les enregistrements pour une date inférieure à debut '''
    # debut = "20161105"
    # for date in stats.data :
    #     if date < debut:
    #         print ('Statistiques du {} supprimées'.format(date))
    #         del stats.stats[date]
    # stats.saveStats()
