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
# dictionnaire des urls spéciales
# le 15 septembre 2016
#['02', '03', '14', '17', '21', '22', '24', '27', '29',
# '31', '33', '34', '37', '43', '46', '47', '49', '56',
# '59', '60', '62', '63', '64', '67', '70', '71', '72', '75',
# '76', '77', '78', '86', '89']


special = { '02':{'url':["de_l'Aisne_(nord)",
                        "de_l'Aisne_(sud)"]
                 },
            '03':{'url':["de_l'Allier_(A-H)",
                        "de_l'Allier_(I-Z)"]
                 },
            '14':{'url':["de_l'arrondissement_de_Bayeux",
                        "de_l'arrondissement_de_Caen",
                        "de_l'arrondissement_de_Lisieux",
                        "de_l'arrondissement_de_Vire"]
                 },
            '17':{'url':["de_la_Charente-Maritime_(A-N)",
                        "de_la_Charente-Maritime_(O-Z)"]
                 },
            '18':{'url':["du_Cher",
                        "de_Bourges"]
                 },
            '2A':{'url':["de_la_Corse-du-Sud",
                        "d'Ajaccio"]
                 },
            '21':{'url':["de_la_Côte-d'Or_(A-L)",
                        "de_la_Côte-d'Or_(M-Z)"]
                 },
            '22':{'url':["des_Côtes-d'Armor_(A-O)",
                        "des_Côtes-d'Armor_(P-Z)"]
                 },
            '24':{'url':["de_l'arrondissement_de_Bergerac",
                        "de_l'arrondissement_de_Nontron",
                        "de_l'arrondissement_de_Périgueux",
                        "de_l'arrondissement_de_Sarlat-la-Canéda"]
                 },
            '25':{'url':["du_Doubs",
                        "de_Montbéliard",
                        "de_Besançon"]
                 },
            '27':{'url':["de_l'Eure_(A-I)",
                        "de_l'Eure_(J-Z)"]
                 },
            #FIXME les pages sont découpés suivants les lettre de l'alphabet
            #    -> l'analyse ne prend que le premier tableau
            '29':{'url':["du_Finistère_(A-O)",
                        "du_Finistère_(P-Z)",
                        "du_Faou",
                        "de_Landerneau",
                        "de_Locronan",
                        "de_Morlaix",
                        "de_Penmarc'h",
                        "de_Quimper",
                        "de Quimperlé",
                        "de_Saint-Pol-de-Léon"]
                 },
            '31':{'url':["de_la_Haute-Garonne_(A-L)",
                        "de_la_Haute-Garonne_(M-Z)"]
                 },
            '33':{'url':["de_l'arrondissement_d'Arcachon",
                        "de_l'arrondissement_de_Blaye",
                        "de_l'arrondissement_de_Bordeaux",
                        "de_l'arrondissement_de_Langon",
                        "de_l'arrondissement_de_Lesparre-Médoc",
                        "de_l'arrondissement_de_Libourne"]
                 },
            '34':{'url':["de_l'Hérault_(A-L)",
                        "de_l'Hérault_(M-Z)"]
                 },
            '37':{'url':["d'Indre-et-Loire_(A-J)",
                        "d'Indre-et-Loire_(K-Z)"]
                 },
            '39':{'url':["du_département_du_Jura",
                        "d'Arbois",
                        "de_Dole",
                        "de_Lons-le-Saunier",
                        "de_Salins-les-Bains"]
                 },
            '41':{'url':["de_Loir-et-Cher",
                        "de_Blois",
                        "de_Vendôme"]
            },
            '43':{'url':["de_la_Haute-Loire_(ouest)",
                        "de_la_Haute-Loire_(est)"]
                 },
            '44':{'url':['de_la_Loire-Atlantique',
                        "de_Nantes"]
                 },
            '45':{'url':['du_Loiret',
                        "d'Orléans"]
                 },
            '46':{'url':["du_Lot_(A-K)",
                        "du_Lot_(L-Z)"]
                 },
            '47':{'url':["du_Lot-et-Garonne_(A-L)",
                        "du_Lot-et-Garonne_(M-Z)"]
                 },
            '48':{'url':["de_la_Lozère",
                        "de_Mende"]
                 },
            # FIXMEOK : les villes d'Angers et de Saumur ne sont pas dans les listes générales
            '49':{'url':["de_Maine-et-Loire_(nord)",
                        "de_Maine-et-Loire_(sud)",
                        "d'Angers",
                        "de_Saumur"]
                 },
            '50':{'url':["de_l'arrondissement_de_Saint-Lô",
                        "de_l'arrondissement_de_Coutances",
                        "de_l'arrondissement_de_Cherbourg",
                        "de_l'arrondissement_d'Avranches"]
                 },
            '51':{'url':["de_la_Marne",
                        "de_Reims",
                        "de_Châlons-en-Champagne"]
                 },
            '55':{'url':["de_la_Meuse",
                        "de_Bar-le-Duc",
                        "de_Verdun"]
                 },
            '56':{'url':["de_l'arrondissement_de_Lorient",
                        "de_l'arrondissement_de_Pontivy",
                        "de_l'arrondissement_de_Vannes",]
                 },
            '59':{'url':["du_Nord_(A-L)",
                        "du_Nord_(M-Z)"]
                 },
            '60':{'url':["de_l'Oise_(ouest)",
                        "de_l'Oise_(est)",
                        "de_Beauvais",
                        "de_Compiègne",
                        "de_Senlis"]
                 },
            #FIXME pour le département 61 -> voir Mortagne du perche url répétée une 40aine de fois
            '62':{'url':["du_Pas-de-Calais_(A-H)",
                        "du_Pas-de-Calais_(I-Z)"]
                 },
            '63':{'url':["du_Puy-de-Dôme_(A-L)",
                        "du_Puy-de-Dôme_(M-Z)"]
                 },
            '64':{'url':["des_Pyrénées-Atlantiques_(A-L)",
                        "des_Pyrénées-Atlantiques_(M-Z)"]
                 },
            '66':{'url':["des_Pyrénées-Orientales",
                        "de_Perpignan",
                        "de_Villefranche-de-Conflent"]
                 },
            '67':{'url':["du_Bas-Rhin_(A-L)",
                        "du_Bas-Rhin_(M-Z)"]
                 },
            '69':{'url':["du_Rhône",
                        "de_la_Métropole_de_Lyon"]
                 },
            '70':{'url':["de_la_Haute-Saône_(Vesoul_-_Gray)",
                        "de_la_Haute-Saône_(Lure_-_Héricourt)",
                        "de_la_Haute-Saône_(Luxeuil_-_Jussey)"]
                 },

            '71':{'url':["de_Saône-et-Loire_(A-L)",
                        "de_Saône-et-Loire_(M-Z)"]
                 },
            # FIXMEOK : La ville du Mans n'est pas intégrée à son arrondissement
            '72':{'url':["de_l'arrondissement_de_Mamers",
                        "de_l'arrondissement_du_Mans",
                        "de_l'arrondissement_de_la_Flèche",
                        "du_Mans"]
                 },
            '74':{'url':["de_la_Haute-Savoie",
                        "d'Annecy"]
                 },
            '75':{'url':["du_1er_arrondissement_de_Paris",
                        "du_2e_arrondissement_de_Paris",
                        "du_3e_arrondissement_de_Paris",
                        "du_4e_arrondissement_de_Paris",
                        "du_5e_arrondissement_de_Paris",
                        "du_6e_arrondissement_de_Paris",
                        "du_7e_arrondissement_de_Paris",
                        "du_8e_arrondissement_de_Paris",
                        "du_9e_arrondissement_de_Paris",
                        "du_10e_arrondissement_de_Paris",
                        "du_11e_arrondissement_de_Paris",
                        "du_12e_arrondissement_de_Paris",
                        "du_13e_arrondissement_de_Paris",
                        "du_14e_arrondissement_de_Paris",
                        "du_15e_arrondissement_de_Paris",
                        "du_16e_arrondissement_de_Paris",
                        "du_17e_arrondissement_de_Paris",
                        "du_18e_arrondissement_de_Paris",
                        "du_19e_arrondissement_de_Paris",
                        "du_20e_arrondissement_de_Paris"]
                 },
            '76':{'url':["de_l'arrondissement_de_Dieppe",
                        "de_l'arrondissement_du_Havre",
                        "de_l'arrondissement_de_Rouen"]
                 },
            # FIXMEOK : Villes de Fontainbleau et de Provins non intégrée
            '77':{'url':["de_Seine-et-Marne_(ouest)",
                        "de_Seine-et-Marne_(est)",
                        "de_Fontainebleau",
                        "de_Provins"]
                 },
            # FIXMEOK : Versailles non intégré
            '78':{'url':["des_Yvelines_(nord)",
                        "des_Yvelines_(sud)",
                        "de_Versailles",
                        "de_Saint-Germain-en-Laye"]
                 },
            '86':{'url':["de_la_Vienne_(A-L)",
                        "de_la_Vienne_(M-Z)",]
                 },
            # FIXMEOK : Villes non intégrées
            '89':{'url':["de_l'Yonne_(A-M)",
                        "de_l'Yonne_(N-Z)",
                        "de_sens",
                        "d'Auxerre",
                        "de_Tonnerre",
                        "de_Joigny"]
                 },
            '972':{'url':["de_la_Martinique",
                        "de_Fort-de-France",
                        "de_Saint-Pierre_(Martinique)"]
                 },
            '973':{'url':["de_la_Guyane",
                        "de_Cayenne"]
                 },
          }
""
