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
from collections import OrderedDict
import os
import shutil
import logging
import datetime
import begin
import re
import pprint

import ini
import param
import mohist
import merimee
import overpass
import wikipedia
import index
import wkdcodes
import statistiques
import gen_doubles
import export


def get_log_date():
    return datetime.datetime.now().strftime('%Y%m%d')


def get_bandeau(dep, title, musee):
    ''' définir le bandeau de la page'''
    toCreateWp = musee.get_nb_pageToCreate()
    bandeau = '''<body>
     <div id="bandeau"> <h4 class='Titre'>{}'''.format(title)
    # bandeau+=''' <p id="msg">&nbsp;</p> '''
    # Ils sont {} dans wikipédia (pages départementales et grandes villes). {} n'ont pas de page dédiée.'''.format(dep['text'],musee.stats['mer'],musee.stats['wip'],toCreateWp)
    pagesWp = int(musee.stats['wip']) - int(toCreateWp)
    bandeau += '''</h4> <p><b>Pour le département {}</b>, la base Mérimée Ouverte décrit <b>{} </b>monuments historiques.
         <b>{} </b> d'entre eux ont une page dédiée dans Wikipédia.'''.format(dep['text'], musee.stats['mer'], str(pagesWp))

    bandeau += '''<p> OpenStreetMap connait <b>{} </b> de ces monuments.'''.format(musee.stats['osm'])
    bandeau += '''\n</div>'''
    return bandeau


def get_menu(dep, musee):
    '''Ecriture du menu'''
    menu = '<div id="menu">\n<ul>\n'
    # print(type(musee.salles))
    for salle in reversed(musee.salles):
        if len(salle.s_collection) > 0:
            link = dep["code"] + "_" + salle.salle['nom'] + ".html"
            onglet = salle.salle['onglet']
            titre_onglet = salle.salle['titre_onglet']
            nb_MH = '<span class="emphase">{}</span>'.format(str(len(salle.s_collection)))
            menu += '<li><a href="{}" title="{}" >{} {}</a></li>'.format(link, titre_onglet, nb_MH, onglet)
    menu += '<li class="retour"><a href="../../index.html" title="Autres départements" > Menu général </a></li>'
    menu += '''</ul>
        </div>'''
    return menu


