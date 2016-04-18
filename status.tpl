<h3> Tableau comparatif des monuments pour le département {{ text_departement }}</h3>

% nb_m = len(merimee)
% nb_wp= len(wikipedia)
% nb_osm= len(osm)
% erreur_osm=[]
% note =""
<br>
Pour le département  {{ text_departement }}, la base Mérimée décrits {{nb_m}} monuments. Ils sont {{nb_wp}} dans wikipédia, et OSM en connait {{nb_osm}}.
</ul>
<br>
<table >
    <caption><h4> Tableau des Monuments </h4></caption>
    <tr>
        <th>Code Mérimée</th>
        <th>Description</th>
        <th>OSM</th>
        <th>WP</th>
        <th>Note </th>
    </tr>
    % l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    % for m, value in merimee.items() :
    <tr>
        <td><a href="{{l0}}{{m}}" target="blank">{{ m }}</a></td>
        <td>{{value[2]}}</td>
        % if m in osm :
            <td><a href="http://www.openstreetmap.org/browse/{{osm[m][0]}}" target="blank"> OSM </a></td>
            % if osm[m][-1] :
            %   erreur_osm = osm[m][-1]
            % else:
            %   erreur_osm =[]
            % end
        % else :
            <td>Absent OSM</td>
        % end
        % if m+"-Bis" in osm:
        %  mb = osm[m+"-Bis"]
        %    double = True
        % else:
        %   double = False
        % end
        % if m in wikipedia :
            <td> <a href="{{ wikipedia[m][2] }}#{{ wikipedia[m][3] }}" target="blank">  WP </a> </td>
        % else:
            <td>Absent WP</td>
        % end
        % if m in osm and erreur_osm :
        %   note = "Tags OSM absents : "+", ".join(erreur_osm)
        % end
        % if double :
                <td><a href="http://www.openstreetmap.org/browse/{{mb[0]}}" target="blank"> Dans OSM en double </a>  ; {{note}}</td>
        %else:
            <td> {{note}} </td>
        %end
        %note=""
    </tr>
    %end
</table>
