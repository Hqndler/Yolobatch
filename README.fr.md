# Yolobatch

Permet de créer les .bat à votre place. Copier la ligne de commande MkvToolNix et la coller dans le script, il se chargera du reste.

## Requirements

Python 3.6+
`pip install colorama pyperclip`

## Comment l'utiliser ?

Faire le premier mkv normalement dans MkvToolNix, copier la ligne de commande `Multiplexeur -> Affichier la ligne de commande`, lancer un terminal puis<br>
>`python yolobatch.py`<br>

Fini !

## Comportement

Le script va récupérer tout les fichiers d'entrée, de sortie, chapitre et titre et va incrementer les numbres contenu dedans. Une bonne numérotation est impérative pour le bon fonctionnement du script.

### Ajouter des polices avec l'argument -f

`python yolobatch.py -f "<path>"` avec <path> étant le dossier parent contenant tout les dossiers contenant eux même les polices que vous voulez mettre dans votre mkv.<br>
Il devra y avoir autant de dossier qu'il y a d'épisode. Chacun des dossiers devra contenir des polices, utilisées dans l'ass du dit épisode.<br>
Ces dossiers peuvent être créer et remplis soit en le faisant à la main grâce à aegisub, soit en utilisant mon autre script dispo [ici](https://github.com/Hqndler/AssFontCollector)<br>
Ça devrait ressembler à ce que mon autre script créer.<br>
Comment ça plus de polices muxée inutilement.

### Façon de numéroter supportée

Ce script utilise des regex pour savoir ce qui doit être incrémenté, une petite liste des numérotatio supportée :
- `S01E01` / `s01e01` pour vérifier la regex c'est [ici](https://regex101.com/r/QEEEZV/1)
- `<espace>01<espace>`, `[01]`, `_01_`, `.01.`, `#01 ` pour vérifier la regex c'est [ici](https://regex101.com/r/4FQCIN/1)
- `01x01` (pour saison 01 épisode 01) pour vérifier la regex c'est [ici](https://regex101.com/r/yMGDZP/1)

Les regex sont vérifiée dans cette ordre mais la dernière risque de posée problème. Si votre façon de numéroter ne passe pas les deux premières regex et que la troisième regex est utilisée, si dans votre nom de fichier vous avez mis la résolution sous cette forme `1280x720`, alors vous êtes dans le cas très spécifique où 720 va être incrémenté. Dans le doute, préférez utiliser la première façon de numéroter pour éviter tout problème.

Le nommage "flemmard" est aussi supporté : `01.mkv` est un nom valide de fichier.

Vous pouvez vérifier les regex avec vos noms de fichier en clicant sur le lien.

### Devrait aussi fonctionner sous Linux et MacOS

## Bible d'un nommage propre
Liste non exhaustive des éléments importants à prendre en compte lors du nommage, ceci n'est que mon avis :
- Donner un nom, pas de 01.mkv, 02.mkv etc on est un minimum précis. <br>
- Si on décide de mettre des points à la place des espaces on s'y tient pour tout le nom du fichier.<br>
- Préciser les codecs utilisés est apprécié, importance particulière portée sur le codec vidéo que sur l'audio car ce dernier étant souvent moins problématique.<br>
- Les dates sont entre parenthèse juste après le nom de la série.<br>
- Aller du plus important au moins important, VOSTFR / VF > caractéristique vidéo > caractéristique audio.<br>

### Une étoile sur le repo est fortement appréciée. En vous remerciant.
