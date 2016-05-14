#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html

'''
import os,ini,time
from collections import OrderedDict

def write_entete(file, title, cssFile) :
    '''
        Ecrire l'entête du fichier html
    '''
    header=""
    header += '''<!DOCTYPE html>
    <html>
    <head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
    <title>{}</title>\n\t'''.format(title)
    header+='''<link rel="stylesheet" type="text/css" href="{}">\n\t'''.format(cssFile)
    header+='''<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.1/jquery.min.js"> </script>'''
    header+='''
    <script>
    $(document).ready(function(){
     $(".TableRow").click(function(){
     $(".TableRow").each(function(){
     $(this).removeClass("active");
     });
     $(this).addClass("active");
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
    <p>Pour le moment, et pour tester l'intérêt de cet outil, seuls les départements de l'Ain, du Rhône et de la Loire sont couverts.</p>
    <p>Ces pages sont statiques avec un peu de jQuery. Elles sont générées automatiquement chaque nuit, par un script python sur un Nas, puis poussées sur le serveur.
     Le code est visible et disponible sur <a href="http://jearro.noip.me/gitlist/Mhs.git" target="blank"> Mhs.git </a>.
     <a href="http://jearro.noip.me/gitlist/Wom.git" target ="blank">L'historique des pages web</a> est aussi accessible.</p>
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

    write_entete(oF,titre,ini.cssFile)

    titre="Etat comparé des monuments historiques dans les bases Mérimée, OSM et WikiPédia"
    write_bandeau(oF,titre,dico)
    #    write_footer(oF)
    oF.close()

if __name__ == "__main__":

    ''' générer la page index'''
    gen_page_index(ini.dep)
