#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html
'''
import os,index,data,merimee,overpass,wikipedia,ini,mohist
#from timer import LoggerTimer
from collections import OrderedDict

def write_contenu(file,stats,salle):
    table =""
    note_osm=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    header='''
<div class="TableComplet" >
    <div class="TableHeading">
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead2">Description</div>
        <div class="TableHead1">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead3">Note OSM</div>
        <div class="TableHead3">Note WP</div>
    </div>
    <div class="TableBody">
    '''
    #parcourir la salle
    for mh,desc in salle.collection.items():
        # print( mh,desc)
        # print (desc['osm']['url_osm'])
        # exit()
        description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]
        url_osm_org='href="http://www.openstreetmap.org/browse/'+desc['osm']['url_osm']
        type_osm = desc['osm']['url_osm'].split('/')[0]
        id_osm = desc['osm']['url_osm'].split('/')[1]
        url_osm_id ='href="http://www.openstreetmap.org/edit?editor=id&'+type_osm+'='+id_osm
        url_josm= 'href="http://localhost:8111/load_object?new_layer=true&objects='+type_osm[0]+id_osm
        table += '''
        <div class="TableRow">
            <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
            <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        if 'osm' in salle.nom:
            if len(desc['osm']['tags_manquants'])>0:
                note_osm=", ".join(desc['osm']['tags_manquants'])
            else :
                note_osm =""
            table += '''<div class="TableCell1"><a {}" target="blank" title="Voir sur openstreetmap.org"> ORG </a> -
            <a {}" target="blank" title="Editer avec ID"> ID </a> - <a {}" target="blank" title="Editer avec Josm"> Josm </a> </div>
        '''.format(url_osm_org, url_osm_id,url_josm)
        if 'wip' in salle.nom:
            url_wip = desc['wip']['url']+"#"+desc['wip']['id']
            if 'wikipedia' in desc['osm']['tags_mh']:
                url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+desc['osm']['tags_mh']['wikipedia']
                table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> -
                <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_wip,url_osmwp)
            else:
                table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> </div>'''.format(url_wip)
        else:
            table+='''<div class="TableCell1">  {}  </div>'''.format("----")
        if note_osm !="":
    #        table += '''<div class="TableCell2"><a href="http://www.openstreetmap.org/browse/{} target="blank">Deux descriptions dans OSM</a> '''.format(note_osm)
            table += '''<div class="TableCell2"> {} </div>'''.format(note_osm)
    #     if row[5]:
    #         table += '''<div class="TableCell2"><a href="http://www.openstreetmap.org/browse/{}"
    #          target="blank">Dans OSM en double</a>  ; {} {}</div>'''.format(row[6],",".join(row[4]),",".join(row[7]))
    #     else:
    #         table +=''' <div class="TableCell2"> {} </div> '''.format(",".join(row[4]))
        table+='''</div>'''
    tableau=[header, table]
    for r in tableau:
        file.write(r)


# old - def write_bandeau(file,t,d,dep_text,page,comptes,nb_items):
def write_bandeau(file,t,d,d_dep,stats,salle):
    # page est le nom de la salle, salle est l'objet
    #page = salle.nom inutile !
    menu=""
    pages=['merosmwip','merosm','merwip','osmwip','osm','wip']
    d_pages= {'merosmwip': 'Mérimée, Osm, Wp',
            'merosm':'Mérimée, Osm',
            'merwip':'Mérimée, Wp',
            'osmwip':'Osm, Wp',
            'osm': 'Seulement Osm',
            'wip': 'Seulement Wp'
            }

    intro='''</h4> <p>Pour le département {}, la base Mérimée décrit {} monuments historiques.<p>\
        Ils sont {} dans wikipédia, et OSM en connait {}.<p><p>'''.format(d_dep[d]['text'],stats['mer'],stats['wip'],stats['osm'])
    bandeau1 = '''</body>
<div id="bandeau"> <h4>'''
    bandeau2='''
<div id="menu">
    <ul>'''
    for p in pages:
        #créer le lien vers les autre pages
        link = d+"_"+p+".html"
        title = d_pages[p]
        # nombre de MH dans une salle
        select="s_"+p
        nb_MH = stats[select]
        texte = '<span class="emphase">{} </span>'.format(nb_MH)+d_pages[p]
        menu += '<li><a href="'+link+'" title="'+title+'" >'+texte+'</a></li>'
    close= '''</ul>
    </div>
</div>'''
    contenu=[bandeau1,t,intro,bandeau2,menu,close]
    for c in contenu:
        file.write(c)

