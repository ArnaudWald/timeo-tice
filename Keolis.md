Keolis "open-data" : XML Realtime API
=====================================

Les données retournées sont au format XML.

Document trouvé et modifié depuis [Pastebin](http://pastebin.com/eEumTXw1).

Récupérer la liste des lignes
-----------------------------

	http://timeo3.keolis.com/relais/<code_réseau>.php?xml=1

Renvoie la liste des lignes et les identifiants associés

Récupérer la liste des arrêts pour une ligne et un sens données
---------------------------------------------------------------

	http://timeo3.keolis.com/relais/<code_réseau>.php?xml=1&ligne=<id_ligne>&sens=<id_sens>

Voir le contenu de la première URL pour l'id d'une ligne et les sens (généralement "A" et "R").
Les références des arrêts sont à utiliser pour obtenir les horaires des prochains passages.

Récupérer les horaires des prochains passages pour une ligne et un arrêt donné
------------------------------------------------------------------------------

	http://timeo3.keolis.com/relais/<code_réseau>.php?xml=3&refs=<référence_arret>&ran=1

Voir le contenu de la seconde URL pour les références des arrêts.
L'utilité du paramètre "ran" est inconnue mais il est nécessaire.

Il est également possible de récupérer les horaires pour plusieurs arrêts en les séparant par des point-virgules dans le paramètre refs.

	http://timeo3.keolis.com/relais/<code_réseau>.php?xml=3&refs=<référence_arret>;<référence_arret>;<référence_arret>&ran=1

Codes réseau
------------

|        Ville       | Code réseau |
| ------------------ |:-----------:|
| Le Mans            |     105     |
| Pau                |     117     |
| Soissons           |     120     |
| Aix-en-Provence    |     135     |
| Caen               |     147     |
| Dijon              |     217     |
| Brest              |     297     |
| Pau-Agen           |     402     |
| Blois              |     416     |
| St-Étienne         |     422     |
| Nantes             |     440     |
| Montargis          |     457     |
| Angers             |     497     |
| Macon-Villefranche |     691     |
| Épinay-sur-Orge    |     910     |
| Rennes             |     999     |
