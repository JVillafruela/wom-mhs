#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 JeaRRo <jean.ph.navarro@gmail.com>
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
    Génération de pages statiques directement en html - version 3
'''
from __future__ import unicode_literals
import os,shutil,logging
import datetime
import statistiques
import begin
import re
import index,merimee,overpass,wikipedia,ini,mohist,wkdcodes,param
from collections import OrderedDict

def get_log_date():
    return datetime.datetime.now().strftime('%Y%m%d')

def get_bandeau(dep,title,musee):
    ''' définir le bandeau de la page'''
    toCreateWp = musee.get_nb_pageToCreate()
    bandeau= '''<body>
     <div id="bandeau"> <h4 class='Titre'>{}'''.format(title)
    #bandeau+=''' <p id="msg">&nbsp;</p> '''
    # Ils sont {} dans wikipédia (pages départementales et grandes villes). {} n'ont pas de page dédiée.'''.format(dep['text'],musee.stats['mer'],musee.stats['wip'],toCreateWp)
    pagesWp = int(musee.stats['wip']) - int(toCreateWp)
    bandeau+= '''</h4> <p><b>Pour le département {}</b>, la base Mérimée Ouverte décrit <b>{} </b>monuments historiques.
         <b>{} </b> d'entre eux ont une page dédiée dans Wikipédia.'''.format(dep['text'],musee.stats['mer'],str(pagesWp))

    bandeau+= '''<p> OpenStreetMap connait <b>{} </b> de ces monuments.'''.format(musee.stats['osm'])
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
    menu+='<li class="retour"><a href="../../index.html" title="Autres départements" > Menu général </a></li>'
    menu+= '''</ul>
        </div>'''
    return menu

def get_header():
    header='''
    <div id="container">
    <table id="table_data" class="display nowrap" cellspacing="0" width="100%">
    <caption id='titre'> {}</caption>
    <thead class='heading'>
        <tr>
            <th>Description</th>
            <th>Mérimée</th>
            <th>OSM</th>
            <th>WP</th>
            <th>Remarques OSM</th>
            <th>Remarques WP</th>
        </tr>
    </thead>
    <tbody>
    '''
    return header

