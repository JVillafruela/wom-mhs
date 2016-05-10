#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html - version 2
'''
from __future__ import unicode_literals
import os,shutil
import index,merimee,overpass,wikipedia,ini,mohist
from collections import OrderedDict







if __name__ == "__main__":
    stats={}
    ''' Définir les variables d'entrée'''
    if ini.prod :
        base_url=ini.url_prod+"/Wom"
    else:
        base_url=ini.url_dev+"/Wom"
    d_dep = OrderedDict(sorted(ini.dep.items(), key=lambda t: t[0]))
    ''' Générer la page index'''
    #index.gen_page_index(d_dep)
    ''' Déplacer le fichier style.css vers la racine du site web'''
    #copier_css(base_url)
    '''générer les pages de chaque département'''
    # d= 01, 42, 69,  etc...
    for d in d_dep:
        print('------'+d+'------')
        ''' Acquérir les datas'''
        museum= mohist.Musee()
        museum= overpass.get_osm(d_dep[d]['name'],museum)
        museum= merimee.get_merimee(d_dep[d]['code'],museum)
        museum= wikipedia.get_wikipedia(d_dep[d]['url_d'],museum)
        
        # museum.maj_salle()
        # stats['mer']= museum.get_nb_MH('mer')
        # print(stats['mer'])

        # stats['osm']= museum.get_nb_MH('osm')
        # print(stats['osm'])

        museum.maj_salle()
        print(museum)
        # nb=museum.get_nb_MH('osm')
        # print(nb)
        #print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(d_dep[d]['name'],len(museum.collection)))
