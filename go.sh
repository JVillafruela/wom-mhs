#!/opt/bin/bash

# Ce script (go.sh) est exécuté sur un Nas, lancé par un cron chaque nuit. Il réveille une machine plus puissante (Pentium M) en wakeonlan,
# lui fait exécuter (run.sh) le script gen_html.py de génération des pages html Wom, puis éteint cette machine.

# reveil machine (Portable dell D410 Pentium M)
/opt/bin/wakelan 00:13:72:6E:66:89


machine="172.16.0.55"
temps=5 # 5 second
ssh jearro@$machine 'exit' > /dev/null 2>&1
while [ `echo $?` -eq  255  ]; do
    sleep $temps
    ssh jearro@$machine 'exit' > /dev/null 2>&1
done;

echo "Connexion ok - Lancement mise à jour"
#Exécution de la mise à jour
ssh jearro@$machine 'cd osm && ./run.sh'

echo "Mise à jour complète - extinction"
# extinction du portable
ssh jearro@$machine 'sudo shutdown -h 1 && exit'
