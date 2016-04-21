#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Produire les comparaisons des bases
    et renvoyer les datas pour les tableaux html
'''
import os,index,merimee,overpass,wikipedia

def table_wp_absent(dic_mer,dic_wp,dic_osm):
    '''
        Préparation de variables pour l'affichage des monuments_historiques
        Présents mérimée et OSM, absents WP
    '''
    data=[]
    d=[]
    double = False
    for mhs,value in dic_mer.items():
        if mhs in dic_osm and mhs not in dic_wp:
            url_osm_part2 = dic_osm[mhs][0]
            tags_absents = dic_osm[mhs][-1]
            url_osm_part2_2=""
            tags_absents_2 =[]
            if mhs+"-Bis" in dic_osm:
                double =True
                url_osm_part2_2 = dic_osm[mhs+"-Bis"][0]
                tags_absents_2 = dic_osm[mhs+"-Bis"][-1]
            d = [mhs,value[1],value[2],url_osm_part2,tags_absents,double,url_osm_part2_2,tags_absents_2]
            if d:
                data.append(d)
                double = False
    return data

def table_complet(dic_mer,dic_wp,dic_osm):
    '''
        Préparation des variables pour affichage de la table des monuments complets
    '''
    double = False
    data=[]
    d=[]
    for mhs,value in dic_mer.items():
        if mhs in dic_osm and mhs in dic_wp:
            url_osm_part2 = dic_osm[mhs][0]
            tags_absents = dic_osm[mhs][-1]
            url_osm_part2_2=""
            tags_absents_2 =[]
            if mhs+"-Bis" in dic_osm:
                double =True
                url_osm_part2_2 = dic_osm[mhs+"-Bis"][0]
                tags_absents_2 = dic_osm[mhs+"-Bis"][-1]
            url_wp_part2=dic_wp[mhs][2]+"#"+dic_wp[mhs][3]
            d = [mhs,value[1],value[2],url_osm_part2,tags_absents,double,url_osm_part2_2,tags_absents_2,url_wp_part2]
            if d:
                data.append(d)
                double = False
    return data

def get_data(dep):
    '''
        A partir du code d'un département, interroge les trois bases, et renvoie trois dictionnaires
        et un texte titre du département
    '''
    dic_mer = merimee.get_merimee(dep)
    dep_text, dic_wp = wikipedia.get_wikipedia(dep)
    dic_osm = overpass.get_osm(dep)
    return dep_text,dic_mer,dic_wp,dic_osm

if __name__ == "__main__":
    #d_dep ={'01':'Ain', '69':'Rhône','42':'Loire'}
    d_dep ={'01':'Ain'}
    d_fonct= {'merosmwip': table_complet,
                'merosm' : table_wp_absent,
            }

    ''' tester la présence d'une génération précédente et faire une sauvegarde'''
    ''' tester l'espace disque minimum requis pour la génération... qq Mo ?'''
    ''' Générer la page index'''
    #index.gen_index(d_dep)
    '''générer les six pages de chaque département'''
    for d in d_dep:
        print('------'+d+'------')
        ''' '''
        ''' Acquérir les datas'''
        dep_text,d_me,d_wp,d_osm=get_data(d)
        comptes = [len(d_me),len(d_wp),len(d_osm)]
        #pages=['merosmwip','merosm','merwip','oemwip','osm','wip']
        pages=['merosmwip']
        ''' pour chaque page in pages:'''
        for p in pages:

            result =  d_fonct[p](d_me,d_wp,d_osm)
            print (p,result)
            ''' ouvrir le fichier(pname) et Créer/vérifier les répertoires ./d
                s'il n'existe pas
            '''
            pname=d+'_'+p+'.html'
            '''écrire l'entête'''
            '''écrire le bandeau'''
            '''écrire le menu'''
            '''écrire le contenu'''
            '''écrire le pied de page'''
            ''' fermer le fichier'''
