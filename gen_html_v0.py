#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html
'''
import os,index,data,merimee,overpass,wikipedia,ini
#from timer import LoggerTimer
from collections import OrderedDict

def write_contenu(file,t,d,dep_text,page,comptes,data):
    table =""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    header='''
<div class="TableComplet" >
    <div class="TableHeading">
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead2">Description</div>
        <div class="TableHead1">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead2">Note </div>
    </div>
    <div class="TableBody">
    '''
    for row in data:
        table += '''
        <div class="TableRow">
            <div class="TableCell1"><a href="{}{}" target="blank">{}</a></div>
            <div class="TableCell2">{} -- {}</div>
            <div class="TableCell1"><a href="http://www.openstreetmap.org/browse/{}" target="blank"> OSM </a></div>
        '''.format(l0,row[0],row[0],row[1],row[2],row[3])
        if page=='merosmwip':
            table+='''<div class="TableCell1"> <a href="{}" target="blank">  WP </a> </div>'''.format(row[8])
        elif page=='merosm':
            table+='''<div class="TableCell1">  {}  </div>'''.format("----")
        if row[5]:
            table += '''<div class="TableCell2"><a href="http://www.openstreetmap.org/browse/{}"
             target="blank">Dans OSM en double</a>  ; {} {}</div>'''.format(row[6],",".join(row[4]),",".join(row[7]))
        else:
            table +=''' <div class="TableCell2"> {} </div> '''.format(",".join(row[4]))
        table+='''</div>'''
    tableau=[header, table]
    for r in tableau:
        file.write(r)


def write_bandeau(file,t,d,dep_text,page,comptes,nb_items):
    menu=""
    intro="</h4> <p>Pour le département {}, la base Mérimée décrit {} monuments historiques.<p>\
        Ils sont {} dans wikipédia, et OSM en connait {}.<p><p>".format(dep_text,comptes[0],comptes[1],comptes[2])
    pages=['merosmwip','merosm','merwip','osmwip','osm','wip']
    d_pages= {'merosmwip': 'Mérimée, Osm, Wp',
            'merosm':'Mérimée, Osm',
            'merwip':'Mérimée, Wp',
            'osmwip':'Osm, Wp',
            'osm': 'Seulement Osm',
            'wip': 'Seulement Wp'
            }
    bandeau1='''</body>
<div id="bandeau"> <h4>'''
    bandeau2='''
<div id="menu">
    <ul>'''
    for p in pages:
        link = d+"_"+p+".html"
        title = d_pages[p]
        if p == page:
            texte = '<span class="emphase">{} </span>'.format(nb_items)+ d_pages[p]
        else :
            texte = d_pages[p]
        menu += '<li><a href="'+link+'" title="'+title+'" >'+texte+'</a></li>\n'
    close= '''</ul>
    </div>
</div>'''
    contenu=[bandeau1,t,intro,bandeau2,menu,close]
    for c in contenu:
        file.write(c)

def gen_page(dep_text,dep,comptes,page,data):
    '''créer le fichier'''
    rep="web/"+dep+"_pages"
    p=dep+"_"+page
    oF=index.creer_fichier(p,rep)
    '''écrire l'entête'''
    titre="Etat comparé des monuments historiques {} dans les bases Mérimée, OSM et WikiPédia".format(dep_text)
    index.write_entete(oF,titre,"../static/style.css")
    '''écrire le bandeau et écrire le menu'''
    write_bandeau(oF,titre,dep,dep_text,page,comptes,len(data))
    '''écrire le contenu'''
    write_contenu(oF,titre,dep,dep_text,page,comptes,data)
    '''écrire le pied de page'''
    index.write_footer(oF)
    '''fermer le fichier'''
    oF.close()

if __name__ == "__main__":
    #d_dep ={'01':'Ain', '69':'Rhône','42':'Loire'}
    d_dep ={'01':'Ain'}
    d_dep = OrderedDict(sorted(d_dep.items(), key=lambda t: t[0]))
    d_fonct= {'merosmwip': data.table_complet,
                'merosm' : data.table_wp_absent,
            }

    ''' tester la présence d'une génération précédente et faire une sauvegarde'''
    ''' tester l'espace disque minimum requis pour la génération... qq Mo ?'''
    ''' Générer la page index'''
    #index.gen_index(d_dep)
    '''générer les six pages de chaque département'''
    for d in d_dep:
        print('------'+d+'------')
        ''' '''
        ''' Acquérir les datas'''
        dep_text,d_me,d_wp,d_osm=data.get_data(d)
        comptes = [len(d_me),len(d_wp),len(d_osm)]
        #pages=['merosmwip','merosm','merwip','oemwip','osm','wip']
        pages=['merosmwip','merosm']
        ''' pour chaque page in pages:'''
        for p in pages:

            result =  d_fonct[p](d_me,d_wp,d_osm)
            #print (p,result)
            ''' ouvrir le fichier(pname) et Créer/vérifier les répertoires ./d
                s'il n'existe pas
            '''
            pname=d+'_'+p+'.html'
            print("Construction de la page {}.".format(pname))
            gen_page(dep_text,d,comptes,p,result)
