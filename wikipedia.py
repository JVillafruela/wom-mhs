#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Faire une requette sur les pages wikipédia "Liste_des_monuments_historiques_de_l'Ain". chaque département semble avoir une page de ce type.
    en entrée : un code département = '01' pris dans la table des départements (ini.py)
    en sortie : un dictionnaire dic_wp avec une clé par code mhs ou une clé ERR-Numéro pour les monuments qui n'ont pas de code mhs
            PA01000033' : ['Le Café français', 'Bourg-en-Bresse', 'https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse','Cafe_francais']
            'ERR-0023' :[[nom,commune,url_ville,identifiant],[....]]
            (l'identifiant est l'id, ancre de la page web)
    tester avec le rhône pour avoir des erreurs cde mhs absents

    '''
from __future__ import unicode_literals
import requests,bs4
from bs4 import BeautifulSoup
import ini,insee,mohist
from beaker.cache import CacheManager
from beaker.util import parse_cache_config_options

url_base ="https://fr.wikipedia.org"
#compteur de monument sans code mhs
ctr_no_mhs=0

cache_opts = {
    'cache.type': 'file',
    'cache.data_dir': '/tmp/cache/data',
    'cache.lock_dir': '/tmp/cache/lock'
}

cache = CacheManager(**parse_cache_config_options(cache_opts))

@cache.cache('query-wip-cache', expire=7200)
def makeQuery(url):
    return requests.get(url)

def getData(url):
    r = makeQuery(url)
    contenu = r.text
    #contenu = open("wiki.html", "r").read()
    main_page = BeautifulSoup(contenu,'html.parser')
    #print(main_page.prettify())
    return main_page

def analyseData(data,url,musee):
    global ctr_no_mhs
    # encoding = data.find('meta').attrs['charset']
    # print (encoding)
    # url_ville=url.split('.org')[1]

    grande_commune = False
    tableau =  data.find_all("table", "wikitable sortable")[0]
    for i, tr in enumerate(tableau):
        #print (i, type(tr), tr)
        infos_manquantes=[]
        if isinstance(tr,bs4.element.Tag):
            #l'id du monument permet de le retrouver dans la page
            if 'id' in tr.attrs:
                identifiant = tr.attrs['id']
                #print('Id = ',tr.attrs['id'])
            else:
                identifiant= ''
            td = tr.find_all('td')
            for n, val in enumerate(td):
                #print (n, val)
                code = ''
                # n=0 => nom du monument et lien vers la page Wp du monument
                if n == 0:
                    #print("typedeval = ",type(val.find('a')))
                    if isinstance(val.find('a'),bs4.element.Tag):
                        nom = val.find('a').text
                        # Rechercher si page WP du monument existe
                        if "page inexistante" in val.find('a').attrs['title']:
                            #print(val.find('a').attrs['title'])
                            infos_manquantes.append("Page monument absente")
                    elif val.find('a') == None:
                        nom = val.text
                        infos_manquantes.append("Page monument absente")
                    else :
                        nom =''

                if n == 1:
                    # recherche la commune et l'url_commune
                    commune = val.find('a').string.lstrip().rstrip()
                    #print ('commune =', commune)
                    # print('commune url = ', "/wiki/"+commune)
                    #recherche code_insee
                    c_insee=insee.get_insee(commune)
                    #print ('commune =', commune, "code insee =",c_insee)

                if n == 2 and nom == '' :
                    ''' le nom est vide s'il y a une grande ville (sauf métropole de lyon) '''
                    url_gc = val.find('a')['href']
                    url_gc = url_base+url_gc
                    #print ('url_grosse_commune = ',url_gc)
                    grande_commune=True
                    dat = getData(url_gc)
                    analyseSecondData(dat,url_gc,musee)

                if n == 3:
                    #analyse de la géolocalisation
                    rep = val.find('span', {'class':'geo-dec'})
                    if isinstance(rep,bs4.element.Tag) :
                        geo = val.find('span', {'class':'geo-dec'}).get_text().strip()
                        #lat =  geo.split(',')[0]
                        #lon =  geo.split(',')[1]
                        #pass
                    else:
                        #print ("Erreur : "+nom+" à "+commune+' -> Pas de Géolocalisation\n')
                        geo=""
                        infos_manquantes.append("Géolocalisation absente")
                        #lat=lon=''
                if n == 7:
                    # analyse présence image
                    if "Image manquante" in val.text:
                        #print(nom,"  Pas d'image")
                        infos_manquantes.append("Image absente")

                if n == 4 and not grande_commune:
                    #recherche du code MHS
                    rep = val.find('cite', {'style':'font-style: normal'})
                    if isinstance(rep,bs4.element.Tag) :
                        code = rep.get_text().strip()
                        # print ('Mhs : ', code)
                        # mhs_url = val.find('a').attrs['href']
                        # print(mhs_url)
                        #enregistrement d'un momument si le code mhs existe
                        MH=musee.add_Mh(code)
                        #def add_infos_wip(self, insee, commune, nom, url, ident, infos_manquantes):
                        MH.add_infos_wip(c_insee,commune,nom,geo,url,identifiant,infos_manquantes)
                        #dic_mhs[code] = [nom,commune,c_insee,url,identifiant,infos_manquantes]
                    else :
                        #print ("Erreur : Pas de code MHS pour "+nom+" à "+commune+'\n')
                        code = "ERR-"+str(ctr_no_mhs).zfill(4)
                        infos_manquantes.append("Code MHS absent")
                        MH=musee.add_Mh(code)
                        MH.add_infos_wip(c_insee,commune,nom,geo,url,identifiant,infos_manquantes)
                        #dic_mhs[code] = [nom,commune,c_insee,url,identifiant,infos_manquantes]
                        ctr_no_mhs+=1
                    grande_commune = False
    return musee

