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

        self.salles=[Salle("vrac",'Monuments historiques non classés'),
                    Salle("mer",'Monuments historiques présents seulement dans Mérimée'),
                    Salle("osm",'Monuments historiques présents seulement dans OpenStreetMap'),
                    Salle("merosm", 'Monuments historiques présents dans Mérimée et OpenStreetMap'),
                    Salle("wip", 'Monuments historiques présents seulement dans wikipédia'),
                    Salle("merwip", 'Monuments historiques présents dans Mérimée et Wikipédia',),
                    Salle("osmwip", 'Monuments historiques présents dans OpenStreetMap et Wikipédia'),
                    Salle("merosmwip", 'Monuments historiques présents dans Mérimée, OpenStreetMap et Wikipédia')]

    def __repr__(self):
        #contenu = [salle.collection] for salle in self.salles if len(salle.collection)>0]
        result=""
        for salle in self.salles:
            if len(salle.collection)>0 :
                result += salle.salle['nom']+str(salle.collection)+'\n'
        return result

    def add_Mh(self,ref):
        if self.has_Mh(ref):
            MH = self.get_Mh(ref)
        else:
            MH=MoHist(ref)
            self.collection[ref]=MH
            #ajouter la ref du monument dans la salle en fonction de sa note
        #self.salles[MH.note].collection.append(ref)
        return MH

    def maj_salle(self):
        # raz
        for s in self.salles:
            s.collection=[]
        # mise à jour
        for ref, MH in self.collection.items():
            self.salles[MH.note].collection.append(ref)

    # def move_Mh(self, monument, old_salle):
    #     new_salle= monument.note
    #     old_salle=int(old_salle)
    #     ref= monument.mhs
    #     del self.salles[old_salle].collection[ref]
    #     #monument.note=new_salle
    #     self.salles[new_salle].collection[ref]= monument
    #     #MH.salle=new_salle

    def get_Mh(self, ref):
        ''' Renvoie le monument de la ref '''
        return self.collection[ref]

    def has_Mh(self,ref):
        return ref in self.collection

    # def trier(self):
    #     '''Renvoie la collection triée'''
    #     return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))
    #
    # def calcul_nbMH(self,base):
    #     '''Renvoie le nombre de MH avec et tag 'base' (mer,osm ou wip) '''
    #     x=0
    #     for m,v in self.collection.items():
    #         # on ne compte pas les doubles dans osm
    #         if base == 'osm':
    #             if  v.description[m][base] and not "Bis" in m :
    #                 x+=1
    #         else:
    #             if  v.description[m][base]:
    #                 x+=1
    #     return x
    #
    # def classer_MH(self):
    #     # créer les salle du musée
    #     noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osm','s_wip','s_osmwip','s_mer']
    #     list_salle=[]
    #     for nom_salle in noms_salle :
    #         # créer la salle puis faire les recherches suivants les caractéritiques voulues
    #         nom_salle = Musee(nom_salle)
    #         list_salle.append(nom_salle)
    #     # parcourir les monuments du musée et les ranger dans les salles
    #     for m,v in self.collection.items():
    #         #print (m, v.description[m])
    #         #print(liste_salle[0].collection)
    #         '''Créer une salle avec les MH communs à Mérimée, OSM et WP '''
    #         if  v.description[m]['mer'] and v.description[m]['osm'] and (v.description[m]['wip']
    #                 or "wikipedia" in v.description[m]['osm']['tags_mh']) or \
    #                 (not v.description[m]['mer'] and not v.description[m]['wip'] and "IA" in v.description[m]['osm']['tags_mh']['ref:mhs']
    #                 and  "wikipedia" in v.description[m]['osm']['tags_mh']):
    #             list_salle[0].collection[m] = v
    #         ''' Créer une salle avec les MH communs à Mérimée et OSM'''
    #         if  v.description[m]['mer'] and v.description[m]['osm'] and not v.description[m]['wip'] and ("wikipedia" not in v.description[m]['osm']['tags_mh']):
    #             #print ("code=", m, v.description[m])
    #             list_salle[1].collection[m] = v
    #         ''' Créer une salle avec les MH communs à Mérimée et WP'''
    #         if (v.description[m]['mer'] and v.description[m]['wip'] and not v.description[m]['osm']) or \
    #             ( not v.description[m]['mer'] and v.description[m]['wip'] and "IA" in m) :
    #             list_salle[2].collection[m] = v
    #         ''' Créer une salle avec les MH présents seulement dans Osm '''
    #         if  not v.description[m]['mer'] and v.description[m]['osm'] and not v.description[m]['wip'] and 'Bis' not in m \
    #              and not (not v.description[m]['mer'] and not v.description[m]['wip'] and "IA" in v.description[m]['osm']['tags_mh']['ref:mhs']
    #             and  "wikipedia" in v.description[m]['osm']['tags_mh']):
    #             list_salle[3].collection[m] = v
    #         ''' Créer une salle avec les MH présents seulement dans WP '''
    #         if  not v.description[m]['mer'] and not v.description[m]['osm'] and (v.description[m]['wip'] or 'ERR' in m ) \
    #         and (v.description[m]['wip'] and not "IA" in m) :
    #             list_salle[4].collection[m] = v
    #         ''' Créer une salle avec les MH communs à OSM et WP '''
    #         if  v.description[m]['osm'] and v.description[m]['wip'] and not v.description[m]['mer']:
    #             list_salle[5].collection[m] = v
    #         ''' Créer une salle avec les MH présents seulement dans Mérimée '''
    #         if  not v.description[m]['osm'] and not v.description[m]['wip'] and v.description[m]['mer']:
    #             list_salle[6].collection[m] = v
    #     # trier les salles par code mh croissants
    #     for s in list_salle :
    #         s.collection = OrderedDict(sorted(s.collection.items(), key=lambda t: t[0]))
    #     return list_salle

