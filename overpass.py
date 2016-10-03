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
'''
    Requette sur la base OSM pour rechercher les ref:mhs d'un département

    en entrée : un code département = '01'
                Attention : pour le Rhône est à assembler avec la Métropole de Lyon
                2 boundary (level=6) différentes
    en sortie : un musee avec les clés ref:mhs renvoyant les infos de chaque monument à partir de la clé osm
                'osm' = { 'url_osm':'lien type/id', 'tags_mhs': '{dico des tags}' , 'tags_manquants': 'liste des tags manquants', 'mhs_bis' : {osm double} }
old_exemple =>   PA00116550 : ['way/391391471', {'mhs:inscription_date': '1981', 'name': 'Ferme de Pérignat', 'heritage': '2', 'ref:mhs': 'PA00116550',
                        'wikipedia': 'fr:Ferme de Pérignat', 'heritage:operator': 'mhs'}, ['source']]

        FIXME => la Bbox de l'objet OSM n'est pas sauvé... geo:46.02403,4.99101?z=19 ? URl géo ?
'''

from __future__ import unicode_literals
import overpy,ini,mohist,time,param
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

#@cache.cache('query-osm-cache', expire=7200)
def get_data(query):
    '''
        Requete sur "http://overpass-api.de/api/interpreter" (url par default)
    '''
    # Obtenir la selection géographique sur oapi serveur français
    urlFR = u"http://api.openstreetmap.fr/oapi/interpreter"
    api = overpy.Overpass()
    api.url = urlFR
    try :
        result = api.query(query)
        #raise overpy.exception.OverpassTooManyRequests()
    except overpy.exception.OverpassTooManyRequests:
        print ('TooManyRequests : Trop de requêtes pour le serveur Overpass.eu. Patienter et ré-essayer plus tard.')
        result=None
    except overpy.exception.OverpassGatewayTimeout:
        #print ('TimeOut : Le serveur Overpass.eu ne réponds pas.')
        result=None
    # else :
    #print (type(result))
        # si erreur timeout attendre un moment et recommencer (pas planter)
    return result

def get_tags(dico):
    '''
        Détecter les tags 'Monuments Historiques' présents et absents
        dico contient tous les tags de l'objet osm
    '''
    base_tags=['ref:mhs','name','heritage','heritage:operator','mhs:inscription_date',"wikipedia"]
    source_tags=['source','source:heritage']
    tags_mhs = {}
    tags_absents = []
    if  source_tags[0] or source_tags[1] in dico:
        pass
    else :
        tags_absents.append('source')
    for tag in base_tags:
        if tag in dico:
            tags_mhs[tag] = dico[tag]
        else :
            tags_absents.append(tag)
    # print (len(tags_mhs))
    # print(tags_manquants)
    return tags_mhs,tags_absents

def add_mh(ref_mhs, data, musee):
    ''' ajouter la ref_mhs dans le musee'''
    #traitement des doubles
    if '-Bis' in ref_mhs:
        mhs_bis = ref_mhs.split('-')[0]
        # print (mhs_bis , ' ', data)
        # print(musee.collection[mhs_bis].description[mhs_bis]['osm'])
        # sauvegarde de la description bis dans un champ particulier
        musee.collection[mhs_bis].description[mhs_bis]['osm']['mhs_bis']= data
    else:
        if ref_mhs not in musee.collection :
            m=mohist.MoHist(ref_mhs)
            musee.collection[ref_mhs]=m
        #musee.collection[ref_mhs].description[ref_mhs]['osm']=data
        musee.collection[ref_mhs].description[ref_mhs]["osm"]['url_osm']=data[0]
        musee.collection[ref_mhs].description[ref_mhs]['osm']['tags_mhs']=data[1]
        musee.collection[ref_mhs].description[ref_mhs]['osm']['tags_manquants']=data[2]
        musee.collection[ref_mhs].note +=2
        #corrige la note si lien wikipédia
        if 'wikipedia' in musee.collection[ref_mhs].description[ref_mhs]['osm']['tags_mhs']:
            musee.collection[ref_mhs].note +=4
        # corrige la note si n'est pas déja dans merimée
        if not musee.collection[ref_mhs].description[ref_mhs]['mer'] :
            musee.collection[ref_mhs].note +=1


    return musee

