#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Requette sur la base OSM pour rechercher les ref:mhs d'un département
    http://api.openstreetmap.org/api/0.6/way/67071084/full #pour la tour de guy (id=67071084)
            // Ain -> '3600007387'
            // Rhône -> 3600660056
    en entrée : un code département = '01'
    en sortie : un dico avec les clés ref:mhs renvoyant les infos de chaque monument.

    FIXME : Faire un cache sur disque pour accélérer le traitement... ?
            https://pypi.python.org/pypi/percache : Danger => cache permanent (ok pour le dev)
            à voir : https://pypi.python.org/pypi/fastcache
    FIXME : Attention, il pourrait y avoir des codes ref:mhs en double (....Ok fait....)
    FIXME : Ajouter un tri des codes ref:mhs (clés du dico)
    FIXME : il peut y avoir des objets OSM avec un code ref:mhs contenant
            deux refs : ref:mhs=PA01000012;PA01000013                (....Ok fait....)


'''
from __future__ import unicode_literals
import overpy
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from collections import OrderedDict

code = {'01':'3600007387',
        '38':'3600007437',
        '69':'3600660056',
        '69M':'3604850450',
        }

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('query-cache', expire=3600)
def get_data(query):
    '''
        Obtenir la selection géographique sur overpass.api
    '''
    api = overpy.Overpass()
    try :
        result = api.query(query)
    except OverpassGatewayTimeout:
        print ('TimeOut : Le serveur Overpass.eu ne réponds pas. Ré-essayer plus tard.')
    else :
        #print (type(result))
        return result

def get_tags(dico):
    '''
        Détecter les tags 'Monuments Historiques' présents et absents
        dico contient tous les tags de l'objet osm
    '''
    base_tags=['ref:mhs','name','heritage','heritage:operator','mhs:inscription_date','source',"wikipedia"]
    tags_mhs = {}
    tags_absents = []
    for tag in base_tags:
        if tag in dico:
            tags_mhs[tag] = dico[tag]
        else :
            tags_absents.append(tag)
    # print (len(tags_mhs))
    # print(tags_manquants)
    return tags_mhs,tags_absents

def get_elements(data,tt,dico):
    '''
        Récupérer les éléments contenus dans 'data'
        'data' ne contient qu'un seul type : relation,way ou node (tex_typ) qui
        permettra de reconstruire le lien de l'objet sur une carte OSM
        la sortie : le dictionnaire de résultats

    '''
    tags_mhs = {}
    tags_manquants =[]

    for d in data:
        tags_mhs,tags_manquants = get_tags(d.tags)
        if 'ref:mhs' in tags_mhs:
            #tag mhs déjà présent dans le dico
            if tags_mhs["ref:mhs"] in dico :
                # code ref:mhs identique sur deux objets OSM
                # ajouter le texte 'Bis' au code
                 tags_mhs["ref:mhs"] += '-Bis'
                 #print(tags_mhs["ref:mhs"])
            #tag-ter présence Trois fois ??

            # Si le tag mhs contient deux refs ref:mhs=PA01000012;PA01000013
            if ';' in tags_mhs["ref:mhs"]:
                dico[tags_mhs["ref:mhs"].split(';')[0]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
                dico[tags_mhs["ref:mhs"].split(';')[1]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
            else :
                dico[tags_mhs["ref:mhs"]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
    return dico

# def mise_en_forme(dic_elements):
#     '''
#         Recherche / Préparation pour affichage sous forme de tableau sur la page web
#     '''
#     ctr=0
#     t={'r':'relation','w':'way','n':'node'}
#     liste_monuments = []
#
#     for key in dic_elem:
#         #print (len(dic_elem[key]),' ',text[key])
#
#         for m in (dic_elem[key]):
# #exemple
# #[<class 'overpy.Way'>, 40550808, {'wikipedia': 'fr:Église Saint-Just de Lyon', 'heritage': '2', 'heritage:operator': 'mhs', 'mhs:inscription_date': '1980/12/18', 'source': 'cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre. Mise à jour : 2009', 'ref:mhs': 'PA00117799', 'name': 'Église Saint-Just'}, []]
#         #print (t[key],str(m[1]))
#             # permettra de construire le lien d'affichage de l'objet OSM
#             # ex : http://www.openstreetmap.org/relation/1635056
#             # construit la partie finale : relation,way,node/id
#             osm = t[key]+'/'+str(m[1])
#             #print lien
#             if is_tag(m[2],'name') :
#                 nom= m[2]['name']
#             else :
#                 nom=''
#             mhs= m[2]['ref:mhs']
#             if is_tag(m[2],'wikipedia'):
#                 wp = m[2]['wikipedia']
#             else :
#                 wp=''
#             monument = [nom,mhs,osm,wp,m[3]]
#             liste_monuments.append(monument)
#             #print('     ', nom,' ',mhs,' ',osm,' ',wp,' ',m[3])
#         ctr += len(dic_elem[key])
#     return ctr,liste_monuments

def get_osm(dep):
    '''
        Obtenir les objets OSM contenant le tag 'ref:mhs'
        pour un département
    '''
    
    if dep=='69':
        dep= '69M'
    dic_elements = {}
    if dep in code :
        query =(
        '''
        [out:json];area('''+code[dep]+''')->.searchArea;
        (
          node["ref:mhs"](area.searchArea);
          way["ref:mhs"](area.searchArea);
          relation["ref:mhs"](area.searchArea);
        );
        out meta;>;out meta;
        ''')
        result = get_data(query)
        #print (result.relations)
        ensemble ={'r':result.relations,'w':result.ways,'n':result.nodes}
        dic_typ = {'r':'relation','w':'way','n':'node'}
        for key in ensemble:
            #print(ensemble[key])
            dic_elements = get_elements(ensemble[key],dic_typ[key],dic_elements)
            #print (len(liste_elements[key]),' ',text[key]) #,liste_elements[key][0][0]
            #ctr += len(liste_elements[key])
        dic_elements = OrderedDict(sorted(dic_elements.items(), key=lambda t: t[0]))
        return dic_elements


if __name__ == "__main__":

    dep ='01'
    dic_osm = get_osm(dep)

    for key in dic_osm:
        print (key,':',dic_osm[key] )
    #print(dic_osm)
    print ("Monuments historiques du {} présents dans OSM : {}".format(dep,len(dic_osm)))
