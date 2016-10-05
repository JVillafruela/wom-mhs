#!/opt//bin/bash
#
#  Copyright 2016 JeaRRo <jean.navarro@laposte.net>
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

#récupérer la date/heure
heure=$(date +%H:%M)
jour=$(date +%Y-%m-%d)

base_prod="/var/services/homes/jean/web_wom"
base_dev="/home/jean/osm/monuments_historiques/"
PROD=true
if [ $PROD = true ]; then
     base=$base_prod
else base=$base_dev
fi

cd $base

LANG="fr_FR.utf8"
export LANG

# activer l'environnement python3
source WOM_env/bin/activate

#git pull
cd ./Mhs

#lancer l'éxécution
python3 gen_html.py

# gitter les pages web et les pousser sur le serveur web
if [ $? -eq 0 ]; then
	cd ../Wom
	git add -A
	message="Pages web générées le $jour à $heure"
	git commit -am "$message"
	git push

################# à modifier pour la prod !!
	lftp ftp://user:motdepasse@serveurFtp -e "mirror -e -R -x .git /var/services/homes/jean/web_wom/Wom/. /www/wom/ ; quit"
	if [ $? -eq 0 ]; then
		heure=$(date +%H:%M)
		echo "Transfert vers le serveur : Ok le $jour à $heure"
	fi
#
# # finir
	deactivate
fi
