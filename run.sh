#!/bin/bash

base_prod="/var/services/homes/jean/web_wom"
base_dev="/home/jean/osm/monuments_historiques/"
PROD=true
if [ $PROD = true ]; then
    base=$base_prod
else base=$base_dev
fi
#récupérer la date/heure
heure=$(date +%H:%M)
jour=$(date +%d-%m-%Y)

# Récupérer la dernière version du programme
# cd Mhs
# git fetch
# cd ..

#lancer l'éxécution
# source WOM_env/bin/activate
cd Mhs
python3 gen_html.py

# gitter les pages web et les pousser sur le serveur web
cd ../Wom
git add -A


message="Pages web générées le $jour à $heure"
#echo $message
#echo $base
git commit -am "$message"

################# à modifier pour la prod !!
# lftp ftp://user:password@ftp.server -e "mirror -e -R /var/services/homes/jean/web_wom/Wom/ /www/wom/ ; quit"
#
#
# # finir
# deactivate
