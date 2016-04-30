#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Organisation des infos MH une class Musee qui contient une collection de monuments (MoHist)
'''
import ini,merimee,overpass,wikipedia
from collections import OrderedDict

class Musee:
    '''
        un musée/salle est une collection de monuments historiques
        un musée/salle est décrit par :
                un nom de musée ou de salle
                une collection : un dico d'objets MoHist : {'code mhs': 'objet monument','code mhs': 'objet monument'}

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

    def classer_MH(self):
        # créer les salle du musée
        noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osm','s_wip','s_osmwip','s_mer']
        list_salle=[]
        for nom_salle in noms_salle :
            # créer la salle puis faire les recherches suivants les caractéritiques voulues
            nom_salle = Musee(nom_salle)
            list_salle.append(nom_salle)
        # parcourir les monuments du musée et les ranger dans les salles
        for m,v in self.collection.items():
            #print (m, v.description[m])
            #print(liste_salle[0].collection)
            '''Créer une salle avec les MH communs à Mérimée, OSM et WP '''
            if  v.description[m]['mer'] and v.description[m]['osm'] and (v.description[m]['wip'] or "wikipedia" in v.description[m]['osm']['tags_mh']):
                list_salle[0].collection[m] = v
            ''' Créer une salle avec les MH communs à Mérimée et OSM'''
            if  v.description[m]['mer'] and v.description[m]['osm'] and not v.description[m]['wip'] and ("wikipedia" not in v.description[m]['osm']['tags_mh']):
                #print ("code=", m, v.description[m])
                list_salle[1].collection[m] = v
            ''' Créer une salle avec les MH communs à Mérimée et WP'''
            if v.description[m]['mer'] and v.description[m]['wip'] and not v.description[m]['osm'] :
                list_salle[2].collection[m] = v
            ''' Créer une salle avec les MH présents seulement dans Osm '''
            if  not v.description[m]['mer'] and v.description[m]['osm'] and not v.description[m]['wip'] and 'Bis' not in m:
                list_salle[3].collection[m] = v
            ''' Créer une salle avec les MH présents seulement dans WP '''
            if  not v.description[m]['mer'] and not v.description[m]['osm'] and (v.description[m]['wip'] or 'ERR' in m ):
                list_salle[4].collection[m] = v
            ''' Créer une salle avec les MH communs à OSM et WP '''
            if  v.description[m]['osm'] and v.description[m]['wip'] and not v.description[m]['mer']:
                list_salle[5].collection[m] = v
            ''' Créer une salle avec les MH présents seulement dans Mérimée '''
            if  not v.description[m]['osm'] and not v.description[m]['wip'] and v.description[m]['mer']:
                list_salle[6].collection[m] = v
        # trier les salles par code mh croissants
        for s in list_salle :
            s.collection = OrderedDict(sorted(s.collection.items(), key=lambda t: t[0]))
        return list_salle

