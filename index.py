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
    <title>'''
    header+=title
    header+='''</title>
    <link rel="stylesheet" type="text/css" href="{}">
    </head>'''.format(cssFile)
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
    </script> '''
    file.write(header)

def write_bandeau(file,t,dic):
    menu=""
    contenu=""
    contenu+='''</body>
    <div id="bandeau"> <h4 class="Titre">'''
    contenu += t
    contenu += '''</h4>\n <p>Les pages de ce site présentent des tableaux comparatifs des monuments historiques dans les bases de données suivantes :
        <ul>
        <li>Le ministère de la culture propose en "Open-Data" une
        <a href="https://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/" title="Base Mérimée" target="blank">
        Base des immeubles de France</a>, une partie de la base Mérimée.</li>

        <li>L'encyclopédie "Wikipédia" a des pages dédiées aux monuments historiques par département
        et/ou par ville, par exemple pour <a href="https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_l'Ain" title="L'Ain" target="blank">l'Ain</a>,</li>
        <li>Le site de cartographie participative "OpenStreetMap" répertorie aussi des monuments historiques ... voir
        <a href="http://wiki.openstreetmap.org/wiki/FR:Key:ref:mhs" title ="sur le Wiki OSM" target="blank">le wiki des tags 'mhs'</a>.</li>
        </ul>
        <p>
    <p>
    <p>Pour le moment, et pour tester la faisabilité, seuls les départements de l'Ain, du Rhône et de la Loire sont couverts.
    <p>Ces pages sont complètement statiques. Elles sont générées automatiquement chaque nuit, par un script Python, puis transférées sur le serveur.
    <p> Dernière construction des pages, le :<b> {}</b></p>
    '''.format(time.strftime('%d-%m-%Y %H:%M',time.localtime()))

    contenu+='''
    <div id="menu">
        <ul>\n'''
    for d in dic:
        link = d+"_pages/"+d+"_merosmwip.html"
        title = dic[d][d]
        contenu += '       <li><a href="{}" title="{}">{}</a></li>\n'.format(link,title,title)
    contenu+= '''   </ul>
        </div>
        </div>'''
    file.write(contenu)

def write_footer(file):
    footer='''<div id="footer"> Page proposée par <a href="http://wiki.openstreetmap.org/wiki/User:JeaRRo">JeaRRO</a>, contributeur OSM </div>
        </body
    </html>
    '''
    file.write(footer)

def creer_fichier(name,repertoire):
    '''
        Vérifier si le repertoire existe sinon le créer.
        puis ouvrir le fichier et renvoyer un writer
    '''
    # FIXME !! Le répertoire racine n'est pas créer et ne doit pas être effacer
    if not os.path.exists(repertoire):
        os.mkdir(repertoire)
    if os.path.isdir(repertoire):
        return open(repertoire+'/'+name,"w")

def gen_page_index(dico):
    '''
        l'index ne contient que des liens vers les départements disponibles
        et une petite présentation du projet.
        le fichier index.html est créer à la racine d'un répertoire /Wom
    '''
    dico = OrderedDict(sorted(dico.items(), key=lambda t: t[0]))
    page_name="index.html"

    titre="Wom : Etat comparé des monuments historiques dans les bases Mérimée, OSM et WikiPédia"
    #changer le répertoire de génération des pages : prod=True or not
    if ini.prod :
        oF = creer_fichier(page_name,ini.url_prod+"/Wom")
    else :
        oF = creer_fichier(page_name,ini.url_dev+"/Wom")
    write_entete(oF,titre,ini.cssFile)
    write_bandeau(oF,titre,dico)
    #    write_footer(oF)
    oF.close()

if __name__ == "__main__":
    d_dep = ini.dep   #{'01':'Ain', '69':'Rhône','42':'Loire'}
    #print(d_dep)
    ''' générer la page index'''
    gen_page_index(d_dep)
