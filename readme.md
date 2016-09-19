Scripts Mhs
===========
Génération de pages web de comparaison de l'intégration des monuments historiques dans les bases de données Mérimée, Wikipédia et OpenStreetMap

- Le script gen_html.py génère les pages web après avoir recherché les monuments dans chaque base et établi des tableaux comparatifs.

- Le site web résultat est visible sur http://jearro.fr/wom

- Chaque nuit, un cron lance la génération, puis pousse les fichiers html sur le serveur web (éxécution du script run.sh)

Install
------
    $ virtualenv mhs_env
    $ source ./mhs_env/bin/activate
    $ pip install -r requirements.txt

Modules upgrade
------
pip install --upgrade -r requirements.txt

Use
------
	$ python3 gen_html.py

ToDo
------
	- Traiter la France entière -> en cours dans la branche devFR
