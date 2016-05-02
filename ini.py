#!/usr/bin/env python
# -*- coding: utf-8 -*-

# dictionnaire des départements à analyser
dep = {
           '01' : {
                "01": ["Ain"],
                "text":"de l'Ain",
                "url_d" : ["/wiki/Liste_des_monuments_historiques_de_l'Ain"],
                    },
            '42' : {
                "42":["Loire"],
                "text" : "de la Loire",
                "url_d" : ["/wiki/Liste_des_monuments_historiques_de_la_Loire"],
                },
            '69': {
                "69":['Rhône','Métropole de Lyon'],
                "text": "du Rhône",
                "url_d" : ["/wiki/Liste_des_monuments_historiques_du_Rhône","/wiki/Liste_des_monuments_historiques_de_la_métropole_de_Lyon"],
                },
            # '38': {
            #     "38":['Isère'],
            #     "text": "de l'Isère",
            #     "url_d" : ["/wiki/Liste_des_monuments_historiques_de_l'Isère"],
            #     },
            }

# Attention ce répertoire doit être créer avant le lancement du programme !
# racine des pages web
prod=False
# en local
url_dev="/home/jean/osm/monuments_historiques"
# sur Syno
url_prod="/var/services/homes/jean/web_wom"
# fichier statique : style.css
cssFile ="style.css"