def get_table(salle,musee):

    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    url_osm_org= url_osm_id= url_osmwp=""
    url_josm= url_osm= url_wip=""
    #for mh,MH in salle.s_collection.items():
    n=0
    for mh in sorted(salle.s_collection):
        MH=musee.collection[mh]
        note_osm="<b> Osm : </b>"
        note_wp="<b> Wp : </b>"

        # Variables Champ Description
        if 'nom' in MH.description[mh]['mer']:
            description= MH.description[mh]['mer']['commune']+' - <b>'+MH.description[mh]['mer']['nom']+'</b> - '+MH.description[mh]['mer']['adresse']
        elif 'commune' in MH.description[mh]['wip']:
             description= MH.description[mh]['wip']['commune']+' - <b>'+MH.description[mh]['wip']['nom']+'</b>'
        else :
            #print (mh)
            if 'IA' not in mh:
                commune= merimee.get_commune(mh)
                if commune == '' :
                    print("Le ref:mh {} est inconnu dans Mérimée ouverte : Patrimoine Architectural".format(mh))
                    print('http://www.openstreetmap.org/browse/'+MH.description[mh]['osm']['url'])
                    logging.debug("log : Le ref:mh {} est inconnu dans Mérimée ouverte : Patrimoine Architectural".format(mh))
                    logging.debug("log : Voir url : http://www.openstreetmap.org/browse/{}".format(MH.description[mh]['osm']['url']))
            else:
                commune= ''
            if 'name' in MH.description[mh]['osm']['tags_mhs'] :
                description= commune+' - <b>'+ MH.description[mh]['osm']['tags_mhs']['name']+' </b>'
            else:
                description= commune
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
                url_josm= 'href="http://localhost:8111/load_object?objects='+type_osm[0]+id_osm
            #les tags manquants dans OSM
            if len(MH.description[mh]['osm']['tags_manquants']) > 0:
                # Remplacer dans les tags manquants le terme wikidata (si présent) par un lien url_josm avec ajout du qCode
                if "wikidata" in MH.description[mh]['osm']['tags_manquants'] and MH.description[mh]['wkd'] != "":
                    #print (MH.description[mh]['wkd'])
                    if len(MH.description[mh]['wkd']) == 1 :
                        url_wkd = '<a {}&addtags=wikidata={}" target="__blank" title="Ajout code wikidata avec Josm (Remote control)"> {} </a>'.format(url_josm,MH.description[mh]['wkd'][0],MH.description[mh]['wkd'][0])
                        MH.description[mh]['osm']['tags_manquants'][-1] = url_wkd
                    else:
                        # Multiples codes Wikidata
                        MH.description[mh]['osm']['tags_manquants'][-1]= ', '.join(MH.description[mh]['wkd'])

                note_osm+=", ".join(MH.description[mh]['osm']['tags_manquants'])
            elif MH.description[mh]['osm']['mhs_bis'] != None :
                note_osm+=' <a href="http://www.openstreetmap.org/browse/'+MH.description[mh]['osm']['mhs_bis'][0]+'" target="_blank" title="Monument en double dans OSM"> Double OSM </a>'
            else :
                note_osm =""
            #print(note_osm)
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
                    #print(MH.description[mh]['wip']['infos_manquantes'])
                    if "redlink" in MH.description[mh]['wip']['infos_manquantes'][0] :
                        # Page à créer avec lien
                        MH.description[mh]['wip']['infos_manquantes'][0] = '<a href="http://fr.wikipedia.org'+  MH.description[mh]['wip']['infos_manquantes'][0] + '" target="_blank" title = "Page wikipédia à créer">A créer</a>'
                        note_wp+=", ".join(MH.description[mh]['wip']['infos_manquantes'])
                        #print (note_wp)
                    else:
                        note_wp+=", ".join(MH.description[mh]['wip']['infos_manquantes'])
                else:
                    note_wp+=""
            if 'mhs_ter' in MH.description[mh]['wip'] :
                note_wp+=', <a href="'+MH.description[mh]['wip']['mhs_ter']['url']+'#'+MH.description[mh]['wip']['mhs_ter']['id']+'" target="_blank" \
                        title="Monument en triple dans WP"> Triple WP </a>'
            elif 'mhs_ter' not in MH.description[mh]['wip'] and 'mhs_bis' in MH.description[mh]['wip'] :
                note_wp+=', <a href="'+MH.description[mh]['wip']['mhs_bis']['url']+'#'+MH.description[mh]['wip']['mhs_bis']['id']+'" target="_blank" \
                        title="Monument en double dans WP"> Double WP </a>'
            # recherche des urls WP
            if 'url' in MH.description[mh]['wip']:
                url_wip = MH.description[mh]['wip']['url']+"#"+MH.description[mh]['wip']['id']
            else :
                url_wip=""
    ###########################################
        #debut de la table
        table += '''<tr>'''
        #colonne description
        table+= '''           <td class="desc">{}</td>'''.format(description)
        #colonne mérimée
        if 'ERR' in mh:
            table+= ''' <td class="lien">  ----  </td>'''
        else:
            table+= ''' <td class="lien"><a href="{}{}" target="_blank" title="La fiche dans la base Mérimée">{}</a></td>'''.format(l0,mh,mh)
        #colonne OSM
        if 'osm' in salle.salle['nom']:
            table += '''<td class="lien"><a {}" target="_blank" title="Voir sur OpenStreetMap.org"> ORG </a> -
            <a {}" target="_blank" title="Editer avec ID"> ID </a> - <a {}" target="_blank" title="Editer avec Josm"> Josm </a> </td>
            '''.format(url_osm_org, url_osm_id, url_josm)

        elif 'infos_osm' in MH.description[mh]:
            table+='''<td id="info_bloc{}" class="infoBloc" > Tags pour OSM'''.format(n)
            table+='''   <div id="bloc{}" class="dialogBloc">
                            <ul>{}</ul>
                        </div>'''.format(n,MH.description[mh]['infos_osm'])
            table+='''</td> '''
            #print(MH.description[mh]['infos_osm'])
            n+=1
        else:
            table+='''<td class="lien">  ----  </td>'''

        # colonne WP
        if url_wip and url_osmwp :
            table+='''<td class="lien"> <a href="{}" target="_blank" title="Description sur page Wp départementale">  WP1 </a> -
          <a {}" target="_blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </td>'''.format(url_wip,url_osmwp)
        elif url_wip and not url_osmwp:
            url_wip = MH.description[mh]['wip']['url']+"#"+MH.description[mh]['wip']['id']
            table+='''<td class="lien"> <a href="{}" target="_blank" title="Description sur page Wp départementale">  WP1 </a> </td>'''.format(url_wip)
        elif not url_wip and url_osmwp:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+MH.description[mh]['osm']['tags_mhs']['wikipedia']
            table+='''<td class="lien">  <a {}" target="_blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </td>'''.format(url_osmwp)
        else:
            table+='''<td class="lien">  ---- </td>'''
        #table remarques OSM et WP
        if note_osm !="<b> Osm : </b>" and note_wp!="<b> Wp : </b>":
            table += '''<td class="texte"> {} </td> <td class="texte"> {} </td> '''.format(note_osm,note_wp)
        elif note_osm !="<b> Osm : </b>" and not note_wp!="<b> Wp : </b>":
            table += '''<td class="texte"> {} </td> <td class="texte"></td> '''.format(note_osm)
        elif not note_osm !="<b> Osm : </b>" and note_wp!="<b> Wp : </b>":
            table += '''<td class="texte"></td> <td class="texte"> {} </td>  '''.format(note_wp)
        else:
            table += '''<td class="texte" ></td><td class="texte"></td>  '''

        #table fin
        table+='''</tr>'''
    table+=''' </tbody>
    </table>
    </div>
    '''
    return table

