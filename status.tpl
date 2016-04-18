% rebase('base.tpl', Title='Correspondance Base Mérimée aux données dans Wikipédia et OSM')

<h3> Tableau comparatif des monuments pour le département {{ text_departement }}</h3>

% nb_m = len(merimee)
% nb_wp= len(wikipedia)
% nb_osm= len(osm)
% erreur_osm=[]
% note =""
<br>
Pour le département  {{ text_departement }}, la base Mérimée décrit {{nb_m}} monuments. Ils sont {{nb_wp}} dans wikipédia, et OSM en connait {{nb_osm}}.
<br>
<caption><h4> Tableau des Monuments </h4></caption>
<div class="Table" >
    <div class="TableHeading">
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead2">Description</div>
        <div class="TableHead1">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead2">Note </div>
    </div>
    <div class="TableBody">
    % l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    % for m, value in merimee.items() :
        <div class="TableRow">
            <div class="TableCell1"><a href="{{l0}}{{m}}" target="blank">{{ m }}</a></div>
            <div class="TableCell2">{{value[2]}}</div>
            % if m in osm :
                <div class="TableCell1"><a href="http://www.openstreetmap.org/browse/{{osm[m][0]}}" target="blank"> OSM </a></div>
                % if osm[m][-1] :
                %   erreur_osm = osm[m][-1]
                % else:
                %   erreur_osm =[]
                % end
            % else :
                <div class="TableCell1-err">Absent OSM</div>
            % end
            % if m+"-Bis" in osm:
            %  mb = osm[m+"-Bis"]
            %    double = True
            % else:
            %   double = False
            % end
            % if m in wikipedia :
                <div class="TableCell1"> <a href="{{ wikipedia[m][2] }}#{{ wikipedia[m][3] }}" target="blank">  WP </a> </div>
            % else:
                <div class="TableCell1-err">Absent WP</div>
            % end
            % if m in osm and erreur_osm :
            %   note = "Tags OSM absents : "+", ".join(erreur_osm)
            % end
            % if double :
                    <div class="TableCell2"><a href="http://www.openstreetmap.org/browse/{{mb[0]}}" target="blank">Dans OSM en double</a>  ; {{note}}</div>
            %else:
                <div class="TableCell2"> {{note}} </div>
            %end
            %note=""
        </div>
    %end
</div>
</div>