def get_elements(data,tt,musee):
    '''
        Récupérer les éléments contenus dans 'data'
        'data' ne contient qu'un seul type : relation,way ou node (tex_typ) qui
        permettra de reconstruire le lien de l'objet sur une carte OSM
        la sortie : le musee
    '''

    tags_mhs = {}
    tags_manquants =[]

    for d in data:
        tags_mhs,tags_manquants = get_tags(d.tags)
        if 'ref:mhs' in tags_mhs:
            # Si le tag mhs contient deux refs ref:mhs=PA01000012;PA01000013
            if ';' in tags_mhs["ref:mhs"]:
                #print(tags_mhs["ref:mhs"])
                mhs= tags_mhs["ref:mhs"].split(';')[0]
                #mhs2=tags_mhs["ref:mhs"].split(';')[1] --> NON TRAITE
            else:
                mhs = tags_mhs["ref:mhs"]
            #tag mhs déjà présent dans le dico
            if mhs in musee.collection :
                if mhs in musee.collection[mhs].description:
                    if 'osm' in  musee.collection[mhs].description[mhs]:
                        # code ref:mhs identique sur deux objets OSM : ajouter le texte 'Bis' au code
                        musee.collection[mhs].description[mhs]['osm']['mhs_bis']=[tt+'/'+str(d.id),tags_mhs,tags_manquants]
                        #print(tags_mhs["ref:mhs"])
            else:
                MH=musee.add_Mh(mhs)
                MH.add_infos_osm(tt+'/'+str(d.id),tags_mhs,tags_manquants)
    return musee

def get_osm(departement,musee):
    '''
        Obtenir les objets OSM contenant le tag 'ref:mhs'
        pour un département = '01' par exemple
    '''
    dic_elements={}
    query = "[timeout:900];"
    query_part1 = '''area[admin_level=6]["name"="{}"]->.boundaryarea;
    ( node(area.boundaryarea)["ref:mhs"];
    way(area.boundaryarea)["ref:mhs"];
    relation(area.boundaryarea)["ref:mhs"]);'''
    query_end='''out meta;>;out meta;'''
    for d in departement :
        query += query_part1.format(d)
    query+=query_end
    query = ' '.join(query.replace("\n","").split())
    print("Query : ", query)
    result = get_data(query)
    ''' tester si le résulat est OK (!=None)
        sinon attendre puis refaire
    '''
    x=0
    while x<3 and result == None:
        time.sleep(60) # 1 minute
        #print('essais de {}'.format(x))
        result = get_data(query)
        x+=1
    if result == None:
        raise overpy.exception.OverPyException('Le serveur Overpass ne réponds pas.')
    #print (result.relations)
    ensemble ={'r':result.relations,'w':result.ways,'n':result.nodes}
    dic_typ = {'r':'relation','w':'way','n':'node'}
    for key in ensemble:
        #print(ensemble[key])
        musee = get_elements(ensemble[key],dic_typ[key],musee)
        #print (len(liste_elements[key]),' ',text[key]) #,liste_elements[key][0][0]
        #ctr += len(liste_elements[key])
    #dic_elements = OrderedDict(sorted(dic_elements.items(), key=lambda t: t[0]))
    return musee

if __name__ == "__main__":
    departement = '69'
    #osmWip=[]
    musee = mohist.Musee()
    #print("avant =",mohist.MoHist.ctr_monument)
    print(param.dic_dep[departement]['name'])
    musee = get_osm(param.dic_dep[departement]['name'],musee)
    #print ("apres =", mohist.MoHist.ctr_monument)
    #for mh,MH in musee.collection.items():
        #print(mh, MH)
        #for value in MH.description[mh]['osm']:
    #     #print (mh, MH.description[mh]['osm'][0], MH.note)
    print("Pour le département {}, il y a {} monuments dans la base OpenStreetMap.".format(departement,len(musee.collection)))
    musee.maj_salle()
    print(musee)


    nb=musee.get_nb_MH('osm')
    print(nb)