def gen_pages(dep, musee):
    ''' Effacer les fichiers du répertoire du département (supprime les fichiers anciens inutiles)'''
    index.del_files(dep)
    '''Définir le bandeau '''
    titre="Etat comparé des monuments historiques {} dans les bases Mérimée, OSM et WikiPédia".format(dep['text'])
    bandeau = get_bandeau(dep, titre, musee)
    '''Définir le menu '''
    menu = get_menu(dep, musee)
    for page in reversed(musee.salles):
        if len(page.s_collection) >0:
            page_name=str(dep['code'])+'_'+page.salle['nom']+'.html'
            #print("Construction de la page  {}.".format(page_name))
            print(page)
            logging.info("log : {}".format(page))
            oF = index.creer_fichier(page_name, dep)
            titre=" Wom : Mérimée, OpenStreetMap, Wikipédia"
            index.write_entete(oF, titre)
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
        # # '''écrire le pied de page'''
            index.write_footer(oF)
        # # '''fermer le fichier'''
            oF.close()

@begin.start
def main(departement:'Analyse d\'un seul département'='all',monument:'Analyse d\'un seul monument'='all'):
    '''
        Obtenir la mise à jour d'un département ou d\'une liste de département (-d code_dep,code_dep,code_dep). Obtenir le dico d'un seul monument (-d code_dep -m code_Mérimée). Attention : pour avoir le dico d'un monument,
        il faut donner le code de son département.
    '''
    stats={}
    wkdCodes = {}
    #print(departement,monument)
    if ',' in departement :
        departement = departement.split(',')
    if monument != 'all' and departement == 'all':
        print('ERREUR : vous devez préciser un code de département.')
        exit(3)
    if monument != 'all' and not re.match('^PA[0-9]{8}', monument) :
        print ('ERREUR : Code monument non conforme. ')
        exit(4)
    ''' Définir les variables d'entrée'''
    if ini.prod :
        base_url = ini.url_prod+"/Wom"
        log_url = ini.url_prod+"/Mhs/log"
    else:
        base_url=ini.url_dev+"/Wom"
        log_url = ini.url_dev+"/Mhs/log"

    ''' Mise en place du fichier de log  '''
    fname = log_url+"/wom_"+get_log_date()+".log"
    #print (fname)
    logging.basicConfig(filename=fname,format='%(asctime)s %(levelname)s: %(message)s',level=logging.DEBUG,datefmt='%m/%d/%Y %H:%M')

    ''' Rechercher les Qcodes sur wikidata'''
    wkdCodes = wkdcodes.get_Q_codes()

    ''' Rechercher une maj de la base Mérimée'''
    merimee.get_maj_base_merimee()

    ''' Générer la page index'''
    index.gen_page_index()

    ''' Créer l'objet de statistique  et son fichier ./stats.json'''
    st = statistiques.Statistiques()
    st.fname = './stats.json'

    '''Créer la liste des départements à mettre à jour'''
    if departement == 'all':
        listDep = OrderedDict(sorted(param.dic_dep.items(), key=lambda t: t[0]))
    #listDep = ['88','25','48', '52']
    elif type(departement) == list :
        listDep = departement
    else :
        listDep = [departement]
    #print (listDep)
    # print(len(listDep))
    '''Mettre à jour les pages des départements de la liste'''
    for dep in listDep :
        print('------'+dep+'------')
        logging.info('log : ------ {} ------'.format(dep))
        ''' Acquérir les datas'''
        #print('----- Acquisition des datas ------')
        museum= mohist.Musee()
        museum= overpass.get_osm(param.dic_dep[dep]['name'],museum)
        museum= merimee.get_merimee(param.dic_dep[dep]['code'],museum)
        museum= wikipedia.get_wikipedia(param.dic_dep[dep]['url_d'],museum)
        '''Associer les qcodes de wikidata à chaque MH'''
        museum.maj_Qcodes(wkdCodes)
        ''' Trier et compter '''
        museum.maj_salle()
        # pour les salles mer et merwip générer les infos à faire apparaitre dans la popup
        # Infos à ajouter dans OSM
        for x in [1,5]:
            museum.gen_infos_osm(x)
        museum.maj_stats()

        pagesToCreate = museum.get_nb_pageToCreate()
        # enregistrer les stats du département et des salles
        st.addStats(dep,museum.stats,pagesToCreate,museum.statsSalles())
        # listStatSalles = museum.statsSalles()
        # print(listStatSalles)
        #st.addStatsSalles(dep, museum.statsSalles())
        #print('----- Statistiques globales ------')
        print("Merimée :",museum.stats['mer'])
        logging.info("log : Merimée : {}".format(museum.stats['mer']))
        print("OSM :",museum.stats['osm'])
        logging.info("log : OSM : {}".format(museum.stats['osm']))
        print("Wikipedia :",museum.stats['wip'])
        logging.info("log : Wikipedia : {}".format(museum.stats['wip']))
        print("     ---- ")
        logging.info("log : ----------------")
        #print(museum)

        print (" A ajouter dans Wp : {} pages".format(pagesToCreate))
        logging.info("log : A ajouter dans Wp : {} pages".format(pagesToCreate))
        ''' Générer le Html si on ne demande pas le dico d'un monument'''
        if monument == 'all' :
            gen_pages(param.dic_dep[dep],museum)

    if departement == 'all' :
        # faire le total des stats et afficher
        st.totalStats()
        print (st)

        #générer la page html de stat
        #statistiques.gen_graphe(st.get_series())
        # générer la page de stats par departement
        #statistiques.gen_graphe2(st.getSeriePourCent(st.getLastDate()))
        #statistiques.gen_graphe3(st.getPcSeries())
        statistiques.genGraphes(st.getSeriePourCent(),st.getPcSeries(),st.CalculeAugmentation())
        #sauvegarde stats du jour
        st.saveStats()
    # Afficher le contenu d'un monument
    if monument != 'all' :
        print(museum.collection[monument])
    exit()

if __name__ == "__main__":
    main()
