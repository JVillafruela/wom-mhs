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
# dictionnaire des départements à analyser
dep = {
           '01' : {
                "name": ["Ain"],
                "code": "01",
                "text": "de l'Ain",
                "url_d": ["/wiki/Liste_des_monuments_historiques_de_l'Ain"],
                    },
            '03' : {
                 "name": ["Allier"],
                 "code": "03",
                 "text": "de l'Allier",
                 "url_d": ["/wiki/Liste_des_monuments_historiques_de_l'Allier_(A-H)","/wiki/Liste_des_monuments_historiques_de_l'Allier_(I-Z)"],
                     },
            '26' : {
                 "name": ["Drôme"],
                 "code": "26",
                 "text": "de la Drôme",
                 "url_d": ["/wiki/Liste_des_monuments_historiques_de_la_Drôme"],
                     },
            '38': {
                "name":['Isère'],
                "code": "38",
                "text": "de l'Isère",
                "url_d" : ["/wiki/Liste_des_monuments_historiques_de_l'Isère"],
                },
            '42' : {
                "name": ["Loire"],
                "code": "42",
                "text": "de la Loire",
                "url_d": ["/wiki/Liste_des_monuments_historiques_de_la_Loire"],
                },
            '69': {
                "name": ['Rhône','Métropole de Lyon'],
                "code": "69",
                "text": "du Rhône",
                "url_d": ["/wiki/Liste_des_monuments_historiques_du_Rhône","/wiki/Liste_des_monuments_historiques_de_la_métropole_de_Lyon"],
                },

            }

# Attention ce répertoire doit être créer avant le lancement du programme !
# racine des pages web
prod=False
# en local
url_dev="/home/jean/osm/monuments_historiques"
# sur Syno
url_prod="/var/services/homes/jean/web_wom"
# fichier statique : style.css
#cssFile ="style.css"
