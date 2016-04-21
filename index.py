#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html
'''
import os
from collections import OrderedDict

def write_entete(file,title,cssFile):
    '''
        Ecrire l'entête du ficheir html
    '''
    head0 = '''<!DOCTYPE html>
<html>
<head>
    <meta content="text/html; charset=UTF-8" http-equiv="Content-Type"/>
    <title>'''
    head1 ='''</title>
    <link rel="stylesheet" type="text/css" href="{}">
</head>'''.format(cssFile)
    file.write(head0+title+head1)

def write_bandeau(file,t,dic):
    menu=""
    intro='''</h4> <p>Les pages de ce site présentent des tableaux comparatifs des monuments historiques dans les bases de données suivantes :
        <ul>
        <li>Le ministère de la culture propose en "open-data" une base des immeubles de France,</li>
        <li>L'encyclopédie "Wikipédia" a des pages dédiées aux monuments historiques,</li>
        <li>Le site de cartographie participative "OpenStreetMap" répertorie aussi des monuments historiques</li>
        </ul>
        <p>
    Ces tableaux comparatifs devraient permettrent d'améliorer le qualité et le suivi des descriptions des MH sur OSM et Wikpédia.
    <p>Pour le moment, et pour tester la faisabilité, seuls les départements de l'Ain, du Rhône et de la Loire sont couverts
    '''
    bandeau1='''</body>
<div id="bandeau"> <h4>'''
    bandeau2='''
<div id="menu">
    <ul>'''
    for d in dic:
        link = d+"_pages/"+d+"_merosmwip.html"
        title = dic[d]
        texte = dic[d]
        menu += '<li><a href="'+link+'" title="'+title+'">'+texte+'</a></li>\n'
    close= '''</ul>
    </div>
</div>'''
    contenu=[bandeau1,t,intro,bandeau2,menu,close]
    for c in contenu:
        file.write(c)

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
    if not os.path.exists(repertoire):
        os.mkdir(repertoire)
    if os.path.isdir(repertoire):
        return open(repertoire+'/'+name+".html","w")

def gen_index(dico):
    '''
        l'index ne contient que des liens vers les trois départements disponibles
        et une petite présentation du projet
        le fichier index.html est créer à la racine d'un répertoire /web
    '''
    index_name="index"
    racine="web"
    titre="Etat comparé des monuments historiques dans les bases Mérimée, OSM et WikiPédia"
    oF = creer_fichier(index_name,racine)
    write_entete(oF,titre,"static/style.css")
    write_bandeau(oF,titre,dico)
    write_footer(oF)
    oF.close()

if __name__ == "__main__":
    d_dep= {'01':'Ain', '69':'Rhône','42':'Loire'}
    d_dep = OrderedDict(sorted(d_dep.items(), key=lambda t: t[0]))
    ''' tester la présence d'une génération précédente et faire une sauvegarde'''
    ''' tester l'espace disque minimum requis pour la génération... qq Mo ?'''
    ''' générer la page index'''
    gen_index(d_dep)
    '''générer les six pages de chaque département'''
    for d in d_dep:
        print('------'+d+'------')
        ''' '''
        ''' Acquérir les datas'''
        ''' Générer les résultats pour affichage (tests présences)'''
        pages=['merosmwip','merosm','merwip','oemwip','osm','wip']
        ''' pour chaque page in pages:'''
        for p in pages:
            pname=d+'_'+p+'.html'
            print (pname)
            ''' ouvrir le fichier(pname) et Créer/vérifier les répertoires ./d
                s'il n'existe pas
            '''
            '''écrire l'entête'''
            '''écrire le bandeau'''
            '''écrire le menu'''
            '''écrire le contenu'''
            '''écrire le pied de page'''
            ''' fermer le fichier'''


    # htmlFile = "./web/index.html"
    # hF =open(htmlFile,'w')
    # gen_htm(hF)
    # hF.close()
