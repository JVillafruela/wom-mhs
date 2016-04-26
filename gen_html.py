#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html
'''
import os,index,merimee,overpass,wikipedia,ini,mohist
#from timer import LoggerTimer
from collections import OrderedDict

def get_table_merosmwip(salle):

    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
        note_osm=""
        note_wp=""
    #      print( mh,desc)
    #      print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]
        # les urls OSM
        if 'url_osm' in desc['osm']:
            url_osm_org='href="http://www.openstreetmap.org/browse/'+desc['osm']['url_osm']
            type_osm = desc['osm']['url_osm'].split('/')[0]
            id_osm = desc['osm']['url_osm'].split('/')[1]
            url_osm_id ='href="http://www.openstreetmap.org/edit?editor=id&'+type_osm+'='+id_osm
            url_josm= 'href="http://localhost:8111/load_object?new_layer=true&objects='+type_osm[0]+id_osm
        #les tags manquants dans OSM
        if len(desc['osm']['tags_manquants'])>0:
            note_osm=", ".join(desc['osm']['tags_manquants'])
        elif 'mhs_bis' in desc['osm']:
            note_osm+=' <a href="http://www.openstreetmap.org/browse/'+desc['osm']['mhs_bis'][0]+'" target="blank" title="Monument en double dans OSM"> Double OSM </a>'
        else :
            note_osm =""
        #les infos manquantes dans wikipédia
        if 'infos_manquantes' in desc['wip']:
            #print(desc['wip'])
            if len(desc['wip']['infos_manquantes'])>0:
                note_wp=", ".join(desc['wip']['infos_manquantes'])
            else:
                note_wp=""
        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1"><a {}" target="blank" title="Voir sur openstreetmap.org"> ORG </a> -
        <a {}" target="blank" title="Editer avec ID"> ID </a> - <a {}" target="blank" title="Editer avec Josm"> Josm </a> </div>
    '''.format(url_osm_org, url_osm_id,url_josm)
        #suite de la tabele : col WP
        # recherche des urls WP
        if 'wikipedia' in desc['osm']['tags_mh']:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+desc['osm']['tags_mh']['wikipedia']
        else :
            url_osmwp =""
        if 'url' in desc['wip']:
            url_wip = desc['wip']['url']+"#"+desc['wip']['id']
        else :
            url_wip=""
        # table colonne WP
        if url_wip and url_osmwp :
            table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> -
          <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_wip,url_osmwp)
        elif url_wip and not url_osmwp:
            url_wip = desc['wip']['url']+"#"+desc['wip']['id']
            table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> </div>'''.format(url_wip)
        elif not url_wip and url_osmwp:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+desc['osm']['tags_mh']['wikipedia']
            table+='''<div class="TableCell1">  <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_osmwp)
        else:
            table+='''<div class="TableCell1">  ---- </div>'''
        #table note OSM
        if note_osm !="":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_osm)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table note WP
        if note_wp !="":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_wp)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table fin
        table+='''</div>'''
    return table

