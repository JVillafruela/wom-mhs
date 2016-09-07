#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 JeaRRo <jean.navarro@laposte.net>
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
    Génération de pages statiques directement en html

'''
import os,ini,time
from collections import OrderedDict

def write_entete_index(file, title):
    '''
        Ecrire l'entête du fichier html
    '''
    header=""
    header += '''<!DOCTYPE html>
    <html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
    <title>{}</title>\n\t'''.format(title)
    header+='''<link rel="stylesheet" type="text/css" href="css/style.css" />'''
    header+='''   </head>'''
    file.write(header)

def write_entete(file, title) :
    '''
        Ecrire l'entête du fichier html
    '''
    header=""
    header += '''<!DOCTYPE html>
    <html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
    <title>{}</title>\n\t'''.format(title)
    #header+='''<link rel="stylesheet" type="text/css" href="{}">\n\t'''.format(cssFile)
    header+='''<link rel="stylesheet" type="text/css" href="../css/jquery-ui.css">
	           <link rel="stylesheet" type="text/css" href="../css/style.css" />
	           <link rel="stylesheet" type="text/css" href="../css/jquery.dataTables_mod.css"  />'''
    #header+='''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"> </script>'''
    #header+='''<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>'''
    header+='''<script src="../js/jquery.js"></script>
	           <script src="../js/jquery.dataTables.min.js"></script>
               <script src="../js/jquery-ui.js"></script>  '''
    header+='''
    <script>
    $(document).ready(function(){
         $("tr").click(function(){
             $("tr").each(function(){
             $(this).removeClass("selected");
             });
             $(this).addClass("selected");
         });

        $(".infoBloc").click(function(){
            $("#"+this.id.slice(5)).dialog({
				title: "Pour créer le monument dans OSM",
                draggable: false,
                resizable: false,
                width:400,
                height:250,
                modal: true,
                overlay: {
                    backgroundColor: '#000',
                    opacity: 0.5,
                },
            });
            return false;
        });

		$("#table_data").DataTable({
			"columnDefs": [
            {
                "targets": [ 2 ],
                "searchable": false,
                "sortable" : false,
            }],
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
    });
    </script>
    </head>'''

    file.write(header)

def write_bandeau(file,t,dic):
    #menu=""
    contenu=""
    contenu+=''' <body>
    <div id="bandeau"> <h4 class="Titre">{}</h4>\n'''.format(t)
    contenu += ''' <p>Les pages de ce site présentent des tableaux comparatifs des monuments historiques dans les bases de données suivantes :
        <ul>
        <li>Le ministère de la culture propose en "Open-Data" une
        <a href="https://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/" title="Base Mérimée" target="blank">
        Base des immeubles de France</a>, une partie de la base Mérimée ( les codes PA* ). Les codes IA* et EA* qui n'apparaissent pas dans cette base ouverte ne sont donc pas comptés dans les colonnes Mérimée.</li>

        <li>L'encyclopédie "Wikipédia" a des pages dédiées aux monuments historiques par département
        et/ou par ville, par exemple pour <a href="https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_l'Ain" title="L'Ain" target="blank">l'Ain</a>,
        ou pour <a href="https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse#" title="Bourg-en-Bresse" target="blank">Bourg-en-Bresse</a></li>
        <li>Le site de cartographie participative "OpenStreetMap" répertorie aussi des monuments historiques ... voir
        <a href="http://wiki.openstreetmap.org/wiki/FR:Key:ref:mhs" title ="sur le Wiki OSM" target="blank">le wiki des tags 'mhs'</a> ou encore la page
        <a href="https://wiki.openstreetmap.org/wiki/Saint-%C3%89tienne/Patrimoine" title =" St Etienne Patrimoine" target="blank">  St Etienne Patrimoine</a>.</li>
        </ul>
        </p>
    <p>Pour le moment, et pour tester l'intérêt de cet outil, seuls les départements de l'Ain du Rhône et de la Loire sont couverts. **6 Sept 2016 : Ajout des départements de l'Allier, de la Drôme et de l'Isère</p>

    <p>Ces pages sont du HTML statique avec un peu de jQuery. Elles sont générées automatiquement chaque nuit par un script python3 sur un petit Nas (~3min/département), puis poussées sur un serveur Web.
     Le code est visible et disponible sur <a href="https://jearro.noip.me/gitlist/Mhs.git" target="blank"> Mhs.git </a>.
     <a href="https://jearro.noip.me/gitlist/Wom.git" target ="blank">L'historique des pages web</a> est aussi accessible.</p>
    <p> Dernière construction des pages, le :<b> {}</b></p>
    '''.format(time.strftime('%d-%m-%Y %H:%M',time.localtime()))

    contenu+='''
    <div id="menu">
        <ul>\n'''
    for d in dic:
        #print (d)
        link = d+"_pages/"+d+"_merosmwip.html"
        title = dic[d]['name'][0]
        contenu += '       <li><a href="{}" title="{}">{}</a></li>\n'.format(link,title,title)
    contenu+= '''   </ul>
            </div>
        </div>'''
    file.write(contenu)

def write_footer(file):
    footer='''<div id="footer"> Page proposée par <a href="http://wiki.openstreetmap.org/wiki/User:JeaRRo">JeaRRo</a>, contributeur OSM </div>
        </body
    </html>
    '''
    file.write(footer)

def creer_fichier(name,d=None):
    '''
        Vérifier si le repertoire existe sinon le créer.
        puis ouvrir le fichier et renvoyer un writer
    '''
    if d :
        s_rep=str(d['code'])+"_pages"
    else:
        s_rep=""
    if ini.prod :
        rep=ini.url_prod+"/Wom/"+s_rep
    else :
        rep=ini.url_dev+"/Wom/"+s_rep
    # FIXME !! Le répertoire racine n'est pas créer et ne doit pas être effacé
    if not os.path.exists(rep):
        os.mkdir(rep)
    if os.path.isdir(rep):
        return open(rep+'/'+name,"w")

def gen_page_index(dico):
    '''
        l'index ne contient que des liens vers les départements disponibles
        et une petite présentation du projet.
        le fichier index.html est créer à la racine d'un répertoire /Wom
    '''
    # génération dans l'odre des départements pour le menu
    dico = OrderedDict(sorted(dico.items(), key=lambda t: t[0]))

    page_name="index.html"

    titre=" Wom : Mérimée, OpenStreetMap, Wikipédia"
    #changer le répertoire de génération des pages : prod=True or not
    oF = creer_fichier(page_name)

    write_entete_index(oF,titre)

    titre="Etat comparé des monuments historiques dans les bases Mérimée, OSM et WikiPédia"
    write_bandeau(oF,titre,dico)
    #    write_footer(oF)
    oF.close()

if __name__ == "__main__":

    ''' générer la page index'''
    gen_page_index(ini.dep)
