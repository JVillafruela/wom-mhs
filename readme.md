Scripts Mhs
===========
Génération de pages web de comparaison de l'intégration des monuments historiques dans les bases de données Mérimée, Wikipédia et OpenStreetMap

- Le script gen_html.py génère des pages Html après avoir recherché les monuments dans chaque base et établi des tableaux comparatifs.

- Le site web résultat est visible sur http://wom.jearro.fr

- Chaque nuit, un cron lance la génération des pages, qui sont "gittées" sur https://github.com/JeaRRo/Wom (Exécution des scripts go.sh puis run.sh)

Install
------
    $ virtualenv mhs_env --no-site-packages -p /usr/bin/python3
    $ source ./mhs_env/bin/activate
    $ mkdir Wom
    $ git clone https://framagit.org/JeaRRo/Mhs.git
    $ cd Mhs
    $ cp -r css ../Wom/css
    $ cp -r images ../Wom/images
    $ cp -r js ..Wom/js
    $ pip install -r requirements.txt


Modules upgrade
------
    $ pip install --upgrade -r requirements.txt

Use
------
	$ python3 gen_html.py

  Pour les codes wikidata, il faut d'abord lancer JOSM (remoteControl) et aussi travailler par département :

    $ python3 gen_html.py -d 03 --wk