def get_header():
    header = '''
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


def get_table(salle, musee):

    table = ""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    url_osm_org = url_osm_id = url_osmwp = ""
    url_josm = url_osm = url_wip = ""
    # for mh,MH in salle.s_collection.items():
    # liste des ref:mhs avec objets multiples
    double = []
    n = 0
    for mh in sorted(salle.s_collection):
        MH = musee.collection[mh]
        note_osm = "<b> Osm : </b>"
        note_wp = "<b> Wp : </b>"

        # Variables Champ Description
        if 'nom' in MH.description[mh]['mer']:
            description = MH.description[mh]['mer']['commune'] + ' - <b>' + MH.description[mh]['mer']['nom'] + '</b> - ' + MH.description[mh]['mer']['adresse']
        elif 'commune' in MH.description[mh]['wip']:
            description = MH.description[mh]['wip']['commune'] + ' - <b>' + MH.description[mh]['wip']['nom'] + '</b>'
        else:
            # print (mh)
            if 'IA' not in mh:
                commune = merimee.get_commune(mh)
                if commune == '':
                    print("Le ref:mh {} est inconnu dans Mérimée ouverte : Patrimoine Architectural".format(mh))
                    print('http://www.openstreetmap.org/browse/' + MH.description[mh]['osm']['url'])
                    logging.error("log : Le ref:mh {} est inconnu dans Mérimée ouverte : Patrimoine Architectural".format(mh))
                    logging.error("log : Voir url : http://www.openstreetmap.org/browse/{}".format(MH.description[mh]['osm']['url']))
            else:
                commune = ''
            if 'name' in MH.description[mh]['osm']['tags_mhs']:
                description = commune + ' - <b>' + MH.description[mh]['osm']['tags_mhs']['name'] + ' </b>'
            else:
                description = commune
        # Variables Champ Mérimée
            # RAS
        # Variables Champ OSM
        if 'osm' in salle.salle['nom']:
            # les urls OSM
            if 'url' in MH.description[mh]['osm']:
                url_osm_org = 'href="http://www.openstreetmap.org/browse/' + MH.description[mh]['osm']['url']
                type_osm = MH.description[mh]['osm']['url'].split('/')[0]
                id_osm = MH.description[mh]['osm']['url'].split('/')[1]
                url_osm_id = 'href="http://www.openstreetmap.org/edit?editor=id&' + type_osm + '=' + id_osm
                url_josm = 'href="http://localhost:8111/load_object?objects=' + type_osm[0] + id_osm
            # ###### les tags manquants dans OSM
            if len(MH.description[mh]['osm']['tags_manquants']) > 0:
                # Remplacer le tag manquant "wikipedia"par le lien wikipedia si présent
                if 'tag_wk' in MH.description[mh]['wip']:
                    if "wikipedia" in MH.description[mh]['osm']['tags_manquants'] and MH.description[mh]['wip']['tag_wk'] != "":
                        url_add_wp = '<a {}&addtags=wikipedia=fr:{}" target="hide" title="Ajout tag wikipedia avec Josm (Remote control)"> wikipedia </a>'.format(url_josm, MH.description[mh]['wip']['tag_wk'])
                        pos = MH.description[mh]['osm']['tags_manquants'].index("wikipedia")
                        MH.description[mh]['osm']['tags_manquants'][pos] = url_add_wp
                        # print(MH.description[mh]['wip']['tag_wk'])
                        # print(MH.description[mh]['osm']['tags_manquants'])
                # Remplacer dans les tags manquants le terme wikidata (si présent) par un lien url_josm avec ajout du qCode
                if "wikidata" in MH.description[mh]['osm']['tags_manquants'] and MH.description[mh]['wkd'] != "":
                    # print (MH.description[mh]['wkd'])
                    if len(MH.description[mh]['wkd']) == 1:
                        url_wkd = '<a {}&addtags=wikidata={}" target="hide" title="Ajout code wikidata avec Josm (Remote control)"> {} </a>'.format(url_josm, MH.description[mh]['wkd'][0], MH.description[mh]['wkd'][0])
                        MH.description[mh]['osm']['tags_manquants'][-1] = url_wkd
                    else:
                        # Multiples codes Wikidata
                        MH.description[mh]['osm']['tags_manquants'][-1] = ', '.join(MH.description[mh]['wkd'])

                note_osm += ", ".join(MH.description[mh]['osm']['tags_manquants'])
            else:
                note_osm = ""
            if MH.description[mh]['osm']['mhs_bis'] is not None:
                # Traitement des doubles
                # pprint.pprint(MH.description[mh]['osm']['mhs_bis'])
                # note_osm += ' <a href="http://www.openstreetmap.org/browse/' + MH.description[mh]['osm']['mhs_bis'][0][0] + '" target="_blank" title="Monument en double dans OSM"> Double OSM </a>'
                double.append(mh)
            # print(note_osm)
            # recherche des urls WP
            if 'wikipedia' in MH.description[mh]['osm']['tags_mhs']:
                url_osmwp = 'href="https://fr.wikipedia.org/wiki/' + MH.description[mh]['osm']['tags_mhs']['wikipedia']
            else:
                url_osmwp = ""
        # Variables champ Wikipédia
        if 'wip' in salle.salle['nom']:
            # les infos manquantes dans wikipédia
            if 'infos_manquantes' in MH.description[mh]['wip']:
                # print(MH.description[mh]['wip'])
                if len(MH.description[mh]['wip']['infos_manquantes']) > 0:
                    # print(MH.description[mh]['wip']['infos_manquantes'])
                    if "redlink" in MH.description[mh]['wip']['infos_manquantes'][0]:
                        # Page à créer avec lien
                        MH.description[mh]['wip']['infos_manquantes'][0] = '<a href="http://fr.wikipedia.org' + MH.description[mh]['wip']['infos_manquantes'][0] + '" target="_blank" title = "Page wikipédia à créer">A créer</a>'
                        note_wp += ", ".join(MH.description[mh]['wip']['infos_manquantes'])
                        # print (note_wp)
                    else:
                        note_wp += ", ".join(MH.description[mh]['wip']['infos_manquantes'])
                else:
                    note_wp += ""
            if 'mhs_ter' in MH.description[mh]['wip']:
                note_wp += ', <a href="' + MH.description[mh]['wip']['mhs_ter']['url'] + '#' + MH.description[mh]['wip']['mhs_ter']['id'] + '" target="_blank" \
                        title="Monument en triple dans WP"> Triple WP </a>'
            elif 'mhs_ter' not in MH.description[mh]['wip'] and 'mhs_bis' in MH.description[mh]['wip']:
                note_wp += ', <a href="' + MH.description[mh]['wip']['mhs_bis']['url'] + '#' + MH.description[mh]['wip']['mhs_bis']['id'] + '" target="_blank" \
                        title="Monument en double dans WP"> Double WP </a>'
            # recherche des urls WP
            if 'url' in MH.description[mh]['wip']:
                url_wip = MH.description[mh]['wip']['url'] + "#" + MH.description[mh]['wip']['id']
            else:
                url_wip = ""
    ###########################################
        # debut de la table
        table += '''<tr>'''
        # colonne description
        table += '''           <td class="desc">{}</td>'''.format(description)
        # colonne mérimée
        if 'ERR' in mh:
            table += ''' <td class="lien">  ----  </td>'''
        else:
            table += ''' <td class="lien"><a href="{}{}" target="_blank" title="La fiche dans la base Mérimée">{}</a></td>'''.format(l0, mh, mh)
        # colonne OSM
        if 'osm' in salle.salle['nom']:
            table += '''<td class="lien"><a {}" target="_blank" title="Voir sur OpenStreetMap.org"> ORG </a> -
            <a {}" target="_blank" title="Editer avec ID"> ID </a> - <a {}" target="hide" title="Editer avec Josm"> Josm </a> </td>
            '''.format(url_osm_org, url_osm_id, url_josm)

        elif 'infos_osm' in MH.description[mh]:
            table += '''<td id="info_bloc{}" class="infoBloc" data-clipboard-target="#data{}"> Tags pour OSM'''.format(n, n)
            table += '''   <div id="bloc{}" class="dialogBloc">
                            <ul><div id="data{}">{}</ul>
                        </div>'''.format(n, n, MH.description[mh]['infos_osm'])
            table += '''</td> '''
            # print(MH.description[mh]['infos_osm'])
            n += 1
        else:
            table += '''<td class="lien">  ----  </td>'''

        # colonne WP
        if url_wip and url_osmwp:
            table += '''<td class="lien"> <a href="{}" target="_blank" title="Description sur page Wp départementale">  WP1 </a> -
          <a {}" target="_blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </td>'''.format(url_wip, url_osmwp)
        elif url_wip and not url_osmwp:
            url_wip = MH.description[mh]['wip']['url'] + "#" + MH.description[mh]['wip']['id']
            table += '''<td class="lien"> <a href="{}" target="_blank" title="Description sur page Wp départementale">  WP1 </a> </td>'''.format(url_wip)
        elif not url_wip and url_osmwp:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/' + MH.description[mh]['osm']['tags_mhs']['wikipedia']
            table += '''<td class="lien">  <a {}" target="_blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </td>'''.format(url_osmwp)
        else:
            table += '''<td class="lien">  ---- </td>'''
        # table remarques OSM et WP
        if note_osm != "<b> Osm : </b>" and note_wp != "<b> Wp : </b>":
            table += '''<td class="texte"> {} </td> <td class="texte"> {} </td> '''.format(note_osm, note_wp)
        elif note_osm != "<b> Osm : </b>" and not note_wp != "<b> Wp : </b>":
            table += '''<td class="texte"> {} </td> <td class="texte"></td> '''.format(note_osm)
        elif not note_osm != "<b> Osm : </b>" and note_wp != "<b> Wp : </b>":
            table += '''<td class="texte"></td> <td class="texte"> {} </td>  '''.format(note_wp)
        else:
            table += '''<td class="texte" ></td><td class="texte"></td>  '''

        # table fin
        table += '''</tr>'''
    table += ''' </tbody>
    </table>
    <iframe name="hide" style="display: None;"></iframe>
    </div>
    '''
    return table, double


def gen_pages(dep, musee):
    ''' Effacer les fichiers du répertoire du département (supprime les fichiers anciens inutiles)'''
    index.del_files(dep)
    '''Définir le bandeau '''
    titre = "Etat comparé des monuments historiques {} ({}) dans les bases Mérimée, OSM et WikiPédia".format(dep['text'], str(dep['code']))
    bandeau = get_bandeau(dep, titre, musee)
    '''Définir le menu '''
    menu = get_menu(dep, musee)
    for page in reversed(musee.salles):
        if len(page.s_collection) > 0:
            page_name = str(dep['code']) + '_' + page.salle['nom'] + '.html'
            # print("Construction de la page  {}.".format(page_name))
            print(page)
            logging.debug(" {}".format(page))
            oF = index.creer_fichier(page_name, dep)
            titre = " Wom : Mérimée, OpenStreetMap, Wikipédia"
            index.write_entete(oF, titre)
            oF.write(bandeau)
            # corriger la classe active
            menu = menu.replace('class="active"', '')
            chercher = '<li><a href="{}"'.format(page_name)
            remplacer = '<li><a class="active" href="{}"'.format(page_name)
            menu = menu.replace(chercher, remplacer)
            oF.write(menu)
            '''écrire le contenu'''
            header = get_header().format(page.salle['titre'])
            oF.write(header)
            ''' le tableau '''
            table, doubles = get_table(page, musee)
            oF.write(table)
            # Traitement des objets multiples
            if len(doubles) > 0 and page.salle['nom'] == "merosmwip":
                name = str(dep['code']) + "_doubles.html"
                print("mhs avec objets multiples : ", doubles)
                logging.debug("Mhs avec objets multiples : {}".format(doubles))
                gen_doubles.gen_page_double(dep, musee, doubles)
                lien = "<a href='./{}' title='Monuments en double' target='blank'> Attention : monuments multiples dans OSM </a>".format(name)
                oF.write(lien)
        # # '''écrire le pied de page'''
            index.write_footer(oF)
        # # '''fermer le fichier'''
            oF.close()


@begin.start
def main(departement: 'Analyse d\'un seul département'='all', monument: 'Analyse d\'un seul monument'='all', wk: 'Importer les codes wikidata manquants dans JOSM'=False):
    '''
        Obtenir la mise à jour d'un département ou d\'une liste de département (-d code_dep, code_dep, code_dep).\n
        Obtenir le dico d'un seul monument (-d code_dep -m code_Mérimée).\n
        Importer les codes Wikidata manquants dans JOSM (--wk)\n
        Attention : pour avoir le dico d'un monument, il faut donner le code de son département.
    '''
    stats = {}
    wkdCodes = {}
    # print(departement,monument)
    if ',' in departement:
        departement = departement.split(',')
    if monument != 'all' and departement == 'all':
        print('ERREUR : Vous devez préciser un code de département.')
        exit(3)
    if monument != 'all' and not re.match('^PA[0-9]{8}', monument):
        print('ERREUR : Code monument non conforme. ')
        exit(4)

    ''' Définir les répertoires de travail et les créer s'ils n'existent pas'''
    base = os.getcwd().split('/Mhs')[0]
    if not os.path.exists(base + "/Wom"):
        os.mkdir(base + '/Wom')
    base_url = base + "/Wom"
    if not os.path.exists(base + "/Mhs/log"):
        os.mkdir(base + '/Mhs/log')
    log_url = base + "/Mhs/log"
    if not os.path.exists(base + "/Wom/mp"):
        os.mkdir(base + '/Wom/mp')
    export_url = base + '/Wom/mp'

    ''' Mise en place du fichier de log  '''
    fname = "/var/log/wom/" + get_log_date() + ".log"
    # print (fname)
    logging.basicConfig(filename=fname, format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %H:%M')

    ''' Rechercher les Qcodes sur wikidata'''
    wkdCodes = wkdcodes.get_Q_codes()

    ''' Rechercher une maj de la base Mérimée'''
    merimee.Mise_A_Jour()

    ''' Générer la page index'''
    index.gen_page_index()

    ''' Créer l'objet de statistique  et son fichier ./stats.json'''
    st = statistiques.Statistiques()
    st.fname = './stats.json'

    ''' Créer l'entête du fichier d'export csv des monuments non présents dans OSM'''
    # exportfile = "export.csv"
    # export.write_head(exportfile)
    for fichier in ini.exportfile:
        export.write_head(export_url + '/' + fichier)
    # le contenu de ce fichier est créer dans mohist.py par la fonction gen_infos_osm()

    # listdepA = [
    #     '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19',
    #     '2A', '2B', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39',
    #     '40', '41', '42', '43', '44', '45', '46', '47']
    # listdepB = [
    #     '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67',
    #     '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87',
    #     '88', '89', '90', '91', '92', '93', '94', '95']

    '''Créer la liste des départements à mettre à jour'''
    if departement == 'all':
        listDep = OrderedDict(sorted(param.dic_dep.items(), key=lambda t: t[0]))
    elif type(departement) == list:
        listDep = departement
    else:
        listDep = [departement]
    # listDep = ['88','25','48', '52']
    # listDep = listdepB
    # print (listDep)
    # print(len(listDep))
    '''Mettre à jour les pages des départements de la liste'''
    for dep in listDep:
        if dep not in param.dic_dep:
            print('Code département inconnu, Revoir votre frappe !')
            exit(0)
        ''' Trouver le nom du fichier d'export '''
        exportFile = export_url + '/' + export.get_export_filename(param.dic_dep[dep]['code'])
        # print('exportFile : ', exportFile)
        print('------' + dep + '------')
        logging.info(' ------ {} ------'.format(dep))
        ''' Acquérir les datas'''
        # print('----- Acquisition des datas ------')
        museum = mohist.Musee()
        museum = overpass.get_osm(param.dic_dep[dep]['name'], museum)
        museum = merimee.get_merimee(param.dic_dep[dep]['code'], museum)
        museum = wikipedia.get_wikipedia(param.dic_dep[dep]['url_d'], museum)
        '''Associer les qcodes de wikidata à chaque MH'''
        museum.maj_Qcodes(wkdCodes)
        ''' Trier et compter '''
        museum.maj_salle()
        ''' Rechercher les monuments de la salle merosmwip dont le code wk n'est pas intégré '''
        if wk:
            museum.searchQcodes()
            exit(6)
        else:
            pass
            # print('codes wikidata non demandés')

        # pour les salles mer et merwip générer les infos à faire apparaitre dans la popup
        # Infos à ajouter dans OSM
        for x in [1, 5]:
            museum.gen_infos_osm(x, exportFile)
        museum.maj_stats()

        pagesToCreate = museum.get_nb_pageToCreate()
        # enregistrer les stats du département et des salles
        st.addStats(dep, museum.stats, pagesToCreate, museum.statsSalles())
        # listStatSalles = museum.statsSalles()
        # print(listStatSalles)

        # print('----- Statistiques globales ------')
        print("Merimée :", museum.stats['mer'])
        logging.info("Merimée : {}".format(museum.stats['mer']))
        print("OSM :", museum.stats['osm'])
        logging.info("OSM : {}".format(museum.stats['osm']))
        print("Wikipedia :", museum.stats['wip'])
        logging.info("Wikipedia : {}".format(int(museum.stats['wip']) - int(pagesToCreate)))
        print("     ---- ")
        logging.info(" ----------------")
        # print(museum)

        print(" A ajouter dans Wp : {} pages".format(pagesToCreate))
        logging.debug("A ajouter dans Wp : {} pages".format(pagesToCreate))
        ''' Générer le Html si on ne demande pas le dico d'un monument'''
        if monument == 'all':
            gen_pages(param.dic_dep[dep], museum)

    if departement == 'all':
        # faire le total des stats et afficher
        st.totalStats()
        print(st)
        # sauvegarde stats du jour
        st.saveStats()
        # générer la page html de stat
        statistiques.genGraphes(st.getSeriePourCent(), st.getPcSeries(), st.CalculeAugmentation(), st.getTotalMerimee())

    # Afficher le contenu d'un monument
    if monument != 'all':
        print(museum.collection[monument])
    exit()


if __name__ == "__main__":
    main()
