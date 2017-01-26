#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2017 JeaRRo <jean.ph.navarro@gmail.com>
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
    Génération d'une page regroupant les objets OSM ayant un même code ref:mhs

    en entrée : une liste de code ref:mhs et un musée ( l'appel se fait à partir de la fonction
    gen_pages de gen_html.py )
    en sortie : une page html avec un tableau des liens pour pouvoir faire les corrections

'''
import os
import pprint

import ini
import index


def gen_head():
    head = '''<!DOCTYPE html>
    <html>
    <head>
        <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
        <title>Objets OSM multiples avec ref:mhs unique</title>
        <link rel="stylesheet" type="text/css" href="../../css/jquery-ui.min.css">
        <link rel="stylesheet" type="text/css" href="../../css/style.css" />
        <link rel="stylesheet" type="text/css" href="../../css/jquery.dataTables_mod.css"  />
        <script src="../../js/jquery.js"></script>
        <script src="../../js/jquery.dataTables.min.js"></script>
        <script src="../../js/jquery-ui.min.js"></script>
    </head>
    <script>
    $(document).ready(function(){
        $("#table_double").DataTable({
            "columnDefs": [
        {
            "targets": [ 2 ],
            "searchable": false,
            "sortable" : false,
        }],
        "order": [[ 1, 'asc' ]],
        "scrollX": true,
        "pageLength": 25,
        "language": {
                "search": "Rechercher :",
                "lengthMenu": "Voir _MENU_ monuments/page",
                "zeroRecords": "Aucun résultat pour cette recherche - désolé",
                "info": "Monuments visibles : de _START_ à _END_ sur _TOTAL_ ",
                "infoEmpty": "Aucun résultat",
                "infoFiltered": " sélectionnés parmi _MAX_ enregistrements",
                "paginate": {
                    "first":      "Première",
                    "last":       "Dernière",
                    "next":       "Suivante",
                    "previous":   "Précédente"
                    },
                    }
        });
        $("tr").click(function(){
            $("tr").each(function(){
            $(this).removeClass("selected");
            });
            $(this).addClass("selected");
        });
});
    </script>
    '''
    return head


def gen_top(dep):
    body = '''<body>
        <div id="bandeau"> <h4 class='Titre'>{} </h4></div>
        <div id="menu">
            <ul>
                <li class="retour"><a href="{}_merosmwip.html" title="" >Retour</a></li>
            </ul>
        </div>
    '''.format('', dep['code'])
    return body


def gen_table_header(dep):
    table_header = '''
    <div id="container">
    <table id="table_double" class="display nowrap" cellspacing="0" width="100%">
    <caption id='titre'> Liste des Ref:Mhs correspondant à plusieurs objets OSM du département {} </caption>
    <thead class='heading'>
        <tr>
            <th>Description</th>
            <th>Mérimée</th>
            <th>OSM</th>
            <th>lien WP</th>
        </tr>
    </thead>
    '''.format(dep['code'])
    return table_header


def get_data(MH):
    mh = MH.mhs
    # Variables Champ Description
    if 'nom' in MH.description[mh]['mer']:
        description = MH.description[mh]['mer']['commune'] + ' - <b>' + MH.description[mh]['mer']['nom'] + '</b> - ' + MH.description[mh]['mer']['adresse']
    elif 'commune' in MH.description[mh]['wip']:
        description = MH.description[mh]['wip']['commune'] + ' - <b>' + MH.description[mh]['wip']['nom'] + '</b>'
    # Variables champ Mérimée
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    # Variables champ OSM
    url_osm_org = 'href="http://www.openstreetmap.org/browse/' + MH.description[mh]['osm']['url']
    type_osm = MH.description[mh]['osm']['url'].split('/')[0]
    id_osm = MH.description[mh]['osm']['url'].split('/')[1]
    url_osm_id = 'href="http://www.openstreetmap.org/edit?editor=id&' + type_osm + '=' + id_osm
    url_josm = 'href="http://localhost:8111/load_object?objects=' + type_osm[0] + id_osm
    if 'wikipedia' in MH.description[mh]['osm']['tags_mhs']:
        url_osmwp = 'href="https://fr.wikipedia.org/wiki/' + MH.description[mh]['osm']['tags_mhs']['wikipedia']
    else:
        url_osmwp = ""
    # recherche des urls WP
    if 'url' in MH.description[mh]['wip']:
        url_wip = MH.description[mh]['wip']['url'] + "#" + MH.description[mh]['wip']['id']
    else:
        url_wip = ""
    ###############
    # Création de la table

    # description
    table = '<tr>\n'
    table += ''' <td class="desc">{}</td>'''.format(description)
    # lien Mérinée
    table += ''' <td class="lien"><a href="{}{}" target="_blank" title="La fiche dans la base Mérimée">{}</a></td>'''.format(l0, mh, mh)
    # liens OSM
    table += '''<td class="lien"><a {}" target="_blank" title="Voir sur OpenStreetMap.org"> ORG </a> -
            <a {}" target="_blank" title="Editer avec ID"> ID </a> - <a {}" target="_blank" title="Editer avec Josm"> Josm </a> </td>
            '''.format(url_osm_org, url_osm_id, url_josm)
    # lien Wikipédia
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
    table += '</tr>\n'
    # Lignes BIS #####################################
    # print(MH.description[mh]['osm']['mhs_bis'])
    for mhs in MH.description[mh]['osm']['mhs_bis']:
        # description
        description = "---------------BIS "
        table += '<tr>\n'
        table += ''' <td class="desc">{}</td>'''.format(description)
        # lien Mérimée
        # table += ''' <td> --------------- </td>'''
        table += ''' <td class="lien"><a href="{}{}" target="_blank" title="La fiche dans la base Mérimée">{}</a></td>'''.format(l0, mhs[1]['ref:mhs'], mhs[1]['ref:mhs'])

        # lien OSM
        url_org = 'href="http://www.openstreetmap.org/browse/' + mhs[0]
        # print(url_org)
        type_osm = mhs[0].split('/')[0]
        id_osm = mhs[0].split('/')[1]
        url_id = 'href="http://www.openstreetmap.org/edit?editor=id&' + type_osm + '=' + id_osm
        # print(url_id)
        url_josm = 'href="http://localhost:8111/load_object?objects=' + type_osm[0] + id_osm
        # print(url_josm)
        table += '''<td class="lien"><a {}" target="_blank" title="Voir sur OpenStreetMap.org"> ORG </a> -
                <a {}" target="_blank" title="Editer avec ID"> ID </a> - <a {}" target="_blank" title="Editer avec Josm"> Josm </a> </td>
                '''.format(url_org, url_id, url_josm)
        table += ''' <td> --------------- </td>'''
        table += '\n</tr>\n'
    return table


def gen_page_double(departement, musee, liste_doubles):
    ''' Créer une page html avec un tableau descriptif des objets multiples dans OSM
    '''
    # Créer le fichier
    name = str(departement['code']) + "_doubles.html"
    # print(name)
    oF = index.creer_fichier(name, departement)
    # Ecrire l'entete
    head = gen_head()
    oF.write(head)
    top = gen_top(departement)
    oF.write(top)
    table_header = gen_table_header(departement)
    oF.write(table_header)
    # Ecrire le tableau des doubles
    oF.write('\n<tbody>')
    for ref in liste_doubles:
        # print(musee.collection[ref])
        data = get_data(musee.collection[ref])
        oF.write(data)
    oF.write('\n</tbody> \n </table> \n</div>')
    # écrire le pied de page
    # index.write_footer(oF)
    footer = '''\n<div id="footer"> Page proposée par <a href="http://wiki.openstreetmap.org/wiki/User:JeaRRo">JeaRRo</a>, contributeur OSM </div>
        </body
    </html>
    '''
    oF.write(footer)


if __name__ == "__main__":
    departement = dep
    musee = {}
    liste_doubles = []
    print(liste_doubles)
