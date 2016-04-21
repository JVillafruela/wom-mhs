#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Génération de pages statiques directement en html
'''
import os,index



if __name__ == "__main__":
    d_dep ={'01':'Ain', '69':'Rhône','42':'Loire'}
    d_dep1 ={'01':'Ain'}
    ''' tester la présence d'une génération précédente et faire une sauvegarde'''
    ''' tester l'espace disque minimum requis pour la génération... qq Mo ?'''
    ''' générer la page index'''
    #index.gen_index(d_dep)
    '''générer les six pages de chaque département'''
    for d in d_dep1:
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