class MoHist:
    '''
        Un monument historique est décrit par :
            un code MHS : code donné officiel extrait sur le site du ministère de la culture (base Mérimée)
                            ou un code d'erreur si le code précédent n'existe pas
            une description : Un dico contenant le dico obtenu par analyse de chaque base.
                            C'est regroupement des informations fournies par chaque base pour un même code mhs.
    '''
    ctr_monument=0

    def __init__(self,ref_mhs):
        if ref_mhs:
            self.mhs=ref_mhs
        # else:
        #     # self.mhs = "no_mhs_"+str(MoHist.ctr_monument)
        #     # le code d'erreur est donné dans la fonction d'analyse de la base wikipédia
        #     self.mhs = ""

        self.description={self.mhs:{"mer":{},"osm":{},"wip":{}}}
        #self.description = {"mer":{},"osm":{},"wip":{}}
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
    # si une deuxième zone, augmenter le dic_osm
    if d['zone_osm_alt']:
        dic_osm=overpass.get_osm(d['zone_osm_alt'],dic_osm)
    #ajouter un tri pour être sur que le code mhs-bis arrive après le code mhs-bis donc déja créé dans la collection
    dic_osm = OrderedDict(sorted(dic_osm.items(), key=lambda t: t[0]))
    for mhs in dic_osm:
        #traitement des doubles
        if '-Bis' in mhs:
            mhs_bis = mhs.split('-')[0]
            #print (mhs_bis)
            #print(dic_osm[mhs])
            # sauvegarde de la description bis dnas un champ particulier
            musee.collection[mhs_bis].description[mhs_bis]['osm']['mhs_bis']=dic_osm[mhs]
        else:
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
    dic_wp => {code-mhs-1 : [nom MH,commune, code insee,url_wp_departement,identifiant,infos_manquantes],
                code-mhs-2 : [nom MH,commune, code insee,url_wp_departement,identifiant,infos_manquantes],
                E-N° d'ordre : [nom MH,ville,code insee, url_wp_ville,identifiant,infos_manquantes],
                E-N° d'ordre : [nom MH,ville,code insee, url_wp_ville,identifiant,infos_manquantes]}
    exemple de dic_wp => {PA01000033' : ['Le Café français', 'Bourg-en-Bresse','01035',
    'https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse', 'Cafe_francais',[]]
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
        musee.collection[mhs].description[mhs]['wip']['infos_manquantes']=dic_wp[mhs][5]
    return musee

if __name__ == "__main__":
    bases =['mer','osm','wip']
    # Une salle va correspondre à une page_web : une sélection de MH d'une certaine catégorie
    #noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osmwip','s_osm','s_wip','s_mer']

    # print(liste_salle[0])

    # par département
    for d in ini.dep:
        liste_salle=[]
        #print(d,ini.dep[d])
        # Un musée museum par département !!
        museum = Musee(ini.dep[d][d])
        print("Nombre de MH init dans le Musee {} : {}".format(ini.dep[d]['text'],len(museum.collection)))
        # Créer les monuments du museum
        # FIXME !!! supprimer le passage par le dictionnaire dans la génération...
        museum = charge_merimee(d,museum)
        museum = charge_osm(ini.dep[d],museum)
        museum = charge_wp(ini.dep[d],museum)
        # créer les classements
        liste_salle = museum.classer_MH()

#################################################################################
        # des affichages pour tests intermédiaires
        ''' Affichage  extrait base Mérimée '''
        #print(museum.collection['PA00116330'].description['PA00116330']['mer'])
        # museum_trier=museum.trier()
        # for m,value in museum_trier.items():
        #     print(value.description[m]['mer']['commune'])


        museum_trier=museum.trier()
        # for m,value in museum_trier.items():
        #     #Affichage  double extrait base OSM
        #     if "mhs_bis" in value.description[m]['osm'] :
        #         print(" Premier Mh =", value.description[m]['osm']['url_osm']," => ","Mh en double : ", value.description[m]['osm']['mhs_bis'][0])
        #         # Affichage No code mHS base wikipédia
        #     if "ERR" in m :
        #         print(m)
        #         print(value.description[m]['wip']['nom_MH'],', ',value.description[m]['wip']['commune'])

        ''' qq stats'''
        print("Nombre de MH dans le Musee {} : {}".format(ini.dep[d]['text'],len(museum.collection)))
        for bs in bases:
            print ("Nombre de MH issues de la base {} : {}".format(bs,museum.calcul_nbMH(bs)))


        for n in range(len(liste_salle)):
            print("Nombre de MH dans la salle : {} = {}".format(liste_salle[n].nom, len(liste_salle[n].collection)))

        print (MoHist.ctr_monument, " Références traitées !")
        # for mh in museum.collection:
        #     #print(museum.collection[mh].description[mh])
        #     if mh in salle_merosmwip.collection :
        #         print(salle_merosmwip.collection[mh]['wip'])

        # for mh in salle_merosmwip.collection:
        #     print (mh,salle_merosmwip.collection[mh]['osm'] )
