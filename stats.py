#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle,run,view,SimpleTemplate
import wikipedia,overpass,merimee
import requests_cache

app = Bottle()

requests_cache.install_cache('wikipedia_cache', backend='memory', expire_after=180)

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

@app.route('/status/<dep>')
@view('status.tpl')
def status(dep):
    print(type(dep),dep)
    dep_text,d_me,d_wp,d_osm = get_data(dep)
    context = {'text_departement' : dep_text, 'merimee': d_me,'wikipedia':d_wp, 'osm':d_osm }
    return context

# @app.route('/osm/<dep>')
# @view('osm1.tpl')
# def osm(dep):
#     dic_elem =overpass_v5.get_osm(dep)
#     ctr, liste_monuments = overpass_v5.mise_en_forme(dic_elem)
#
#     context ={'resultat' : "Monuments historiques du {} présents dans OSM : {}".format(dep,ctr), 'monuments': liste_monuments}
#     return context


if __name__ == "__main__":
    run(app, host='0.0.0.0', port=8080,reloader=True)