def get_table_merosm(salle):

    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
        note_osm=""
    #      print( mh,desc)
    #      print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]
        # les urls OSM
        if 'url_osm' in desc['osm']:
            url_osm_org='href="http://www.openstreetmap.org/browse/'+desc['osm']['url_osm']
            type_osm = desc['osm']['url_osm'].split('/')[0]
            id_osm = desc['osm']['url_osm'].split('/')[1]
            url_osm_id ='href="http://www.openstreetmap.org/edit?editor=id&'+type_osm+'='+id_osm
            url_josm= 'href="http://localhost:8111/load_object?new_layer=true&objects='+type_osm[0]+id_osm
        #les tags manquants dans OSM
        if len(desc['osm']['tags_manquants'])>0:
            note_osm=", ".join(desc['osm']['tags_manquants'])
        elif 'mhs_bis' in desc['osm']:
            note_osm+=' <a href="http://www.openstreetmap.org/browse/'+desc['osm']['mhs_bis'][0]+'" target="blank" title="Monument en double dans OSM"> Double OSM </a>'
        else :
            note_osm =""
        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1"><a {}" target="blank" title="Voir sur openstreetmap.org"> ORG </a> -
        <a {}" target="blank" title="Editer avec ID"> ID </a> - <a {}" target="blank" title="Editer avec Josm"> Josm </a> </div>
    '''.format(url_osm_org, url_osm_id,url_josm)
        #suite de la tabele : col WP
        table+='''<div class="TableCell1">  ---- </div>'''
        #table note OSM
        if note_osm !="":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_osm)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table note WP

        #table fin
        table+='''</div>'''
    return table

def get_table_merwip(salle):
    table=""

    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
        note_wp=""
    #      print( mh,desc)
    #      print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]

        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1">  ---- </div>'''
        #suite de la tabele : col WP = adresse WP1
        if 'url' in desc['wip']:
            url_wip = desc['wip']['url']+"#"+desc['wip']['id']
        else :
            url_wip=""
        #les infos manquantes dans wikipédia
        if 'infos_manquantes' in desc['wip']:
            #print(desc['wip'])
            if len(desc['wip']['infos_manquantes'])>0:
                note_wp=", ".join(desc['wip']['infos_manquantes'])
            else:
                note_wp=""
        table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> </div>'''.format(url_wip)
        #table note OSM
        table += '''<div class="TableCell3">  </div>'''
        #table note WP
        if note_wp !="":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_wp)
        else:
            table += '''<div class="TableCell3">  </div>'''
        #table fin
        table+='''</div>'''
    return table

def get_table_osmwip(salle):
    pass

def get_table_osm(salle):

    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
        note_osm=""
    #      print( mh,desc)
    #      print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        #description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]
        if 'name' in desc['osm']['tags_mh']:
            description = desc['osm']['tags_mh']['name']
        else:
            description =""
        # les urls OSM
        if 'url_osm' in desc['osm']:
            url_osm_org='href="http://www.openstreetmap.org/browse/'+desc['osm']['url_osm']
            type_osm = desc['osm']['url_osm'].split('/')[0]
            id_osm = desc['osm']['url_osm'].split('/')[1]
            url_osm_id ='href="http://www.openstreetmap.org/edit?editor=id&'+type_osm+'='+id_osm
            url_josm= 'href="http://localhost:8111/load_object?new_layer=true&objects='+type_osm[0]+id_osm
        #les tags manquants dans OSM
        if len(desc['osm']['tags_manquants'])>0:
            note_osm=", ".join(desc['osm']['tags_manquants'])
        elif 'mhs_bis' in desc['osm']:
            note_osm+=' <a href="http://www.openstreetmap.org/browse/'+desc['osm']['mhs_bis'][0]+'" target="blank" title="Monument en double dans OSM"> Double OSM </a>'
        else :
            note_osm =""
        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1"><a {}" target="blank" title="Voir sur openstreetmap.org"> ORG </a> -
        <a {}" target="blank" title="Editer avec ID"> ID </a> - <a {}" target="blank" title="Editer avec Josm"> Josm </a> </div>
    '''.format(url_osm_org, url_osm_id,url_josm)
        #suite de la tabele : col WP
        # recherche des urls WP
        if 'wikipedia' in desc['osm']['tags_mh']:
            url_osmwp = 'href="https://fr.wikipedia.org/wiki/'+desc['osm']['tags_mh']['wikipedia']
        else :
            url_osmwp =""

        # table colonne WP
        if  url_osmwp :
            table+='''<div class="TableCell1">  <a {}" target="blank" title ="Lien direct à partir du tag wikipedia sur Osm" > WP2 </a> </div>'''.format(url_osmwp)
        else:
            table+='''<div class="TableCell1">  ---- </div>'''
        #table note OSM
        if note_osm !="":
            table += '''<div class="TableCell2"> {} </div> '''.format(note_osm)
        else:
            table += '''<div class="TableCell2">  </div>'''
        #table note WP

        #table fin
        table+='''</div>'''
    return table

def get_table_wip(salle):

    table=""

    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
        note_wp=""
        #print( mh,desc)
    #   print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        #description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]
        description =""
        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1">  ---- </div>'''
        #suite de la tabele : col WP
        if 'url' in desc['wip']:
            url_wip = desc['wip']['url']+"#"+desc['wip']['id']
        else :
            url_wip=""
        #les infos manquantes dans wikipédia
        if 'infos_manquantes' in desc['wip']:
            #print(desc['wip'])
            if len(desc['wip']['infos_manquantes'])>0:
                note_wp=", ".join(desc['wip']['infos_manquantes'])
            else:
                note_wp=""
        table+='''<div class="TableCell1"> <a href="{}" target="blank" title="Description sur page Wp départementale">  WP1 </a> </div>'''.format(url_wip)
        #table note OSM
        table += '''<div class="TableCell3">  </div>'''
        #table note WP
        if note_wp !="":
            table += '''<div class="TableCell3"> {} </div> '''.format(note_wp)
        else:
            table += '''<div class="TableCell3">  </div>'''

        #table fin
        table+='''</div>'''
    return table

