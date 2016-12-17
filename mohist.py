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
    Organisation des infos MH une class Musee qui contient une collection de monuments (MoHist)
'''
import ini
import merimee
import overpass
import wikipedia
import pprint
import bbox
import re
from collections import OrderedDict


class Musee:
    '''
        un musée/salle est une collection de monuments historiques
        un musée/salle est décrit par :
                un nom de musée ou de salle
                une collection : un dico d'objets MoHist : {'code mhs': 'objet monument','code mhs': 'objet monument'}

    '''

    def __init__(self, nom=None):
        self.collection = {}
        if nom:
            self.nom = nom
        else:
            self.nom = "Musée_général"

        self.salles = [
            Salle("vrac", 'Monuments historiques non classés'),
            Salle("mer", 'Monuments historiques présents seulement dans Mérimée', 'Mérimée', 'Monuments à créer dans Wikipédia et dans OpenstreetMap'),
            Salle("osm", 'Monuments historiques présents seulement dans OpenStreetMap', 'Osm', 'Monuments non présents dans la base Mérimée Ouverte ou Erreur de géolocalisation du monument dans OSM ou Erreur de code MHS'),
            Salle("merosm", 'Monuments historiques présents dans Mérimée et OpenStreetMap', 'Mérimée, Osm', 'Monuments à créer dans Wikipédia'),
            Salle("wip", 'Monuments historiques présents seulement dans wikipédia', 'Wp ', 'Monuments non présents dans la base Mérimée Ouverte ou Erreur de géolocalisation du monument dans OSM ou Erreur de code MHS'),
            Salle("merwip", 'Monuments historiques présents dans Mérimée et Wikipédia', 'Mérimée, Wp', 'Monuments à créer dans OpenStreetMap'),
            Salle("osmwip", 'Monuments historiques présents dans OpenStreetMap et Wikipédia', 'Osm, Wp', 'Erreur de géolocalisation du monument dans OSM ou Erreur de code MHS'),
            Salle("merosmwip", 'Monuments historiques présents dans Mérimée, OpenStreetMap et Wikipédia', 'Mérimée, Osm, Wp', 'Monuments présents dans les trois bases.')
        ]
        self.stats = {}

    def __repr__(self):
        result = ""
        for salle in self.salles:
            if len(salle.s_collection) > 0:
                result += str(len(salle.s_collection)) + ' ' + salle.salle['nom'] + " : " + str(sorted(salle.s_collection)[:4]) + '\n'
            else:
                result += salle.salle['nom'] + " : vide\n"
        return result

    def add_Mh(self, ref):
        '''Ajoute un MH ou le crée dans le musee'''
        if ref in self.collection:
            MH = self.collection[ref]
        else:
            MH = MoHist(ref)
            self.collection[ref] = MH
        return MH

    def exist_Mh(self, ref):
        ''' Recherche si un MH existe  '''
        return ref in self.collection

    def get_MH(self, ref):
        ''' récupère un MH'''
        return self.collection[ref]

    def maj_salle(self):
        '''Met à jour les salles après ajout des MH dans le musée '''
        # raz
        for s in self.salles:
            s.s_collection = []
        # mise à jour
        for ref, MH in self.collection.items():
            # correction de la note si osm donne un lien wikipédia
            # print(MH.note, ref)
            if MH.note in [2, 3]:
                MH.corrige_note()

            self.salles[MH.note].s_collection.append(ref)

    def maj_Qcodes(self, dic_Qcodes):
        ''' Associer les Qcodes de wikidata à chaque MH'''
        for codeMh in self.collection:
            if ("ERR" not in codeMh) and (codeMh in dic_Qcodes):
                self.collection[codeMh].description[codeMh]['wkd'] = dic_Qcodes[codeMh]

    def maj_stats(self):
        ''' Compter les MH '''
        base = ['mer', 'osm', 'wip']
        for bs in base:
            self.stats[bs] = self.get_nb_MH(bs)

    def statsSalles(self):
        ''' renvoie une liste des nombres de ref dans chaque salle dans l'ordre des objets salle'''
        listeStatsSalles = []
        for s in self.salles:
            # print(s.getNbRef())
            listeStatsSalles.append(s.getNbRef())
        return listeStatsSalles[1:]

    def trier(self):
        '''Renvoie la collection triée'''
        return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))

    def get_nb_MH(self, base):
        '''Renvoie le nombre de MH dans 'base' (mer,osm ou wip) '''
        x = 0
        for m, v in self.collection.items():
            if v.description[m][base] != {}:
                x += 1
        return x

    def get_nb_pageToCreate(self):
        ''' Renvoie le nombre de page Wp à créer'''
        x = 0
        for m, v in self.collection.items():
            # print(v)
            if (v.description[m]['wip'] != {}) and (v.description[m]['wip']['toCreateWp']):
                x += 1
        return x

    def get_other_tags(self, mh):
        ''' construire des tags OSM à partir des infos TICO et SCLE de la base mérimée'''
        ot = ''
        k = self.collection[mh].description[mh]['mer']['nom'].split(' ')[0].lower()
        if k in ini.other_tags:
            # print("<li>", '</li> <li>'.join(ini.other_tags[k]), "</li>")
            ot = "<li>" + '</li><li>'.join(ini.other_tags[k]) + "</li>"
        # FIXME : ajouter une liste des noms n'ayant pas de tags
        s = self.collection[mh].description[mh]['mer']['siecle']
        if 'e siècle' in s:
            # print(s[s.index('e siècle') - 2:s.index('e siècle')])
            ot += "<li>start_date={}C</li>".format(s[s.index('e siècle') - 2:s.index('e siècle')])
        elif 'er siècle' in s:
            # print(s[s.index('er siècle') - 1: s.index('er siècle')])
            ot += "<li>start_date={}C</li>".format(s[s.index('er siècle') - 1:s.index('er siècle')])
        return ot

    def gen_infos_osm(self, n):
        '''
            Produire des infos d'aide (les tags) pour la création du MH dans OSM
            n est le rang de la salle dans la liste des salles (voir plus haut)
        '''
        # print("Génération complémentaire pour : {}".format(self.salles[n].salle['nom']))
        if len(self.salles[n].s_collection) > 0:
            for mh in self.salles[n].s_collection:
                # print (self.collection[mh])
                infos = ""
                ################
                # trouvés les autres tags (détails )
                tag_O = self.get_other_tags(mh)
                # print(tag_O)
                # Enlever le tag 'building' pour la création d'un point dans Josm
                if tag_O != "":
                    modif = re.sub(r'<li>building=([a-z]*)</li>', r'', tag_O)
                    modif = re.sub(r'</li><li>', r'%7C', modif)
                    tag_P = re.sub(r'<(/*)li>', r'', modif)
                else:
                    tag_P = ''
                # print(tag_P)
                infos += tag_O
                ################
                # tag ref:mhs
                # print ("ref:mhs = {}".format(mh))
                tag_A = "ref:mhs={}".format(mh)
                infos += "<li>" + tag_A + "</li>"
                ################
                # tags wikidata
                if len(self.collection[mh].description[mh]['wkd']) == 1:
                    tag_Q = "wikidata={}".format(self.collection[mh].description[mh]['wkd'][0])
                    infos += "<li>" + tag_Q + "</li>"
                else:
                    # infos+= "<li><b>Wikidata multiples :</b> {}</li>".format(', '.join(self.collection[mh].description[mh]['wkd']))
                    # FIXME envoyer les erreurs wikidata vers un fichier
                    # print("ERR wikidata : {} ->  {}".format(mh, ', '.join(self.collection[mh].description[mh]['wkd'])))
                    tag_Q = ""
                ################
                # classement
                tag_C = "heritage:operator=mhs"
                infos += "<li>" + tag_C + "</li>"
                classement = self.collection[mh].description[mh]['mer']['classement']
                # si une seule date
                if ";" not in classement:
                    tag_D = "heritage="
                    if "classé" in classement:
                        # print ("heritage=2")
                        tag_D = "heritage=2"
                    elif "inscrit" in classement:
                        # print ("heritage=3")
                        tag_D = "heritage=3"
                    infos += "<li>" + tag_D + "</li>"
                    # print( "mhs:inscription_date={}".format(classement.split(":")[0].replace("/","-")))
                    tag_E = "mhs:inscription_date={}".format(classement.split(":")[0].replace("/", "-"))
                    infos += "<li>" + tag_E + "</li>"
                else:
                    # print ("Classement : {}".format(classement))+"</li>"
                    infos += "<li><b>Classements multiples</b> : {}</li>".format(classement)
                    tag_D = ""
                    tag_E = ""
                    infos += "<li><b>Import sans classement !</b> </li>"
                    ################
                    # lien wikipedia
                if 'infos_manquantes' in self.collection[mh].description[mh]['wip'] and "Page monument absente" not in self.collection[mh].description[mh]['wip']['infos_manquantes']:
                    texte = self.collection[mh].description[mh]['wip']['tag_wk']
                    ''' Suppression proposition de nom pour un tag wikipédia:fr vers une page qui n'existe pas '''
                    if texte == "":
                        tag_G = ''
                        # texte=self.collection[mh].description[mh]['mer']['nom']
                    else:
                        tag_G = "wikipedia=fr:{}".format(texte)
                else:
                    tag_G = ""
                infos += "<li>" + tag_G + "</li>"
                ################
                # le nom probable du MH
                name = self.collection[mh].description[mh]['mer']['nom']
                if name in ini.no_name:
                    tag_B = ''
                else:
                    tag_B = "name={}".format(name.replace('"', ''))
                infos += "<li>" + tag_B + "</li>"
                ################
                # print ("Source : Base Mérimée ouverte - avril 2016 ")
                tag_F = "source:heritage=data.gouv.fr, Ministère de la Culture - 2016"
                infos += "<li>" + tag_F + "</li>"
                infos += "<p>"
                ################
                # Géolocalisation et liens si elle exite
                if 'geoloc' in self.collection[mh].description[mh]['wip'] and self.collection[mh].description[mh]['wip']['geoloc'] != '':
                    # print ("Geolocalisation : {}".format(self.collection[mh].description[mh]['wip']['geoloc']))
                    lat = self.collection[mh].description[mh]['wip']['geoloc'].split(', ')[0]
                    lon = self.collection[mh].description[mh]['wip']['geoloc'].split(', ')[1]
                    # print("Position estimée : http://www.openstreetmap.org/?mlat={}&mlon={}#map=19/{}/{}".format(lat,lon,lat,lon))
                    infos += '<li><b><a href="http://www.openstreetmap.org/?mlat={}&mlon={}#map=19/{}/{}" title="Géocodage fourni par Wikipédia : à vérifier" target="__blank"'.format(lat, lon, lat, lon)
                    infos += '>Position estimée</a></b></li>'
                    infos += "<p>"
                    infos_tags = [tag_P, tag_A, tag_Q, tag_B, tag_C, tag_D, tag_E, tag_F, tag_G]
                    tags = [t for t in infos_tags if t != ""]
                    infos += '<li><b><a href="http://localhost:8111/add_node?lon={}&lat={}&addtags={}" title="Création d\'un node dans JOSM (remoteControl) : Vérifier la position et les tags ! ATTENTION : un calque doit déjà être ouvert dans JOSM." target="hide" '.format(lon, lat, '%7C'.join(tags))
                    infos += '>Créer un point dans JOSM</a></b></li>'
                    # télécharger la zone du mh dans JOSM
                    # http://127.0.0.1:8111/load_and_zoom?left=8.19&right=8.20&top=48.605&bottom=48.590
                    left, right, top, bottom = bbox.getBB(float(lat), float(lon))
                    infos += '<li><b><a href="http://localhost:8111/load_and_zoom?left={}&right={}&top={}&bottom={}&zoom_mode=download" \
                            title="Selectionner et copier tous les tags ci-dessus (ctrl-C) puis dans Josm, sélectionner le bâtiment correspondant puis coller les tags (Ctrl-shift-V)?  ATTENTION : ne marche pas si \'Classements multiples\'"\
                            target="hide" '.format(left, right, top, bottom)
                    infos += '>Charger la zone dans JOSM</a></b></li>'
                # print (infos)
                self.collection[mh].description[mh]['infos_osm'] = infos
                # print()


