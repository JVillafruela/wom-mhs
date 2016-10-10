#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2016 JeaRRo <jean.ph.navarro@gmail.com>
#  http://wiki.openstreetmap.org/wiki/User:JeaRRo
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
'''
    Lire le dico param.py et en faire une liste pour le menu principal
    copier le résultat dans le fichier js/select.js
'''

from __future__ import unicode_literals
import param
from collections import OrderedDict

def gen_list_dep():
    listDep = []
    dic = OrderedDict(sorted(param.dic_dep.items(), key=lambda t: t[0]))
    for code in dic :
        #print (code)
        name = param.dic_dep[code]['name']
        listDep.append(code+' - '+name)
    return listDep

if __name__ == "__main__":

    liste = gen_list_dep()
    print(liste)
