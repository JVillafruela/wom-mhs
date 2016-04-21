<div class="TableComplet" >
    <div class="TableHeading">
        <div class="TableHead1">Mérimée</div>
        <div class="TableHead2">Description</div>
        <div class="TableHead1">OSM</div>
        <div class="TableHead1">WP</div>
        <div class="TableHead2">Note </div>
    </div>
    <div class="TableBody">
    % l0 = "http://www.culture.gouv.fr/public/mistral/mersri_fr?ACTION=CHERCHER&FIELD_1=REF&VALUE_1="
    % for d in complet:
        <div class="TableRow">
            <div class="TableCell1"><a href="{{l0}}{{d[0]}}" target="blank">{{ d[0] }}</a></div>
            <div class="TableCell2">{{d[1]}} -- {{d[2]}}</div>
            <div class="TableCell1"><a href="http://www.openstreetmap.org/browse/{{d[3]}}" target="blank"> OSM </a></div>
            <div class="TableCell1"> <a href="{{ d[8] }}" target="blank">  WP </a> </div>
            % if d[5] :
                <div class="TableCell2"><a href="http://www.openstreetmap.org/browse/{{d[6]}}" target="blank">Dans OSM en double</a>  ; {{",".join(d[4])}} {{",".join(d[7])}}</div>
            %else:
                <div class="TableCell2"> {{",".join(d[4])}} </div>
            %end
            %note=""
        </div>
    %end
</div>
</div>