def get_table_mer(salle):
    table=""
    l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    for mh,desc in salle.collection.items():
    #      print( mh,desc)
    #      print (desc['osm']['url_osm'])
        # les infos sur le monuments dans mérimée
        description = desc['mer']['nom'][:45]+'; '+desc['mer']['commune'][:20]


        #debut de la table col mérimée et description
        table += '''<div class="TableRow">
                        <div class="TableCell1"><a href="{}{}" target="blank" title="La fiche dans la base Mérimée">{}</a></div>
                        <div class="TableCell2">{}</div>'''.format(l0,mh,mh,description)
        #suite de la table : col OSM
        table += '''<div class="TableCell1"> ---- </div>'''
        #suite de la tabele : col WP
        # recherche des urls WP

        table+='''<div class="TableCell1">  ---- </div>'''
        #table note OSM

        table += '''<div class="TableCell2">  </div>'''
        #table note WP

        #table fin
        table+='''</div>'''
    return table

def write_contenu(file,stats,salle):
    table =""
    d_titre_table= {'s_merosmwip': 'Monuments historiques présents dans Mérimée, OpenStreetMap et Wikipédia',
            's_merosm': 'Monuments historiques présents dans Mérimée et OpenStreetMap',
            's_merwip': 'Monuments historiques présents dans Mérimée et Wikipédia',
            's_osmwip': 'Monuments historiques présents dans OpenStreetMap et Wikipédia',
            's_osm': 'Monuments historiques présents seulement dans OpenStreetMap',
            's_wip': 'Monuments historiques présents seulement dans wikipédia',
            's_mer': 'Monuments historiques présents seulement dans Mérimée',
            }
    d_get_table={'s_merosmwip': get_table_merosmwip,
                's_merosm': get_table_merosm,
                's_merwip': get_table_merwip,
                's_osmwip': get_table_osmwip,
                's_osm': get_table_osm,
                's_wip': get_table_wip,
                's_mer': get_table_mer,
                }

    header='''
<div class="TableComplet" >
    <div class="TableTitre"> {}</div>
    <div class="TableHeading">
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead2">Description</div>
        <div class="TableHead1">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead3">Note OSM</div>
        <div class="TableHead3">Note WP</div>
    </div>
    <div class="TableBody">
    '''.format(d_titre_table[salle.nom])

    #construire la table des données
    table = d_get_table[salle.nom](salle)
    tableau=[header, table]
    for r in tableau:
        file.write(r)


def write_bandeau(file,t,d,d_dep,stats,salle):
    # page est le nom de la salle, salle est l'objet
    menu=""
    pages=['merosmwip','merosm','merwip','osmwip','osm','wip','mer']
    d_pages= {'merosmwip': ['Mérimée, Osm, Wp','Monuments présents dans les trois bases.'],
            'merosm': ['Mérimée, Osm','Monuments à créer dans Wikipédia'],
            'merwip': ['Mérimée, Wp','Monuments à créer dans OpenStreetMap'],
            'osmwip':['Osm, Wp','Monuments non présents dans la base Mérimée Ouverte ou Erreur de code MHS'],
            'osm': ['Seulement Osm','Monuments non présents dans la base Mérimée Ouverte ou Erreur de code MHS'],
            'wip': ['Seulement Wp ','Monuments non présents dans la base Mérimée Ouverte ou Erreur de code MHS'],
            'mer': ['Seulement Mérimée', 'Monuments à créer dans Wikipédia et dans OpenstreetMap'],
            }

    intro='''</h4> <p>Pour le département {}, la base Mérimée décrit {} monuments historiques.<p>\
        Ils sont {} dans wikipédia, et OSM en connait {}.<p><p>'''.format(d_dep[d]['text'],stats['mer'],stats['wip'],stats['osm'])
    bandeau1 = '''</body>
<div id="bandeau"> <h4 class='Titre'>'''
    bandeau2='''
<div id="menu">
    <ul>'''
    for p in pages:
        #créer le lien vers les autre pages
        link = d+"_"+p+".html"
        title = d_pages[p][1]
        # nombre de MH dans une salle
        select="s_"+p
        nb_MH = stats[select]
        #page non vide
        if nb_MH > 0:
            texte = '<span class="emphase">{} </span>'.format(nb_MH)+d_pages[p][0]
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
    print("----------- {} monuments".format(stats[salle.nom]))
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
    noms_salle= ['s_merosmwip','s_merosm','s_merwip','s_osm','s_wip','s_osmwip','s_mer']
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
        #deux pour le moment
        for s in liste_salle :
            if stats[s.nom] > 0:
                # s est un objet musee
                #print(s.nom)
                gen_page(d,d_dep,stats,s)



    ''' Générer la page index'''
    #index.gen_index(d_dep)