class Salle:

    def __init__(self,nom,titre):
        #l'id sera la note de classement ?
        self.salle ={"nom": nom, "titre": titre}
        #la liste de ref:mhs
        self.collection = []

    def __repr__(self):
        return("Classe "+self.salle['nom']+" : "+str(len(self.collection)))+" Monument"

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

    ctr_monument=0

    def __init__(self,ref_mhs):
        self.mhs=ref_mhs
        self.description={self.mhs:{"mer":{},"osm":{},"wip":{}}}
        self.note = 0

        MoHist.ctr_monument+=1

    def __repr__(self):
        return "ref: "+self.mhs+' classé dans : '+ str(self.note)

    def add_infos_mer(self, insee, commune, adresse, nom, classement):
        self.description[self.mhs]['mer'] = {'insee' : insee,
                                             'commune': commune,
                                             'adresse': adresse,
                                             'nom': nom,
                                             'classement': classement }
        self.note+=1

    def add_infos_osm(self, url, tag_mhs, tags_absents, mhs_bis=None ):
        self.description[self.mhs]['osm'] = {'url': url,
                                             'tags_mhs': tag_mhs,
                                             'tags_absents': tags_absents,
                                             'mhs_bis': mhs_bis}
        self.note+=2
        #correction si présence lien vers wikipédia
        if 'wikipedia' in self.description[self.mhs]['osm']['tags_mhs']:
            #self.add_url_wip(self.description[self.mhs]['osm']['tags_mhs']['wikipedia'])
            self.note+=4
        #correction si mhs n'est pas dans mérimée
        if not self.description[self.mhs]['mer']:
            self.note+=1

    def add_infos_wip(self, insee, commune, nom, url, id, infos_manquantes):
        self.description[self.mhs]['wip'] = {'insee': insee,
                                             'commune': commune,
                                             'nom': nom,
                                             'url': url,
                                             'id': id,
                                             'infos_manquantes': infos_manquantes,}
        self.note+=4


def charge_wp(d,musee):
    '''Créer les MH à partir du scrapping des pages départementales et grandes villes sur Wikipédia
    dic_wp => {code-mhs-1 : [nom MH,commune, code insee,url_wp_departement,identifiant,infos_manquantes],
                code-mhs-2 : [nom MH,commune, code insee,url_wp_departement,identifiant,infos_manquantes],
                E-N° d'ordre : [nom MH,ville,code insee, url_wp_ville,identifiant,infos_manquantes],
                E-N° d'ordre : [nom MH,ville,code insee, url_wp_ville,identifiant,infos_manquantes]}
    exemple de dic_wp => {PA01000033' : ['Le Café français', 'Bourg-en-Bresse','01035',
    'https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse', 'Cafe_francais',[]]
            '''
    dic_wp = wikipedia.get_wikipedia(d['url_d'])
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
        musee=Musee()

        mhs='AP123456'
        m=musee.add_Mh(mhs)
        m.add_infos_mer('01004','ambérieu en Bugey','9 rue truchon','Maison Navarro', 'classé : 1928')

        print(musee)

        mhs2='AP456789'
        # if musee.has_Mh(mhs2):
        #     #print(mhs, " : Présent")
        #     #récupérer le monument existant
        #     MH = musee.get_Mh(mhs2)
        #     # print(type(MH))
        #     # print(MH)
        #     #modifier le monument existant
        #     MH.add_infos_osm('way/124578',{'name':'église de la gare', 'ref:mhs': 'AP456789', 'heritage':'3', 'wikipedia':'fr:wiki/église'},['source',])
        #     #print(MH)
        # else:
        #     #créer le monument
        #     m=MoHist(mhs2)
        #     #ajouter les infos
        #     m.add_infos_osm('node/124578',{'name':'gare sncf', 'ref:mhs': 'AP123456', 'heritage':'2'},[])
        #     #le mettre dans le musée
        #     musee.add_Mh(mhs2,m)
        m= musee.add_Mh(mhs2)
        m.add_infos_osm('way/124578',{'name':'église de la gare', 'ref:mhs': 'AP456789', 'heritage':'3', 'wikipedia':'fr:wiki/église'},['source',])
        m= musee.add_Mh(mhs)
        m.add_infos_osm('way/124578',{'name':' gare', 'ref:mhs': 'AP123456', 'heritage':'3'},['wikipedia',])
        print(musee)
        for ref in musee.collection:
            print (musee.collection[ref])
        musee.maj_salle()
        print(musee)
        # mhs2='AP456789'
        # monu2=MoHist(mhs2)
        # monu2.add_infos_osm('way/124578',{'name':'église de la gare', 'ref:mhs': 'AP456789', 'heritage':'3', 'wikipedia':'fr:wiki/église'},['source',])
        # musee.add_Mh(monu2)
        #
        # mhs3='AP123456'
        # if musee.contient(mhs3):
        #     index= musee.get_salle_de_mh(mhs3)
        #     print (index)
        #     print (salle, Mh)
        #     Mh.add_infos_osm('node/124578',{'name':'gare sncf', 'ref:mhs': 'AP123456', 'heritage':'2'},[])
        #     musee.move_MH(Mh,salle)
        # else :
        #     monu3=MoHist(mhs3)
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
