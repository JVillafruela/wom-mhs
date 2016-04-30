#!/opt/bin/bash
#récupérer la date/heure
heure=$(date +%H:%M)
jour=$(date +%Y-%m-%d)
#LOG_FILE="../log/out_gen_"$jour"_"$heure.log
#ERR_FILE="../log/err_gen_"$jour"_"$heure.log

#exec 1>$LOG_FILE
#exec 2>$ERR_FILE

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

source WOM_env/bin/activate

# Récupérer la dernière version du programme
#git pull

cd ./Mhs

#lancer l'éxécution de la génération
python3 gen_html.py
# Ne pas effectuer les synchros si le script s'est planté
if [ $? -eq 0 ]; then
    # gitter les pages web et les pousser sur le serveur web

    cd ../Wom
    git add -A

    message="Pages web générées le $jour à $heure"
    #echo $message
    #echo $base
    git commit -am "$message"
    git push

    ################# à modifier pour la prod !!
    lftp ftp://user:password@ftp.server -e "mirror -e -R -x /var/services/homes/jean/web_wom/Wom/.git /var/services/homes/jean/web_wom/Wom/ /www/wom/ ; quit"
    #
    #
    # finir
     deactivate
if
