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
    $ pip install -r requirements.txt

Modules upgrade
------
pip install --upgrade -r requirements.txt

Use
------
	$ python3 gen_html.py

ToDo
------
	 - Certaines villes de France ont des pages Wikipédia qui ne sont pas liées à leur pages départementales et donc non traitées par le script.
                Voir le fichier paramSpecial.py
     - Certains monuments ont une référence unique dans Mérimée mais plusieurs codes wikidata et donc plusieurs pages wikipédia.
                OSM ne propose qu'un seul code wikidata par ref Mérimée. A corriger.
