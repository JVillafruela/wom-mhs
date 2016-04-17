#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    requette sur la base osm pour connaitre les mhs
    http://api.openstreetmap.org/api/0.6/way/67071084/full #pour la tour de guy (id=67071084)
            // Ain -> '3600007387'
            // Ambérieu-en-bugey -> 3600145704
            // Rhône -> 3600660056
'''
from __future__ import unicode_literals
import overpy

code = {'01':'3600007387',
        '38':'3600007437',
        '69':'3600660056',
        '69M':'3604850450',
        }
text={'r':'Relations','w':'Ways','n':'Nodes'}

api = overpy.Overpass()

def get_data(query):
    '''
        Obtenir la selection géographique sur overpass.api
    '''
    try :
        result = api.query(query)
    except OverpassGatewayTimeout:
        print ('TimeOut : Le serveur Overpass.eu ne réponds pas. Ré-essayer plus tard.')
    else :
        # file ="data_way.osm"
        # If = open(file,'r')
        # result = If.readlines()
        # If.close()
        #print (type(result))
        return result

def is_tag(dico,tag):
    return tag in dico

def test_tags(dico):
    '''
        Détecter les tags 'Monuments Historiques' absents
    '''
    base_tags=['ref:mhs','name','heritage','heritage:operator','mhs:inscription_date','source',"wikipedia"]
    tags_mhs = {}
    tags_absents = []
    for tag in base_tags:
        if is_tag(dico,tag):
            tags_mhs[tag] = dico[tag]
        else :
            tags_absents.append(tag)
    # print (len(tags_mhs))
    # print(tags_manquants)
    return tags_mhs,tags_absents

def get_elements(data):
    '''
        Récupérer les éléments contenus dans data
        data ne contient qu'un seul type d'objet : relation,way ou node
    '''
    liste_elements=[]
    tags_mhs = {}
    tags_manquants =[]
    for d in data:
        if is_tag(d.tags,'ref:mhs'):
            tags_mhs,tags_manquants = test_tags(d.tags)
            liste_elements.append([type(d),d.id,tags_mhs,tags_manquants])
    return liste_elements

def mise_en_forme(dic_elements):
    '''
        Préparation pour affichage sous forme de tableau
    '''
    ctr=0
    t={'r':'relation','w':'way','n':'node'}
    liste_monuments = []

    for key in dic_elements:
        #print (len(dic_elem[key]),' ',text[key])

        for m in (dic_elements[key]):
#exemple
#[<class 'overpy.Way'>, 40550808, {'wikipedia': 'fr:Église Saint-Just de Lyon', 'heritage': '2', 'heritage:operator': 'mhs', 'mhs:inscription_date': '1980/12/18', 'source': 'cadastre-dgi-fr source : Direction Générale des Impôts - Cadastre. Mise à jour : 2009', 'ref:mhs': 'PA00117799', 'name': 'Église Saint-Just'}, []]
        #print (t[key],str(m[1]))
            osm = t[key]+'/'+str(m[1])
            #print lien
            if is_tag(m[2],'name') :
                nom= m[2]['name']
            else :
                nom=''
            mhs= m[2]['ref:mhs']
            if is_tag(m[2],'wikipedia'):
                wp = m[2]['wikipedia']
            else :
                wp=''
            monument = [nom,mhs,osm,wp,m[3]]
            liste_monuments.append(monument)
            #print('     ', nom,' ',mhs,' ',osm,' ',wp,' ',m[3])
        ctr += len(dic_elements[key])
    return ctr,liste_monuments



def get_osm(dep):
    '''
        Obtenir les objets OSM contenant le tag 'ref:mhs'
        pour un département
    '''
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
        dic_elements = {'r':[],'w':[],'n':[]}
        for key in ensemble:
            #print(ensemble[key])
            dic_elements[key] = get_elements(ensemble[key])
            #print (len(liste_elements[key]),' ',text[key]) #,liste_elements[key][0][0]
            #ctr += len(liste_elements[key])
        return dic_elements

if __name__ == "__main__":

    dep ='01'
    liste_monuments=[]

    dic_elem = get_osm(dep)
    ctr, liste_monuments = mise_en_forme(dic_elem)
    for monument in liste_monuments:
        print (monument)


    print()
    print ("Monuments historiques du {} présents dans OSM : {}".format(dep,ctr))
