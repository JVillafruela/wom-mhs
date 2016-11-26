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

''' calculer une BBox '''

def getBB(lat,lon):
    deltaLat = 0.00043
    deltaLon = 0.000725
    if lat < 0 :
        top = lat - deltaLat
        bottom = lat + deltaLat
    else :
        top = lat + deltaLat
        bottom = lat - deltaLat

    left = lon - deltaLon
    right = lon + deltaLon
    return str(left),str(right),str(top),str(bottom)


if __name__ == "__main__":
    # lat = -20.9661665
    # lon = 55.6288341
    lon = 0.877774
    lat = 47.666316
    print (getBB(lat,lon))
