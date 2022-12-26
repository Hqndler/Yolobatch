# Yolobatch

Créera les .bat à votre place. Copier la ligne de commande MkvToolNix et la coller dans le script, il se chargera du reste.

### Requirements

Python 3.6+
`pip install colorama pyperclip`

### Comportement

Lors d'un batch, le premier épisode servira d'exemple pour tout les autres, ils auront tous les même propriétés. Si la piste 2 est mise en défaut alors toutes les autres piste 2 le seront aussi.

### Comment l'utiliser ?

Lancer le script dans un terminal et suivre les instructions. Seulement la ligne de commande est nécessaire, pas le JSON.<br>
>`python yolobatch.py`<br>

Le script est basé sur le nommage, il est donc important de bien nommer tout ses fichiers. Un message d'erreur sera affiché si mal nommé.<br>
Plusieurs regex sont utilisées :
1. [Relatif](https://regex101.com/r/Eawjea/1) -> `Something 01 Videos Propreties.extension`<br>
La regex accepte les caractères suivant : `espace`, "\[" pour l'ouverture et "\]" pour la fermeture, '\_' (underscore), '.' (point) et '#' juste avant le numéro.<br>
Le numéro doit faire minimum 2 chiffres (01 à 09 compris).<br>
Le but est de ne pas avoir à renommer le fichier.<br>

Quelques exemples : `Something #01 someting.extension`, `Something - [1337][something not new].old`, `Somethin_01_something.avi` or `Something.01.something.mp4`<br>

2. [Saison](https://regex101.com/r/Eawjea/3) -> `Someting S01E01 Videos Propreties.extension`<br>
La regex commence au 'S' et termine au dernier chiffre du numéro de l'épisode.<br>
La regex statifait la structure suivante "SXXEXX" (le numéro de l'épisode peut faire plus que deux chiffres).<br>

Cliquez sur les liens pour vérifier les regex.

### L'exception du titre

Le titre du mkv peut être changé avec le script s'il contient un numéro suivant la regex "Relatif", à l'exception qu'il n'y a pas besoin de caractères de fermeture.<br>
Un nom correct ressemble à ça : `Episode 01` (sans de caractère après le 1).

### Ajouter des polices avec l'argument -f

Le script peut être lancer avec l'argument -f pour ouvrir un menu spécial.<br>
Pour que ça fonctionne, il a besoin d'autant de dossier qu'il y a d'épisode. Chacun des fichiers devra contenir des polices, utilisées dans l'ass du dit épisode.<br>
Ces dossiers peuvent être créer et remplis soit en le faisant à la main, soit en utilisant mon autre script dispo [ici](https://github.com/Hqndler/AssFontCollector)<br>
Ça devrait ressembler à [ça](https://github.com/Hqndler/AssFontCollector/blob/main/Output%20proof%20for%20ALL_IN_ONE%20False.png).<br>
Plus qu'à coller le chemin du dossier contenant tout ces dossiers (eux même contenant les polices). Comment ça plus de polices muxée inutilement.

### Bible d'un nommage propre
Liste non exhaustive des éléments importants à prendre en compte lors du nommage, ceci n'est que mon avis :
- Donner un nom, pas de 01.mkv, 02.mkv etc on est un minimum précis. <br>
- Si on décide de mettre des points à la place des espaces on s'y tient pour tout le nom du fichier.<br>
- Préciser les codecs utilisés est apprécié, importance particulière portée sur le codec vidéo que sur l'audio car ce dernier étant souvent moins problématique.<br>
- Les dates sont entre parenthèse juste après le nom de la série.<br>
- Aller du plus important au moins important, VOSTFR / VF > caractéristique vidéo > caractéristique audio.<br>
