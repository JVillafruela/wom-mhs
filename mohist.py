#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Organisation des infos MH une class Musee qui contient une collection de monuments (MoHist)
'''
import ini,merimee,overpass
from collections import OrderedDict
#
# class Salle(Musee):
#     ''' Un extrait, une partie d'un musée'''
#     pass

class Musee:
    '''
        un musée contient des monuments historiques
    '''
    def __init__(self,nom):
        self.collection = {}
        self.nom=nom

    def trier(self):
        '''Renvoie la collection triée'''
        return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))

    def calcul_nbMH_merimee(self):
        '''Renvoie le nombre de MH dans la base Mérimée '''
        x=0
        for m,v in self.collection.items():
            if  v.description[m]['mer']:
                x+=1
        return x

    def calcul_nbMH_osm(self):
        '''Renvoie le nombre de MH dans la base OSM '''
        x=0
        for m,v in self.collection.items():
            if  v.description[m]['osm'] and not "Bis" in m :
                x+=1
        return x

    def chercher_MerOsm(self):
        ''' Créer une salle avec les MH communs à Mérimée et OSM'''
        salle_merosm=Musee('merosm')
        for m,v in self.collection.items():
            if  v.description[m]['mer'] and v.description[m]['osm']:
                salle_merosm.collection[m] = v.description[m]
                v.cat="merosm"
        #print(len(salle_merosm.collection))
        return salle_merosm

    def chercher_Osm(self):
        ''' Créer une salle avec les MH OSM qui ne sont pas dans Mérimée'''
        salle_osm=Musee('osm')
        for m,v in self.collection.items():
            if not v.description[m]['mer'] and v.description[m]['osm'] and not "Bis" in m :
                salle_osm.collection[m] = v.description[m]
                v.cat="osm"
        #print(len(salle_osm.collection))
        return salle_osm

class MoHist:
    '''
        un monument historique
    '''
    ctr_monument=0

    def __init__(self, ref_mhs=None):
        if ref_mhs:
            self.mhs=ref_mhs
        else:
            self.mhs = "no_mhs_"+str(MoHist.ctr_monument)
        self.description={self.mhs:{"mer":{},"osm":{},"wip":{}}}
        #la catégorie du monument => résultat des tests en fonciton de la source mer,osm,wip
        self.cat=""
        MoHist.ctr_monument+=1

def charge_merimee(dep,musee):
    ''' Créer les MH à partir de la base Mérimée
    dic_merimee => {ref:mhs :[N°insee_commune, Nom commune, Nom monument, infos classement avec dates], ref_suivante : [,,,], etc...}'''
    dic_mer = merimee.get_merimee(dep)
    for mhs in dic_mer:
        if mhs not in musee.collection:
            m=MoHist(mhs)
            musee.collection[mhs]=m
        musee.collection[mhs].description[mhs]["mer"]['insee']=dic_mer[mhs][0]
        musee.collection[mhs].description[mhs]['mer']['commune']=dic_mer[mhs][1]
        musee.collection[mhs].description[mhs]['mer']['nom']=dic_mer[mhs][2]
        musee.collection[mhs].description[mhs]['mer']['classement']=dic_mer[mhs][3]

def charge_osm(d,musee):
    ''' Créer les MH à partir de la requette overpass sur OSM
    dic_osm => {'ref:mhs':[type/id,le dico des tags, la liste des tags manquants],ref_suivante : [,,,], etc...}
    '''
    dic_osm = overpass.get_osm(d['zone_osm'])
    for mhs in dic_osm:
        if mhs not in musee.collection:
            m=MoHist(mhs)
            musee.collection[mhs]=m
        musee.collection[mhs].description[mhs]["osm"]['url_osm']=dic_osm[mhs][0]
        musee.collection[mhs].description[mhs]['osm']['tags_mh']=dic_osm[mhs][1]
        musee.collection[mhs].description[mhs]['osm']['tags_manquants']=dic_osm[mhs][2]
        #récupérer le tag wikipédia
        if 'wikipedia' in dic_osm[mhs][1]:
            musee.collection[mhs].description[mhs]['osm']['wikipedia']=dic_osm[mhs][1]['wikipedia']

if __name__ == "__main__":
    salle_merosm=Musee('test')
    salle_osm=Musee('test1')
    for d in ini.dep:
        #print(d,ini.dep[d])
        StPierre=Musee(ini.dep[d][d])
        charge_merimee(d,StPierre)
        charge_osm(ini.dep[d],StPierre)


        ''' Affichage  extrait base Mérimée '''
        #print(StPierre.collection['PA00116330'].description['PA00116330']['mer'])
        # StPierre_trier=StPierre.trier()
        # for m,value in StPierre_trier.items():
        #     print(value.description[m]['mer']['commune'])
        ''' Affichage  extrait base OSM'''
        # StPierre_trier=StPierre.trier()
        # for m,value in StPierre_trier.items():
        #     if "Bis" in m :
        #         print(m)
            #print(value.description[m]['osm']['url_osm'])
        ''' qq stats'''
        print("Nombre de MH dans le Musee {}".format(len(StPierre.collection)))
        print ("Nombre de MH issues de la base Mérimée {}".format(StPierre.calcul_nbMH_merimee()))
        print ("Nombre de MH issues de la base Osm {}".format(StPierre.calcul_nbMH_osm()))
        salle_merosm = StPierre.chercher_MerOsm()
        nb_salle_merosm = len(salle_merosm.collection)
        print("Nombre de MH commun à Mérimée et OSM {}".format(nb_salle_merosm))
        salle_osm = StPierre.chercher_Osm()
        nb_salle_osm = len(salle_osm.collection)
        print("Nombre de MH présents seulemnt dans OSM {}".format(nb_salle_osm))
        print ()
