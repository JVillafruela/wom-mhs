#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Requette sur la base OSM pour rechercher les ref:mhs d'un département

    en entrée : un code département = '01'
                Attention : le rhône est à assembler avec la Métropole de Lyon
                2 boundary level =6 différentes
    en sortie : un dico avec les clés ref:mhs renvoyant les infos de chaque monument.
                dic= { 'ref:mhs1':[lien type/id,le dico des tags, la liste des tags manquants],...}
exemple=>   PA00116550 : ['way/391391471', {'mhs:inscription_date': '1981', 'name': 'Ferme de Pérignat', 'heritage': '2', 'ref:mhs': 'PA00116550',
                        'wikipedia': 'fr:Ferme de Pérignat', 'heritage:operator': 'mhs'}, ['source']]

        FIXME => la Bbox de l'objet OSM n'est pas sauvé... geo:46.02403,4.99101?z=19 ? URl géo ?
'''

from __future__ import unicode_literals
import overpy,ini
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options
from collections import OrderedDict

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('query-osm-cache', expire=7200)
def get_data(query):
    '''
        Obtenir la selection géographique sur overpass.api
    '''
    api = overpy.Overpass()
    try :
        result = api.query(query)
    except api.OverpassGatewayTimeout:
        print ('TimeOut : Le serveur Overpass.eu ne réponds pas. Ré-essayer plus tard.')
    except api.OverpassTooManyRequests:
        print ('TooManyRequests : Trop de requêtes pour le serveur Overpass.eu. Patienter et ré-essayer plus tard.')
    else :
        #print (type(result))
        # si erreur timeout attendre un moment et recommencer (pas planter)
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
        la sortie : le dictionnaire des résultats
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

            # Si le tag mhs contient deux refs ref:mhs=PA01000012;PA01000013
            if ';' in tags_mhs["ref:mhs"]:
                dico[tags_mhs["ref:mhs"].split(';')[0]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
                dico[tags_mhs["ref:mhs"].split(';')[1]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
            else :
                dico[tags_mhs["ref:mhs"]] = [tt+'/'+str(d.id),tags_mhs,tags_manquants]
    return dico

def get_osm(departement, dic=None):
    '''
        Obtenir les objets OSM contenant le tag 'ref:mhs'
        pour un département = '01' par exemple
    '''
    dic_elements={}
    query=""
    query_part1 = '''area[admin_level=6]["name"="{}"]->.boundaryarea;
    ( node(area.boundaryarea)["ref:mhs"];
    way(area.boundaryarea)["ref:mhs"];
    relation(area.boundaryarea)["ref:mhs"]);'''

    query_end='''out meta;>;out meta;'''

    for d in departement :
        query += query_part1.format(d)
    query+=query_end
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
    departement = '69'
    # choix du dico departement
    dp = ini.dep[departement]
    print(dp.keys())
    #choix du dico de la clé departement
    dic_osm = get_osm(dp[departement])
    # if dp['zone_osm_alt']:
    #     dic_osm=get_osm(dp['zone_osm_alt'],dic_osm)
    for key in dic_osm:
        print (key,':',dic_osm[key])
    #print(dic_osm)
    print ("il y a {} Monuments du département {} dans OpenStreetMap.".format(len(dic_osm),dp['text']))
