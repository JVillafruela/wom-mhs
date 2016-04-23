#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
    Organisation des infos MH dans une Class MoHist
'''
import merimee
from collections import OrderedDict

class Musee:
    '''
        un musée contient des monuments historiques
    '''
    def __init__(self,nom):
        self.collection = {}
        self.nom=nom

    def trier(self):
        '''Renvoie la collection triée'''
        return OrderedDict(sorted(self.collection.items(), key=lambda t: t[0]))

class MoHist:
    '''
        un monument historique
    '''
    ctr_monument=0

    def __init__(self, ref_mhs=None):
        if ref_mhs:
            self.mhs=ref_mhs
        else:
            self.mhs = "no_mhs_"+str(MoHist.ctr_monument)
        self.description={self.mhs:{"mer":{},"osm":{},"wip":{}}}
        #la catégorie du monument => résultat des tests en fonciton de la source mer,osm,wip
        self.cat=""
        MoHist.ctr_monument+=1



def charge_merimee(dep,musee):
    ''' Créer les MH à partir de la base Mérimée
    dic_merimee =>  {ref:mhs :[N°insee_commune, Nom commune, Nom monument, infos classement avec dates]}'''
    dic_mer = merimee.get_merimee(dep)
    for mhs in dic_mer:
        if mhs not in musee.collection:
            m=MoHist(mhs)
            m.description[mhs]["mer"]['insee']=dic_mer[mhs][0]
            m.description[mhs]['mer']['commune']=dic_mer[mhs][1]
            m.description[mhs]['mer']['nom']=dic_mer[mhs][2]
            m.description[mhs]['mer']['classement']=dic_mer[mhs][3]
            musee.collection[mhs]=m
        else:
            print ("Alerte !! monument {} en double".format(mhs))

if __name__ == "__main__":
    Ain=Musee('Ain')
    #charge departement, musee
    charge_merimee('01',Ain)
    # Mh.charge_merimee('01'')
    print(len(Ain.collection))
    #print(Ain.collection['PA00116330'].description['PA00116330']['mer'])
    Ain_trier=Ain.trier()
    for m,value in Ain_trier.items():
        print(value.description[m]['mer']['commune'])
