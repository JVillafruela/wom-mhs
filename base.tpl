<!DOCTYPE html>

<head>
    <meta content='text/html; charset=UTF-8' http-equiv='Content-Type'/>
    <title>{{Title or 'Sans titre' }}</title>
    <link href="/status/css/stylesheet.css" rel="stylesheet" media="all" type="text/css">
    <script type="text/javascript" src="/status/css/jquery-1.3.1.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function(){ 	// le document est chargé
       $("a").click(function(){ 	// on selectionne tous les liens et on d�finit une action quand on clique dessus
    	page=($(this).attr("href")); // on recuperer l' adresse du lien
    	$.ajax({  // ajax
    		url: page, // url de la page � charger
    		cache: false, // pas de mise en cache
    		success:function(tpl){ // si la requêté est un succès
    			afficher(html);	    // on execute la fonction afficher(donnees)
    		},
    		error:function(XMLHttpRequest, textStatus, errorThrows){ // erreur durant la requete
    		}
    	});
    	return false; // on desactive le lien
       });
    });

    function afficher(donnees){ // pour remplacer le contenu du div contenu
    	$("#contenu").empty(); // on vide le div
    	$("#contenu").append(donnees); // on met dans le div le r�sultat de la requete ajax
    }
    </script>
</head>
<html>
<body>
    {{!base}}
</body>
</html>