#def gen_page(dep_text,dep,comptes,page,data):
def gen_page(d,d_dep,stats,salle):
    page = salle.nom.split('_')[1]
    page_name=d+'_'+page+'.html'
    print("Construction de la page {}.".format(page_name))
    '''créer le fichier'''
    # FIXME  !!! ouvrir le fichier(page_name) et Créer/vérifier les répertoires s'il n'existe pas
    rep="web/"+d+"_pages"
    oF=index.creer_fichier(page_name,rep)
    '''écrire l'entête'''
    titre="Etat comparé des monuments historiques {} dans les bases Mérimée, OSM et WikiPédia".format(d_dep[d]['text'])
    index.write_entete(oF,titre,"../static/style.css")
    '''écrire le bandeau et écrire le menu'''
    write_bandeau(oF,titre,d,d_dep,stats,salle)
    '''écrire le contenu'''
    write_contenu(oF,stats,salle)
    # '''écrire le pied de page'''
    index.write_footer(oF)
    # '''fermer le fichier'''
    oF.close()

if __name__ == "__main__":
    ''' Définir les variables d'entrée'''
    #d_dep ={'01':'Ain', '69':'Rhône','42':'Loire','38':'Isère'}
    d_dep = ini.dep
    d_dep = OrderedDict(sorted(d_dep.items(), key=lambda t: t[0]))
    bases =['mer','osm','wip']
    stats={}
    # Une salle va correspondre à une page_web : une sélection de MH d'une certaine catégorie
    noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osmwip','s_osm','s_wip']
    liste_salle=[]
    for nom_salle in noms_salle :
        # créer l'objet Musee correspondant -> faire les recherches suivants les caractéritiques
        nom_salle = mohist.Musee(nom_salle)
        liste_salle.append(nom_salle)
    ''' tester la présence d'une génération précédente et faire une sauvegarde'''
    ''' tester l'espace disque minimum requis pour la génération... qq Mo ?'''

    '''générer les six pages de chaque département'''
    for d in d_dep:
        print('------'+d+'------')
        ''' '''
        ''' Acquérir les datas'''
        # Un musée museum par département !!
        museum = mohist.Musee(ini.dep[d][d])
        # Créer les monuments du museum
        # FIXME !!! supprimer le passage par le dictionnaire dans la génération...
        museum = mohist.charge_merimee(d,museum)
        museum = mohist.charge_osm(ini.dep[d],museum)
        museum = mohist.charge_wp(ini.dep[d],museum)
        # Obtenir les stats du Musée


        stats['musee']=len(museum.collection)
        for bs in bases:
            # ajouter le nombre total de monuments, mettre le nom complet de la base Mérimée, OSM, WP
            stats[bs]=museum.calcul_nbMH(bs)
            print ("Nombre de MH issues de la base {} : {}".format(bs,stats[bs]))
        # créer les classements
        museum.classer_MH(liste_salle)
        # statistiques résultats
        for salle in liste_salle:
            stats[salle.nom] = len(salle.collection)
            #print(salle.nom, stats[salle.nom])
        ''' pour chaque salle une page'''
        #une seule pour le moment
        for s in liste_salle[:1] :

            # s est un objet musee
            #print(s.nom)
            gen_page(d,d_dep,stats,s)



    ''' Générer la page index'''
    #index.gen_index(d_dep)
