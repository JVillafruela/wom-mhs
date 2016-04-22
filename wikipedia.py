#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Faire une requette sur les pages wikipédia "Liste_des_monuments_historiques_de_l'Ain". chaque département semble avoir une page de ce type.
    en entrée : un code département = '01'



    FIXME => il y a un dico pour convertir le Numéro du département en lien wikipédia. Avec dans certains cas, deux liens (voir le rhône)
    FIXME => supprimer le code dep_text du dico d'entrée... et reporter cela à l'affichage des pages html
'''
from __future__ import unicode_literals
import requests,requests_cache
from bs4 import BeautifulSoup
import bs4
from collections import OrderedDict

#mhs_wp est un dico suivant les codes : mhs il contient pour chaque clé/code
#la liste :  nom, commune, url_dep_wp , identifiant (ancre dans la page)
#requests_cache.install_cache('wikipedia_cache', backend='memory', expire_after=3600)
dic_mhs_wp = {}
url_base ="https://fr.wikipedia.org"
#urls =["https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_l'Ain",\
        # "https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Belley",\
        # "https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Bourg-en-Bresse",\
        # "https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Pérouges",\
        # "https://fr.wikipedia.org/wiki/Liste_des_monuments_historiques_de_Trévoux"]
dep = {'01' : {
            "url_d" : "/wiki/Liste_des_monuments_historiques_de_l'Ain",
            "url_d_2" : "",
                },
        '42' : {
            "url_d" : "/wiki/Liste_des_monuments_historiques_de_la_Loire",
            "url_d_2" : "",
            },
        '69': {
            "url_d" : "/wiki/Liste_des_monuments_historiques_du_Rhône",
            'url_d_2' : "/wiki/Liste_des_monuments_historiques_de_la_métropole_de_Lyon",
            }
        }

def getData(url):
    r = requests.get(url)
    contenu = r.text
    #contenu = open("wiki.html", "r").read()
    main_page = BeautifulSoup(contenu,'html.parser')
    #print(main_page.prettify())
    return main_page

def analyseData(data,url,dic_mhs):
    # encoding = data.find('meta').attrs['charset']
    # print (encoding)
    url_ville=url.split('.org')[1]
    grande_commune = False
    tableau =  data.find_all("table", "wikitable sortable")[0]
    for i, tr in enumerate(tableau):
        #print (i, type(tr), tr)

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
                #n=0 => nom du monument et lien vers la page Wp du monument
                if n == 0:
                    #print("typedeval = ",type(val.find('a')))
                    if isinstance(val.find('a'),bs4.element.Tag):
                        nom = val.find('a').text
                    elif val.find('a') == None:
                        nom = val.text
                    else :
                        nom =''
                    #print('name =',nom)
                    # #name_href = val.find('a').attrs['href']
                    # #print('href =', name_href)
                    # page_url = '/wiki/'+nom.replace(' ','_')
                    # print('page_url: ',page_url)
                    # else:
                    #     page_href = page_href+name_href.split(page_href[-3])[1]
                    #     print('reelle : ', page_href)
                    # if isinstance(name,bs4.element.Tag):
                    #     nom = name.string.lstrip().rstrip()
                    # else :
                    #     #manque le lien sur le nom
                    #     nom = val.text
                        #liste_incomplet.append([nom,commune,"pas de page liée"])
                if n == 1:
                    # recherche la commune et l'url_commune
                    commune = val.find('a').string.lstrip().rstrip()
                    #print ('commune =', commune)
                    # print('commune url = ', "/wiki/"+commune)

                if n == 2 and nom == '' :
                    # le nom est vide s'il y a une grosse ville (sauf métropole de lyon)
                    url_gc = val.find('a')['href']
                    url_gc = url_base+url_gc
                    #print ('url_grosse_commune = ',url_gc)
                    grande_commune=True
                    dat = getData(url_gc)
                    analyseSecondData(dat,url_gc,dic_mhs)

                # if n == 3:
                #     #analyse de la géolocalisation (inutile ?)
                #     rep = val.find('span', {'class':'geo-dec'})
                #     if isinstance(rep,bs4.element.Tag) :
                #         geo = val.find('span', {'class':'geo-dec'}).get_text().strip()
                #         lat =  geo.split(',')[0]
                #         lon =  geo.split(',')[1]
                #     else:
                #         #print ("Erreur : "+nom+" à "+commune+' -> Pas de Géolocalisation\n')
                #         liste_incomplet.append([nom,commune,"géolocalisation absente"])
                #         lat=lon=''

                if n == 4 and not grande_commune:
                    #recherche du code MHS
                    rep = val.find('cite', {'style':'font-style: normal'})
                    if isinstance(rep,bs4.element.Tag) :
                        code = rep.get_text().strip()
                        # print ('Mhs : ', code)
                        # mhs_url = val.find('a').attrs['href']
                        # print(mhs_url)
                    #enregistrement d'un momument si le code mhs existe
                        dic_mhs[code] = [nom,commune,url,identifiant]
                        # new_monument= Monument(code,nom,commune,identifiant)
                        # liste.append(new_monument)
                    else :
                        #print ("Erreur : Pas de code MHS pour "+nom+" à "+commune+'\n')
                        if 'erreur' in dic_mhs:
                            dic_mhs['erreur'].append([nom,commune,url,identifiant,"code MHS absent"])
                        else :
                            dic_mhs['erreur']=[[nom,commune,url_ville,identifiant,"code MHS absent"]]
                        #liste_mhs_absent.append([nom,commune,url,identifiant,"code MHS absent"])
                    grande_commune = False
    return dic_mhs

def analyseSecondData(data,url,dic_mhs):
    commune = url.split('_')[-1]
    url_ville = url.split('.org')[1]
    tableau =  data.find_all("table", "wikitable sortable")[0]
    for i, tr in enumerate(tableau):
        #print (i, type(tr), tr)

        if isinstance(tr,bs4.element.Tag):
            #l'id du monument permet de le retrouver dans la page
            if 'id' in tr.attrs:
                identifiant = tr.attrs['id']
                #print('Id = ',tr.attrs['id'])
            else:
                identifiant =''
            #     identifiant= tr.find('td').find('a')['title']
            td = tr.find_all('td')
            for n, val in enumerate(td):
                #print (n, val)
                code = ''
                #n=0 => nom du monument et lien vers la page Wp du monument
                if n == 0:
                    #print("typedeval = ",type(val.find('a')))
                    if isinstance(val.find('a'),bs4.element.Tag):
                        nom = val.find('a').text
                    elif val.find('a') == None:
                        nom = val.text
                    else :
                        nom =''
                    #print('name =',nom)
                    # #name_href = val.find('a').attrs['href']
                    # #print('href =', name_href)
                    # page_url = '/wiki/'+nom.replace(' ','_')
                    # print('page_url: ',page_url)
                    # else:
                    #     page_href = page_href+name_href.split(page_href[-3])[1]
                    #     print('reelle : ', page_href)
                    # if isinstance(name,bs4.element.Tag):
                    #     nom = name.string.lstrip().rstrip()
                    # else :
                    #     #manque le lien sur le nom
                    #     nom = val.text
                        #liste_incomplet.append([nom,commune,"pas de page liée"])
                if n == 1:
                    pass

                if n == 2 and nom == '' :
                    # # le nom est vide s'il y a une grosse ville (sauf métropole de lyon)
                    # url_gc = val.find('a')['href']
                    # url_gc = url_base+url_gc
                    # print ('url_grosse_commune = ',url_gc)
                    # grande_commune=True
                    # dat = getData(url_gc)
                    # analyseSecondData(dat,url_gc,dic_mhs)
                    pass
                # if n == 3:
                #     #analyse de la géolocalisation (inutile ?)
                #     rep = val.find('span', {'class':'geo-dec'})
                #     if isinstance(rep,bs4.element.Tag) :
                #         geo = val.find('span', {'class':'geo-dec'}).get_text().strip()
                #         lat =  geo.split(',')[0]
                #         lon =  geo.split(',')[1]
                #     else:
                #         #print ("Erreur : "+nom+" à "+commune+' -> Pas de Géolocalisation\n')
                #         liste_incomplet.append([nom,commune,"géolocalisation absente"])
                #         lat=lon=''

                if n == 3 :
                    #recherche du code MHS
                    rep = val.find('cite', {'style':'font-style: normal'})
                    if isinstance(rep,bs4.element.Tag) :
                        code = rep.get_text().strip()
                        # print ('Mhs : ', code)
                        # mhs_url = val.find('a').attrs['href']
                        # print(mhs_url)
                    #enregistrement d'un momument si le code mhs existe
                        dic_mhs[code] = [nom,commune,url,identifiant]
                        # new_monument= Monument(code,nom,commune,identifiant)
                        # liste.append(new_monument)
                    else :
                        #print ("Erreur : Pas de code MHS pour "+nom+" à "+commune+'\n')
                        dic_mhs['erreur'].append([nom,commune,url_ville,identifiant,"code MHS absent"])
                        #liste_mhs_absent.append([nom,commune,url,identifiant,"code MHS absent"])
                    #grande_commune = False
    return dic_mhs

def get_wikipedia(D):
    dic_mhs_wp = {}
    if D in dep:
        url_departement = dep[D]['url_d']
        url_dep_2 = dep[D]['url_d_2']
    else:
        exit()
    main_page = getData(url_base+url_departement)
    dic_mhs_wp = analyseData(main_page,url_base+url_departement,dic_mhs_wp)
    if url_dep_2 :
        main_page = getData(url_base+url_dep_2)
        dic_mhs_wp = analyseData(main_page,url_base+url_dep_2,dic_mhs_wp)
    dic_mhs_wp = OrderedDict(sorted(dic_mhs_wp.items(), key=lambda t: t[0]))
    return dic_mhs_wp

if __name__ == "__main__":
    dic_wp = {}
    dp="01"
    dic_wp = get_wikipedia(dp)
    for key in dic_wp:
        print (key,':',dic_wp[key][0])
    if 'erreur' in dic_wp:
        print ("Monuments {} dans Wikipédia = {}".format(dp,len(dic_wp)-1))
        print ('Erreurs = ', dic_wp['erreur'])
    else :
        print ("Monuments département {} dans Wikipédia = {}.".format(dp,len(dic_wp)))
    #print("Descriptions incompletes = {}".format(len(liste_incomplet)))
    # for erreur in liste_incomplet:
    #     #print (erreur)
    #     for E in erreur:
    #         if "MHS absent" in E:
    #             print("ERREUR : Pas de code MHS pour {}".format(erreur[0]))
    # for mhs in liste_mhs:
    #     print(mhs.mhs)
