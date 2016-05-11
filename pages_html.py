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
    '''Ecriture du menu'''
    menu='<div id="menu">\n<ul>\n'
    #print(type(musee.salles))
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

def get_table(salle,musee):

    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    url_osm_org= url_osm_id= url_osmwp=""
    url_josm= url_osm= url_wip=""
    #for mh,MH in salle.s_collection.items():
    for mh in sorted(salle.s_collection):
        MH=musee.collection[mh]
        note_osm="-Osm: "
        note_wp="-Wp: "
        # Variables Champ Description
        if 'nom' in MH.description[mh]['mer']:
            description= MH.description[mh]['mer']['commune']+' - <b>'+MH.description[mh]['mer']['nom']+'</b> - '+MH.description[mh]['mer']['adresse']
        elif 'commune' in MH.description[mh]['wip']:
             description= MH.description[mh]['wip']['commune']+' - <b>'+MH.description[mh]['wip']['nom']+'</b>'
        else :
            description= ' <b>'+ MH.description[mh]['osm']['tags_mhs']['name']+' </b>'
        # Variables Champ Mérimée
            # RAS
        # Variables Champ OSM
        if 'osm' in salle.salle['nom']:
            # les urls OSM
            if 'url' in MH.description[mh]['osm']:
                url_osm_org='href="http://www.openstreetmap.org/browse/'+MH.description[mh]['osm']['url']
                type_osm = MH.description[mh]['osm']['url'].split('/')[0]
                id_osm = MH.description[mh]['osm']['url'].split('/')[1]
                url_osm_id ='href="http://www.openstreetmap.org/edit?editor=id&'+type_osm+'='+id_osm
                url_josm= 'href="http://localhost:8111/load_object?new_layer=true&objects='+type_osm[0]+id_osm
            #les tags manquants dans OSM
            if len(MH.description[mh]['osm']['tags_manquants'])>0:
                note_osm+=", ".join(MH.description[mh]['osm']['tags_manquants'])
            elif MH.description[mh]['osm']['mhs_bis'] != None :
                note_osm+=' <a href="http://www.openstreetmap.org/browse/'+MH.description[mh]['osm']['mhs_bis'][0]+'" target="blank" title="Monument en double dans OSM"> Double OSM </a>'
            else :
                note_osm =""
            # recherche des urls WP
            if 'wikipedia' in MH.description[mh]['osm']['tags_mhs']:
                url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+MH.description[mh]['osm']['tags_mhs']['wikipedia']
            else :
                url_osmwp =""
        # Variables champ Wikipédia
        if 'wip' in salle.salle['nom'] :
            #les infos manquantes dans wikipédia
            if 'infos_manquantes' in MH.description[mh]['wip']:
                #print(MH.description[mh]['wip'])
                if len(MH.description[mh]['wip']['infos_manquantes'])>0:
                    note_wp+=", ".join(MH.description[mh]['wip']['infos_manquantes'])
                else:
                    note_wp=""
            # recherche des urls WP
            if 'url' in MH.description[mh]['wip']:
                url_wip = MH.description[mh]['wip']['url']+"#"+MH.description[mh]['wip']['id']
            else :
                url_wip=""
    ###########################################
        #debut de la table
        table += '''<div class="TableRow">'''
        #colonne description
        table+= '''           <div class="TableCell2">{}</div>'''.format(description)
        #colonne mérimée
        if 'ERR' in mh:
            table+= ''' <div class="TableCell1">  ----  </div>'''
        else:
            table+= ''' <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>'''.format(l0,mh,mh)
        #colonne OSM
        if 'osm' in salle.salle['nom']:
            table += '''<div class="TableCell12"><a {}" target="blank" title="Voir sur openstreetmap.org"> ORG </a> -
            <a {}" target="blank" title="Editer avec ID"> ID </a> - <a {}" target="blank" title="Editer avec Josm"> Josm </a> </div>
            '''.format(url_osm_org, url_osm_id, url_josm)
        else:
            table+='''<div class="TableCell12">  ----  </div>'''

        # colonne WP
        if url_wip and url_osmwp :
            table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> -
          <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_wip,url_osmwp)
        elif url_wip and not url_osmwp:
            url_wip = MH.description[mh]['wip']['url']+"#"+MH.description[mh]['wip']['id']
            table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> </div>'''.format(url_wip)
        elif not url_wip and url_osmwp:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+MH.description[mh]['osm']['tags_mhs']['wikipedia']
            table+='''<div class="TableCell1">  <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_osmwp)
        else:
            table+='''<div class="TableCell1">  ---- </div>'''
        #table note OSM
        if note_osm !="-Osm: ":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_osm)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table note WP
        if note_wp !="" and not note_wp=="-Wp: ":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_wp)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table fin
        table+='''</div>'''
    return table

def gen_pages(dep, musee):
    '''Définir le bandeau '''
    titre="Etat comparé des monuments historiques {} dans les bases Mérimée, OSM et WikiPédia".format(d_dep[d]['text'])
    bandeau = get_bandeau(dep, titre, musee)
    '''Définir le menu '''
    menu = get_menu(dep, musee)
    for page in reversed(musee.salles):
        if len(page.s_collection) >0:
            page_name=str(dep['code'])+'_'+page.salle['nom']+'.html'
            print("Construction de la page  {}.".format(page_name))
            print(page)
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
            ''' le tableau '''
            table = get_table(page,musee)
            oF.write(table)
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
        #print('----- Acquisition des datas ------')
        museum= mohist.Musee()
        museum= overpass.get_osm(d_dep[d]['name'],museum)
        museum= merimee.get_merimee(d_dep[d]['code'],museum)
        museum= wikipedia.get_wikipedia(d_dep[d]['url_d'],museum)
        ''' Trier et compter '''
        museum.maj_salle()
        museum.maj_stats()
        #print('----- Statistiques globales ------')
        print("Merimée :",museum.stats['mer'])
        print("OSM :", museum.stats['osm'])
        print("wikipedia :",museum.stats['wip'])

        #print(museum)
        ''' Générer le Html'''
        gen_pages(d_dep[d],museum)
