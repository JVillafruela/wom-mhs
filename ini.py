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
# Les paramètres généraux

# Attention ce répertoire doit être créer avant le lancement du programme !
# racine des pages web
prod = False
# en local
url_dev = "/home/jean/osm/monuments_historiques"
# sur Syno
url_prod = "/home/jearro/osm"
# fichier statique : style.css
# cssFile ="style.css"

# les textes qui ne doivent pas apparaitre comme name= pour OSM
no_name = ['Immeuble', 'Maison', 'Maisons', 'Eglise', 'Église', 'Château', 'Ecurie', 'Ecuries', 'Écurie', 'Écuries', 'Presbytère', 'Beffroi', 'Cimetière', 'Prieuré', 'Remparts', 'Hôtel']

# Un dico des tags qui peuvent être attribué au MH à partir de son code TICO dans Mérimée.
other_tags = {
    'eglise': ["amenity=place_of_worship", "religion=christian", "building=church"],
    'maison': ["building=house", "historic=building"],
    'maisons': ["building=house", "historic=building"],
    'château': ["building=yes", "historic=castle"],
    'immeuble': ["historic=building"],
    'chapelle': ["building=chapel", "historic=yes"],
    'croix': ["historic=wayside_cross"],
    'manoir': ["historic=castle", "castle_type=manor"],
    'abbaye': ["historic=monastery", "religious_rank=abbey"],
    'dolmen': ["historic=archaeological_site", "site_type=megalith", "megalith_type=dolmen"],
    'tour': ["man_made=tower", "historic=yes"],
    'pont': ["historic=bridge"],
    'fontaine': ["amenity=fountain", "historic=yes"],
    'menhir': ["historic=archaeological_site", "site_type=megalith", "megalith_type=menhir"],
    'porte': ["historic=city_gate"],
    'ruine': ["ruin=yes"],
    'ruines': ["ruin=yes"],
    'couvent': ["historic=monastery", "monastery:type=convent"],
    'prieuré': ["historic=monastery"],
    'reste': ["ruin=yes"],
    'ferme': ["historic=farm"],
    'grange': ["historic=farm"],
    'vestige': ["ruin=yes"],
    'vestiges': ["ruin=yes"],
    'villa': ["historic=archaeological_site", "site_type=roman_villa"],
    "gallo-romaine": ["historic:civilization=ancient_roman"],
    "gallo-romain": ["historic:civilization=ancient_roman"],
    'palais': ["historic=castle", "castle_type=palace"],
    'rempart': ["historic=citywalls"],
    'remparts': ["historic=citywalls"],
    'romaine': ["historic:civilization=ancient_roman"],
    'cathédrale': ["amenity=place_of_worship", "religion=christian", "building=cathedral"],
    'grotte': ["natural=cave_entrance"],
    'calvaire': ["historic=wayside_cross"],
    'presbytère': ["religion=catholic"],
    'temple': ["amenity=place_of_worship", "building=temple"],
    'tumulus': ["historic=archaeological_site", "site_type=tumulus"],
    'borne': ["historic=milestone"],
    'protestante': ["religion=christian", "denomination=protestant"],
    'catholique': ["religion=christian", "denomination=catholic"],
    'oppidum': ["historic=archaeological_site", "site_type=fortification", "fortification_type=hill_fort"],
    'pigeonnier': ["man_made=dovecote", "historic=yes"],
    'phare': ["man_made=lighthouse", "historic=yes"],
    'donjon': ["man_made=tower", "tower:type=defensive", "defensive=donjon", "historic=yes"],
    'synagogue': ["amenity=place_of_worship", "religion=jewish", "building=synagogue"],
    'renaissance': ["historic:civilization=early_modern"],
    'polissoir': ["historic=stone", "stone_type=grooves"],
    'lavoir': ["amenity=lavoir"],
    'beffroi': ["man_made=tower", "tower:type=bell_tower", "historic=yes"],
    'clocher': ["man_made=tower", "tower:type=bell_tower", "historic=yes"],
    'monastère': ["historic=monastery", "monastery:type=monastery"],
    'statue': ["historic=memorial", "memorial_type=statue"],
    'cloître': ["building=cloister"],
    'abbatiale': ["amenity=place_of_worship", "religion=christian", "building=church"],
    'colombier': ["man_made=dovecote", "historic=yes"],
    'basilique': ["amenity=place_of_worship", "religion=christian", "building=church"],
    'obélisque': ["man_made=obelisk", "historic=yes"],
    'sépulture': ["historic=tomb"],
    'tombeau': ["historic=tomb"],
    'crypte': ["historic=tomb", "tomb=vault"],
    'nécropole': ["historic=archaeological_site", "site_type=necropolis"],
    'archéologique': ["historic=archaeological_site"],
    'néolithique': ["historic:civilization=prehistoric", "historic:period=stone-age", "historic:era=neolithic"],
    'écurie': ["building=stable", "historic=yes"],
    'tombe': ["historic=tomb"],
    'mausolée': ["historic=tomb", "tomb=mausoleum"],
    'mégalithe': ["historic=archaeological_site", "site_type=megalith"],
    'canon': ["historic=cannon"],
    "sous-préfecture": ["building=public", "historic=yes"],
    'halle': ["amenity=marketplace", "building=yes", "historic=yes"],
    'hôtel': ["historic=building"],
    'grenier': ["historic=yes", "building=barn"],
    'fort': ["historic=fort"],
    'fortification': ["historic=citywalls"],
    'fortifications': ["historic=citywalls"],
}
