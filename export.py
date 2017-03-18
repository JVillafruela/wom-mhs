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
    Faire un export des tags OSM dans un fichier csv pour mapcontrib
'''
import csv


def write_head(filename):
    ''' Ecrire l'entête du fichier csv '''
    with open(filename, 'w', newline='') as csvfile:
        mhswriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # mhswriter.writerow([
        #     'latitude', 'longitude', 'historic', 'start_date', 'ref:mhs', 'wikidata', 'name', 'heritage:operator', 'heritage',
        #     'mhs:inscription_date', 'source:heritage', 'wikipedia'])
        mhswriter.writerow([
            'latitude', 'longitude', 'historic', 'start_date', 'ref:mhs', 'wikidata', 'name', 'heritage',
            'mhs:inscription_date', 'wikipedia'])


def exporter(filename, geoloc, infos):
    # print(geoloc)
    if "%7C" in infos[0]:
        historic = infos[0].split('%7C')[0].split('=')[1]
        start_date = infos[0].split('%7C')[1].split('=')[1]
    elif "historic" in infos[0]:
        historic = infos[0].split('=')[1]
        start_date = ''
    elif "start_date" in infos[0]:
        historic = ''
        start_date = infos[0].split('=')[1]
    else:
        historic = ''
        start_date = ''

    if 'ref:mhs' in infos[1]:
        refmhs = infos[1].split('=')[1]
    else:
        refmhs = ''

    if 'wikidata' in infos[2]:
        wikidata = infos[2].split('=')[1]
    else:
        wikidata = ''

    if 'name' in infos[3]:
        name = infos[3].split('=')[1]
    else:
        name = ''

    # heritage_operator = 'mhs'

    if 'heritage' in infos[5]:
        heritage = infos[5].split('=')[1]
    else:
        heritage = ''

    if 'mhs:inscription_date' in infos[6]:
        mhs_incription_date = infos[6].split('=')[1]
    else:
        mhs_incription_date = ''

    # if 'source:heritage' in infos[-2]:
    #     source_heritage = infos[-2].split('=')[1]
    # else:
    #     source_heritage = ''

    if 'wikipedia' in infos[-1]:
        wikipedia = infos[-1].split('=')[1]
    else:
        wikipedia = ''

    with open(filename, 'a', newline='') as csvfile:
        mhswriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # mhswriter.writerow([
        #     float(geoloc.split(',')[0]), float(geoloc.split(',')[1]), historic, start_date, refmhs, wikidata, name, heritage_operator, heritage,
        #     mhs_incription_date, source_heritage, wikipedia
        # ])
        mhswriter.writerow([
            float(geoloc.split(',')[0]), float(geoloc.split(',')[1]), historic, start_date, refmhs, wikidata, name, heritage,
            mhs_incription_date, wikipedia
        ])


if __name__ == "__main__":

    filename = "export.csv"
    write_head(filename)

    geoloc = '45.90372322, 5.18000876'
    infos = [
        'historic=citywalls%7Cstart_date=15C', 'ref:mhs=PA00116527', 'wikidata=Q3424623', 'name=Rempart attenant à un immeuble', 'heritage:operator=mhs', 'heritage=2',
        'mhs:inscription_date=1921-11-24 ', 'source:heritage=data.gouv.fr, Ministère de la Culture - 2016', 'wikipedia=fr:Remparts de Pérouges']
    exporter(filename, geoloc, infos)
    # 45.90274191, 5.17916641
    #  ['historic=citywalls', 'ref:mhs=PA00116524', 'wikidata=Q3424623', 'name=Rempart attenant à un immeuble', 'heritage:operator=mhs', 'heritage=2', 'mhs:inscription_date=1921-11-24 ', 'source:heritage=data.gouv.fr, Ministère de la Culture - 2016', 'wikipedia=fr:Remparts de Pérouges']
    geoloc = '45.90274191, 5.17916641'
    infos = [
        'historic=citywalls', 'ref:mhs=PA00116524', 'wikidata=Q3424623', 'name=Rempart attenant à un immeuble', 'heritage:operator=mhs', 'heritage=2',
        'mhs:inscription_date=1921-11-24 ', 'source:heritage=data.gouv.fr, Ministère de la Culture - 2016', 'wikipedia=fr:Remparts de Pérouges']
    exporter(filename, geoloc, infos)
