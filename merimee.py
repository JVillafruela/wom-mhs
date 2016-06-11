#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Rechercher et lire le fichier .json de la base mérimée et extraire
    les codes mhs des monuments d'un département. Un test sur la date de version est effectué et la nouvelle version est
    téléchargée si nécéssaire.
    Entrée : le code d'un département  = '01'
    Sortie : un musee avec une clé par code MHS
        'ref:mhs':[le code insee commune,le nom de la commune, adresse, le nom du monument, infos classement avec dates]

'''
from __future__ import unicode_literals
import requests,json
from bs4 import BeautifulSoup
import mohist,ini

new_date=''
datafile='merimee-MH.json'

def get_commune(code):
	'''
    faire une requette sur http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1=IA01000159
    pour récupérer le nom de la commune d'un monument s'il ne fait pas partie de la base ouverte
	'''
	url= "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
	r = requests.get(url+code)
	contenu = r.text
	page= BeautifulSoup(contenu,'html.parser')
	tableau=  page.find_all("td", attrs={"class":u"champ"})[2].text
	return tableau.split("; ")[-1]

def get_url():
    if ini.prod:
        url = ini.url_prod+'/Mhs/'
    else:
        url = ini.url_dev+'/Mhs/'
    return url

def conv_date(d):
	'''
		en entrée une date dans une liste ['24', 'mai', '2016']
		en sortie une date dans une chaine AAMMJJ '20160524' (permetre une comparaison)
	'''
	mois = ["Janvier", u"Février", "Mars", "Avril", "Mai", "Juin", "Juillet", u"Août",
		"Septembtre", "Octobre", "Novembre", u"Décembre"]
	return d[2]+str(mois.index(d[1].capitalize())+1).zfill(2)+d[0]

def existe_nouvelle_version():
	'''
    	La base Mérimée est récupérable sur data.gouv.fr sur la page
    	http://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/
    	rechercher la date de la version du dataset.json
    	et le comparer à la dernière version enregistrée
    	télécharger : http://data.culture.fr/entrepot/MERIMEE/
	'''
	global new_date
	url ="http://www.data.gouv.fr/fr/datasets/monuments-historiques-liste-des-immeubles-proteges-au-titre-des-monuments-historiques/"
	contenu = requests.get(url).text
	page= BeautifulSoup(contenu,'html.parser')
	date = page.find("p", attrs={"class": "list-group-item-text ellipsis"}).text
	old_date = open('last_date.txt','r').read()
	new_date= conv_date(date.strip().split(' ')[-3:])
	return new_date > old_date

def get_maj_base_merimee():
    '''
        Tester si une nouvelle version est disponible : si oui la télécharge
    '''
    url_locale=get_url()

    if existe_nouvelle_version():
        print ('Nouvelle version disponible ! Téléchargement... ')
        url_merimee= "http://data.culture.fr/entrepot/MERIMEE/"
        r=requests.get(url_merimee+datafile,stream=True)
        with open(url_locale+datafile, 'wb') as fd:
            for chunk in r.iter_content(4096):
                fd.write(chunk)
        open(url_locale+'last_date.txt','w').write(new_date)
    else :
        print('Base Mérimée : Version {}, à jour.'.format(new_date))


def get_merimee(dep,musee):
    '''
         Recherche sur le code département (01)
         les champs du fichier json :
         REF|ETUD|REG|DPT|COM|INSEE|TICO|ADRS|STAT|AFFE|PPRO|DPRO|AUTR|SCLE
         Renvoie un musee contenant des monuments par reférence mhs contenant la clé 'mer' avec la note 1
     '''
    global datafile
    url_locale=get_url()

    with open(url_locale+datafile) as data_file:
	       data = json.load(data_file)

    for mh in data[:-1]:
        if mh['DPT'] == dep:
			# print('mhs : ',mh['REF'])
			# print (' insee :',mh['INSEE'],'\n','commune :',mh['COM'],'\n',\
			#		'adresse:',mh['ADRS'],'\n','nom monument :',mh['TICO'],'\n','Classement :',mh['DPRO'])
            MH=musee.add_Mh(mh['REF'])
            #m.add_infos_mer('insee','commune','adresse','Nom mh', 'Infos classement')
            MH.add_infos_mer(mh['INSEE'],mh['COM'],mh['ADRS'],mh['TICO'],mh['DPRO'])
    return musee

if __name__ == "__main__":
    departement = '42'
    get_maj_base_merimee()
    musee = mohist.Musee()
    musee = get_merimee(ini.dep[departement]['code'],musee)
    # for mh,MH in musee.collection.items():
    #     print(mh, MH)
    #     for key,value in MH.description[mh]['mer'].items():
    #         print (key,':',value)
    print("Pour le département {}, il y a {} monuments dans la base Mérimée.".format(departement,len(musee.collection)))
    #print(dic_merimee['PA01000038'])
    musee.maj_salle()
    print(musee)

    nb=musee.get_nb_MH('mer')
    print(nb)
