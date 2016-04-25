#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Organisation des infos MH une class Musee qui contient une collection de monuments (MoHist)
'''
import ini,merimee,overpass,wikipedia
from collections import OrderedDict

class Musee:
    '''
        un musée contient des monuments historiques
        {ref_mh: objet Mohist}
    '''
    def __init__(self,nom=None):
        self.collection = {}
        if nom:
            self.nom=nom
        else:
            self.nom="Musée_général"
        #self.salle_merosmwip = Musee("merosmwip")


    def trier(self):
        '''Renvoie la collection triée'''
        return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))

    def calcul_nbMH(self,base):
        '''Renvoie le nombre de MH avec et tag 'base' (mer,osm ou wip) '''
        x=0
        for m,v in self.collection.items():
            # on ne compte pas les doubles dans osm
            if base == 'osm':
                if  v.description[m][base] and not "Bis" in m :
                    x+=1
            else:
                if  v.description[m][base]:
                    x+=1
        return x

    def classer_MH(self,list_salle):
        # parcourir les clés des monuments du musée...
        # noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osmwip','s_osm','s_wip']
        for m,v in self.collection.items():
            '''Créer une salle avec les MH communs à Mérimée, OSM et WP '''
            if  v.description[m]['mer'] and v.description[m]['osm'] and v.description[m]['wip']:
                list_salle[0].collection[m] = v.description[m]
            ''' Créer une salle avec les MH communs à Mérimée et OSM'''
            if  v.description[m]['mer'] and v.description[m]['osm']:
                list_salle[1].collection[m] = v.description[m]
            ''' Créer une salle avec les MH communs à Mérimée et WP'''
            if v.description[m]['mer'] and v.description[m]['wip']:
                list_salle[2].collection[m] = v.description[m]
            ''' Créer une salle avec les MH communs à OSM et WP '''
            if  v.description[m]['osm'] and v.description[m]['wip']:
                list_salle[3].collection[m] = v.description[m]
            ''' Créer une salle avec les MH présents seulement dans Osm '''
            if  not v.description[m]['mer'] and v.description[m]['osm'] and not v.description[m]['wip'] and 'Bis' not in m:
                list_salle[4].collection[m] = v.description[m]
            ''' Créer une salle avec les MH présents seulement dans WP '''
            if  not v.description[m]['mer'] and not v.description[m]['osm'] and v.description[m]['wip']:
                list_salle[5].collection[m] = v.description[m]
        # triée les salle par code mh croissants
        for s in list_salle :
            s.collection = OrderedDict(sorted(s.collection.items(), key=lambda t: t[0]))
            
class MoHist:
    '''
        un monument historique
    '''
    ctr_monument=0

    def __init__(self, ref_mhs=None,cat=None):
        if ref_mhs:
            self.mhs=ref_mhs
        else:
            self.mhs = "no_mhs_"+str(MoHist.ctr_monument)

        self.description={self.mhs:{"mer":{},"osm":{},"wip":{}}}
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
    return musee

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
    return musee

def charge_wp(d,musee):
    '''Créer les MH à partir du scrapping des pages départementales et grandes villes sur Wikipédia
    dic_wp => {code-mhs-1 : [nom MH,commune, code insee,url_wp_departement,identifiant],
                code-mhs-2 : [nom MH,commune, code insee,url_wp_departement,identifiant],
                E-N° d'ordre : [nnom MH,ville,code insee, url_wp_ville,identifiant],
                E-N° d'ordre : [nom MH,ville,code insee, url_wp_ville,identifiant]}
    exemple de dic_wp => {PA01000033' : ['Le Café français', 'Bourg-en-Bresse','01035', 'https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse', 'Cafe_francais']
            '''
    dic_wp = wikipedia.get_wikipedia(d['url_d'],d['url_d_2'])
    for mhs in dic_wp:
        if mhs not in musee.collection:
            m=MoHist(mhs)
            musee.collection[mhs]=m
        musee.collection[mhs].description[mhs]["wip"]['nom_MH']=dic_wp[mhs][0]
        musee.collection[mhs].description[mhs]['wip']['commune']=dic_wp[mhs][1]
        musee.collection[mhs].description[mhs]['wip']['insee']=dic_wp[mhs][2]
        musee.collection[mhs].description[mhs]['wip']['url']=dic_wp[mhs][3]
        musee.collection[mhs].description[mhs]['wip']['id']=dic_wp[mhs][4]
    return musee

if __name__ == "__main__":
    bases =['mer','osm','wip']
    # Une salle va correspondre à une page_web : une sélection de MH d'une certaine catégorie
    noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osmwip','s_osm','s_wip']
    liste_salle=[]
    for nom_salle in noms_salle :
        # créer l'objet Musee correspondant -> faire les recherches suivants les caractéritiques
        nom_salle = Musee(nom_salle)
        liste_salle.append(nom_salle)
    # print(liste_salle[0])

    # par département
    for d in ini.dep:
        #print(d,ini.dep[d])
        # Un musée museum par département !!
        museum = Musee(ini.dep[d][d])
        # Créer les monuments du museum
        # FIXME !!! supprimer le passage par le dictionnaire dans la génération...
        museum = charge_merimee(d,museum)
        museum = charge_osm(ini.dep[d],museum)
        museum = charge_wp(ini.dep[d],museum)
        # créer les classements
        museum.classer_MH(liste_salle)


#################################################################################
        # des affichages pour tests intermédiaires
        ''' Affichage  extrait base Mérimée '''
        #print(museum.collection['PA00116330'].description['PA00116330']['mer'])
        # museum_trier=museum.trier()
        # for m,value in museum_trier.items():
        #     print(value.description[m]['mer']['commune'])
        ''' Affichage  extrait base OSM'''
        # museum_trier=museum.trier()
        # for m,value in museum_trier.items():
        #     if "Bis" in m :
        #         print(m)
            #print(value.description[m]['osm']['url_osm'])
        ''' qq stats'''
        print("Nombre de MH dans le Musee {}".format(len(museum.collection)))
        for bs in bases:
            print ("Nombre de MH issues de la base {} : {}".format(bs,museum.calcul_nbMH(bs)))
        # salle_wip = museum.chercher_Wip()
        # print("Nombre de MH seulement dans WP {}".format(len(salle_wip.collection)))
        # salle_osmwip = museum.chercher_OsmWip()
        # print("Nombre de MH commun à OSM et WP {}".format(len(salle_osmwip.collection)))

        for n in range(len(liste_salle)):
            print("Nombre de MH dans la salle : {} = {}".format(liste_salle[n].nom, len(liste_salle[n].collection)))
        # salle_merosm = museum.chercher_MerOsm()
        # print("Nombre de MH commun à Mérimée et OSM {}".format(len(salle_merosm.collection)))
        # salle_osm = museum.chercher_Osm()
        # print("Nombre de MH présents seulemnt dans OSM {}".format(len(salle_osm.collection)))
        # print ()
        print (MoHist.ctr_monument)
        # for mh in museum.collection:
        #     #print(museum.collection[mh].description[mh])
        #     if mh in salle_merosmwip.collection :
        #         print(salle_merosmwip.collection[mh]['wip'])

        # for mh in salle_merosmwip.collection:
        #     print (mh,salle_merosmwip.collection[mh]['osm'] )