def analyseSecondData(data,url,musee):
    global ctr_no_mhs

    commune = url.split('_')[-1]
    #correction encodage nom de commune
    if "%C3%A9" in commune:
        commune=commune.replace("%C3%A9","é")
    if "%C3%B4" in commune:
        commune=commune.replace("%C3%B4","ô")
    print (commune)
    c_insee = insee.get_insee(commune)
    #print ("commune = ",commune," code insee =",c_insee )
    #url_ville = url.split('.org')[1]
    tableau =  data.find_all("table", "wikitable sortable")[0]
    for i, tr in enumerate(tableau):
        #print (i, type(tr), tr)
        infos_manquantes=[]
        if isinstance(tr,bs4.element.Tag):
            #l'id du monument permet de le retrouver dans la page
            if 'id' in tr.attrs:
                identifiant = tr.attrs['id']
                #print('Id = ',tr.attrs['id'])
            else:
                identifiant =''
            #   identifiant= tr.find('td').find('a')['title']
            td = tr.find_all('td')
            for n, val in enumerate(td):
                #print (n, val)
                code = ''
                #n=0 => nom du monument et lien vers la page Wp du monument
                if n == 0:
                    #print("typedeval = ",type(val.find('a')))
                    if isinstance(val.find('a'),bs4.element.Tag):
                        nom = val.find('a').text
                        # Rechercher si page WP du monument existe
                        if "page inexistante" in val.find('a').attrs['title']:
                            #print(val.find('a').attrs['title'])
                            infos_manquantes.append("Page monument absente")
                    elif val.find('a') == None:
                        nom = val.text
                        infos_manquantes.append("Page monument absente")
                    else :
                        nom =''

                if (commune!="Lyon" and n==2) or (commune=="Lyon" and n==3) :
                    #analyse de la géolocalisation
                    rep = val.find('span', {'class':'geo-dec'})
                    if isinstance(rep,bs4.element.Tag) :
                        geo = val.find('span', {'class':'geo-dec'}).get_text().strip()
                        # lat =  geo.split(',')[0]
                        # lon =  geo.split(',')[1]
                        #pass
                    else:
                        #print ("Erreur : "+nom+" à "+commune+' -> Pas de Géolocalisation\n')
                        geo=""
                        infos_manquantes.append("Géolocalisation absente")
                        # liste_incomplet.append([nom,commune,"géolocalisation absente"])
                        # lat=lon=''
                if (commune!="Lyon" and n == 6) or (commune=="Lyon" and n==7) :
                    # analyse présence image
                    if "Image manquante" in val.text:
                        #print(nom,"  Pas d'image")
                        infos_manquantes.append("Image absente")
                if (commune!="Lyon" and n == 3) or (commune=="Lyon" and n==4):
                    #recherche du code MHS
                    rep = val.find('cite', {'style':'font-style: normal'})
                    #rep = val.find('cite')
                    #print (rep)
                    if isinstance(rep,bs4.element.Tag) :
                        code = rep.get_text().strip()
                        #print (code)
                        # mhs_url = val.find('a').attrs['href']
                        # print(mhs_url)
                    #enregistrement d'un momument si le code mhs existe
                        #dic_mhs[code] = [nom,commune,c_insee,url,identifiant,infos_manquantes]
                        MH=musee.add_Mh(code)
                        MH.add_infos_wip(c_insee,commune,nom,geo,url,identifiant,infos_manquantes)
                    else :
                        #print ("Erreur : Pas de code MHS pour "+nom+" à "+commune+'\n')
                        code = "ERR-"+str(ctr_no_mhs).zfill(4)
                        infos_manquantes.append("Code MHS absent")
                        MH=musee.add_Mh(code)
                        MH.add_infos_wip(c_insee,commune,nom,geo,url,identifiant,infos_manquantes)
                        #dic_mhs[code] = [nom,commune,c_insee,url,identifiant,infos_manquantes]
                        ctr_no_mhs+=1
    return musee

def get_wikipedia(url_list,musee):
    ''' Faire la requette overpass puis l'analyse du résultat '''
    for url in url_list:
        main_page = getData(url_base+url)
        musee = analyseData(main_page,url_base+url,musee)
    return musee


if __name__ == "__main__":
    departement = '69'
    # dic_wp = {}
    # Nb_noMHS=0
    musee = mohist.Musee()
    musee = get_wikipedia(ini.dep[departement]['url_d'],musee)
    # for mh,MH in musee.collection.items():
    #     print(mh, MH)
    #     for key,value in MH.description[mh]['wip'].items():
    #         print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans Wikipédia.".format(departement,len(musee.collection)))
    #print(dic_merimee['PA01000038'])
    musee.maj_salle()
    print(musee)

    nb=musee.get_nb_MH('wip')
    print(nb)


    # print ("il y a {} Monuments du département {} dans Wikipédia.".format(len(dic_wp),ini.dep[departement]['text']))
    # print ("Monuments du département {} sans code MH : {}".format(ini.dep[departement][('text')],Nb_noMHS))
