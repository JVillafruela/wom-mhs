#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle,run,view,SimpleTemplate,static_file
import wikipedia,overpass,merimee
import requests_cache

app = Bottle()

requests_cache.install_cache('wikipedia_cache', backend='memory', expire_after=3600)

def table_wp_absent(dic_mer,dic_wp,dic_osm):
    '''
        Préparation de variables pour l'affichage des monuments_historiques
        Présents mérimée et OSM absents WP
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

@app.route('/')
@view('intro.tpl')
def intro():
    titre=" Statistiques comparées des monuments historiques"
    texte=" A partir de la base de données ouverte Mérimée, un tableau permet la comparaison <br> entre les monuments présents dans wikipédia et/ou dans OSM.\
            <br> Pour le moment, seul le département de l'Ain est traité."
    context = {'titre' : titre,'texte' : texte}
    return context

@app.route('/status/css/<filename>')
def server_static(filename):
    return static_file(filename, root='/home/jean/osm/monuments_historiques/Mhs/css/')

@app.route('/status/<dep>')
@view('status.tpl')
def status(dep):
    #print(type(dep),dep)
    dep_text,d_me,d_wp,d_osm = get_data(dep)
    comptes = [len(d_me),len(d_wp),len(d_osm)]

    # erreur_osm=[]
    complet = table_complet(d_me,d_wp,d_osm)
    wp_absent = table_wp_absent(d_me,d_wp,d_osm)
    context = {'text_departement' : dep_text, 'complet': complet, 'comptes':comptes, 'wp_absent': wp_absent}
    return context

if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080,reloader=True)
