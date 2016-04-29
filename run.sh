#!/bin/bash
#récupérer la date/heure
heure=$(date +%H:%M)
jour=$(date +%Y-%m-%d)
LOG_FILE="../log/out_gen_"$jour"_"$heure.log
ERR_FILE="../log/err_gen_"$jour"_"$heure.log

exec 1>$LOG_FILE
exec 2>$ERR_FILE

# base_prod="/var/services/homes/jean/web_wom"
# base_dev="/home/jean/osm/monuments_historiques/"
# PROD=true
# if [ $PROD = true ]; then
#     base=$base_prod
# else base=$base_dev
# fi


# Récupérer la dernière version du programme

git pull


#lancer l'éxécution
# source WOM_env/bin/activate

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
