% rebase('base.tpl', Title='Correspondance Base Mérimée aux données dans Wikipédia et OSM')
<div class="Bandeau">
<h3> Tableau comparatif des monuments pour le département {{ text_departement }}</h3>

% erreur_osm=[]
% note =""
<br>
Pour le département  {{ text_departement }}, la base Mérimée décrit {{comptes[0]}} monuments. Ils sont {{comptes[1]}} dans wikipédia, et OSM en connait {{comptes[2]}}.
<br>
Il y a {{len(complet)}} monuments de la base Mérimée présents à la fois dans OSM et Wikipédia.
</div>
<a href="/status/css/complet.html">  table complète </a>   <a href="/status/css/wp_absent.html"> Absent WP </a>

<div id="contenu">


</div>
