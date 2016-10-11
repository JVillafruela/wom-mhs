#!/opt//bin/bash
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
# Script bash de lancement de la génération des pages html.

#récupérer la date/heure
heure=$(date +%H:%M)
jour=$(date +%Y-%m-%d)

base_prod="/home/jearro/osm"
base_dev="/home/jean/osm/monuments_historiques"
PROD=true
if [ $PROD = true ];
    then
        base=$base_prod
    else
        base=$base_dev
fi

cd $base

LANG="fr_FR.utf8"
export LANG

# activer l'environnement python3
source WOM_env/bin/activate
cd ./Mhs

#lancer la génération des fichiers html
python3 gen_html.py > /dev/null 2>&1

# gitter les pages html sur github.com (génération web automatique)
if [ $? -eq 0 ]; then
	cd ../Wom
	git add -A
	message="Pages web générées le $jour à $heure"
	git commit -am "$message"
	git push

# # finir
	deactivate
fi
