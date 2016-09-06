#!/opt//bin/bash


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

# nettoyer les répertoires des pages web
rm -rf Wom/01_pages/*
rm -rf Wom/03_pages/*
rm -rf Wom/27_pages/*
rm -rf Wom/38_pages/*
rm -rf Wom/42_pages/*
rm -rf Wom/69_pages/*

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