class Salle:

    def __init__(self, nom, titre, onglet=None, titre_onglet=None):
        # l'id sera la note de classement ?
        self.salle = {"nom": nom, "titre": titre, "onglet": onglet, "titre_onglet": titre_onglet}
        # la liste de ref:mhs
        self.s_collection = []

    def __repr__(self):
        return("Page " + self.salle['nom'] + " : " + str(len(self.s_collection))) + " Monuments"

    def getNbRef(self):
        ''' Renvoie le nombre de ref:mhs dans une salle '''
        return len(self.s_collection)


class MoHist:
    '''
        Un monument historique est décrit par :
            un code MHS : code donné officiel extrait sur le site du ministère de la culture (base Mérimée ouverte)
                            ou un code d'erreur si le code précédent n'existe pas
            une description : Un dico contenant le dico obtenu par analyse de chaque base.
                            C'est regroupement des informations fournies par chaque base pour un même code mhs.
            une note : à l'import des bases les datas sont analysées et une note pour chaque base est attribué au MH :
                    1 Présent dans Mérimée ouverte
                    2 Présent dans OSM
                    4 Présent dans WP
            la somme et l'analyse des trois notes permet le classement pour les pages du site web :
                    3 = Présent Mérimée et OSM
                    5 = Présent Mérimée et WP
                    6 = Présent OSM et WP
                    7 = Présent dans les trois bases

    '''

    ctr_monument = 0

    def __init__(self, ref_mhs):
        self.mhs = ref_mhs
        self.description = {self.mhs: {"mer": {}, "osm": {}, "wip": {}, "wkd": ""}}
        self.note = 0

        MoHist.ctr_monument += 1

    def __repr__(self):
        pprint.pprint(self.description)
        # print(self.description)
        return "ref: " + self.mhs + ' noté : ' + str(self.note)

    def add_infos_mer(self, insee, commune, adresse, nom, classement, siecle):
        '''Ajouter les informations issues de la base Mérimée à un monument'''
        self.description[self.mhs]['mer'] = {'insee': insee,
                                             'commune': commune,
                                             'adresse': adresse,
                                             'nom': nom,
                                             'classement': classement,
                                             'siecle': siecle}
        #  if not 'osm' in self.description[self.mhs]:
        self.note += 1

    def add_infos_osm(self, url, tag_mhs, tags_absents, mhs_bis=None):
        self.description[self.mhs]['osm'] = {'url': url,
                                             'tags_mhs': tag_mhs,
                                             'tags_manquants': tags_absents,
                                             'mhs_bis': mhs_bis}
        self.note += 2

    def add_infos_wip(self, insee, commune, nom, geo, url, ident, infos_manquantes, tag_wk, toCreateWp):
        self.description[self.mhs]['wip'] = {'insee': insee,
                                             'commune': commune,
                                             'nom': nom,
                                             'geoloc': geo,
                                             'url': url,
                                             'id': ident,
                                             'infos_manquantes': infos_manquantes,
                                             'tag_wk': tag_wk,
                                             'toCreateWp': toCreateWp}
        self.note += 4

    def corrige_note(self):
        # correction de la note d'un MH si présence lien vers wikipédia
        if 'wikipedia' in self.description[self.mhs]['osm']['tags_mhs'] and self.description[self.mhs]['wip'] == {}:
            self.note += 4

