#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html - version 2
'''
from __future__ import unicode_literals
import os,shutil
import index,merimee,overpass,wikipedia,ini,mohist
from collections import OrderedDict

def get_bandeau(dep,title,musee):
    ''' définir le bandeau de la page'''

    bandeau= '''<body>
     <div id="bandeau"> <h4 class='Titre'>{}'''.format(title)
    bandeau+= '''</h4> <p><b>Pour le département {}</b>, la base Mérimée Ouverte décrit {} monuments historiques.</p>
         <p>Ils sont {} dans wikipédia (pages départementales), et OSM en connait {}.</p>'''.format(dep['text'],musee.stats['mer'],musee.stats['wip'],musee.stats['osm'])
    bandeau+= '''\n</div>'''
    return bandeau

def get_menu(dep, musee):
    '''Ecrirure du menu'''
    menu='<div id="menu">\n<ul>\n'
    print(type(musee.salles))
    for salle in reversed(musee.salles):
        if len(salle.s_collection) >0:
            link = dep["code"]+"_"+salle.salle['nom']+".html"
            onglet= salle.salle['onglet']
            titre_onglet=salle.salle['titre_onglet']
            nb_MH='<span class="emphase">{}</span>'.format(str(len(salle.s_collection)))
            menu += '<li><a href="{}" title="{}" >{} {}</a></li>'.format(link, titre_onglet, nb_MH, onglet)
    menu+='<li class="retour"><a href="../index.html" title="Autres départements" > Menu général </a></li>'
    menu+= '''</ul>
        </div>
     </div>'''
    return menu

def get_header():
    header='''
    <div class="TableComplet" >
    <div class="TableTitre"> {}</div>
    <div class="TableHeading">
        <div class="TableHead2">    Description</div>
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead12">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead3">    Remarques : erreurs ou manques </div>
    </div>
    <div class="TableBody">
    '''
    return header

def gen_pages(dep, musee):
    '''Définir le bandeau '''
    titre="Etat comparé des monuments historiques {} dans les bases Mérimée, OSM et WikiPédia".format(d_dep[d]['text'])
    bandeau = get_bandeau(dep, titre, musee)
    '''Définir le menu '''
    menu = get_menu(dep, musee)
    for page in reversed(musee.salles):
        page_name=str(dep['code'])+'_'+page.salle['nom']+'.html'
        print("Construction de la page  {}.".format(page_name))
        oF = index.creer_fichier(page_name, dep)
        titre=" Wom : Mérimée, OpenStreetMap, Wikipédia"
        index.write_entete(oF, titre, "../"+ini.cssFile)
        oF.write(bandeau)
        #corriger la classe active
        menu=menu.replace('class="active"','')
        chercher= '<li><a href="{}"'.format(page_name)
        remplacer= '<li><a class="active" href="{}"'.format(page_name)
        menu=menu.replace(chercher, remplacer)
        oF.write(menu)
        '''écrire le contenu'''
        header=get_header().format(page.salle['titre'])
        oF.write(header)
    # # write_contenu(oF,stats,salle)
    # # '''écrire le pied de page'''
    # index.write_footer(oF)
    # # '''fermer le fichier'''
        oF.close()


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
        ''' Trier et compter '''
        museum.maj_salle()
        museum.maj_stats()
        print('----- Statistiques globales ------')
        print("Merimée :",museum.stats['mer'])
        print("OSM :", museum.stats['osm'])
        print("wikipedia :",museum.stats['wip'])

        #print(museum)
        ''' Générer le Html'''
        gen_pages(d_dep[d],museum)
