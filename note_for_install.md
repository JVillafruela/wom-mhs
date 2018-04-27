### Notes for new installation


* Voir le fichier __readme.md__ pour le début de l'installation

*  installer l'envoi de __mail__ : https://www.jbnet.fr/systeme/linux/linux-utiliser-gmail-en-relais-smtp-pour-exim4.html
  pour envoyer un fichier joint il faut construire le mail de la façon suivante :

  ```cat fichier | mail -s $date jean.ph.navarro@gmail.compl```

  Attention à passer en mode __INFO__ dans gen_html.py pour alléger le fichier envoyé

* Transférer le fichier __stats.json__ de l'ancien calculateur vers le nouveau sinon les stats seront perdus.
* Déplacer le fichier __ini.py__ à la racine des scripts

*  installer une nouvelle __clé ssh sur github__ dans la page "settings" puis "ssh & gpg keys" puis changer l'origin url : par exemple :
```  git remote set-url origin git@github.com:JeaRRo/Wom.git ```

* __Mailer les logs :  __
  modification du fichier run.sh :
  ```cat log/wom_$(date +%Y%m%d).log  | mail -s "Les logs de WOM  du $(date +%d/%m/%Y)" jean.ph.navarro@gmail.com ```

  Attention le répertoire __Mhs/log__ grandi tout le temps. Il faudra penser à le faire passer dans /var/log ce qui serait plus logique avec debian et permettrait la rotation plus facile de ces logs.

* __Installer le Cron__
  ```crontab -e ```  puis ajouter ``` 5 0  * * *   bash /home/jearro/osm/run.sh``` puis sauvegarder