if __name__ == "__main__":
        musee = Musee()

        mhs = 'AP123456'
        m = musee.add_Mh(mhs)
        m.add_infos_mer('01004', 'ambérieu en Bugey', '259 rue Praujan', 'Maison Natoche', 'classé : 1928')
        # print(musee)
        musee.maj_salle()
        print(musee)
        mhs2 = 'AP456789'
        m = musee.add_Mh(mhs2)
        m.add_infos_osm('way/124578', {'name': 'église de la gare', 'ref:mhs': 'AP456789', 'heritage': '3', 'wikipedia': 'fr:wiki/église'}, ['source', ])

        m = musee.add_Mh(mhs)
        m.add_infos_osm('way/124578', {'name': 'gare', 'ref:mhs': 'AP123456', 'heritage': '3'}, ['wikipedia', ])
        print(musee)
        for ref in musee.collection:
            print(musee.collection[ref])
        musee.maj_salle()
        print(musee)
        # mhs2 = 'AP456789'
        # monu2 = MoHist(mhs2)
        # monu2.add_infos_osm('way/124578',{'name':'église de la gare', 'ref:mhs': 'AP456789', 'heritage':'3', 'wikipedia':'fr:wiki/église'},['source',])
        # musee.add_Mh(monu2)
        #
        # mhs3 = 'AP123456'
        # if musee.contient(mhs3):
        #     index =  musee.get_salle_de_mh(mhs3)
        #     print (index)
        #     print (salle, Mh)
        #     Mh.add_infos_osm('node/124578',{'name':'gare sncf', 'ref:mhs': 'AP123456', 'heritage':'2'},[])
        #     musee.move_MH(Mh,salle)
        # else :
        #     monu3 = MoHist(mhs3)
        #     monu3.add_infos_osm('node/124578',{'name':'gare sncf', 'ref:mhs': 'AP123456', 'heritage':'2'},[])
        #     musee.add_Mh(monu3)
        #
        #
        #
        #
        # # print (monument.mhs, monument)
        # # print (monu2.mhs, monu2)
        # # #print(musee.get_salle_de_mh(mhs))
        # # # musee.move_MH(monument,6)
        # # # print (monument)
        # #
        # # # #print(musee.get_salle_de_mh(mhs))
        # # # test, salle = musee.is_in(mhs2)
        # # # if test:
        # # #     print (salle)
        # #
        # # for s in musee.salles:
        # #     print(s)
