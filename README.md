# Yolobatch

Créera les .bat à votre place. Copier la ligne de commande MkvToolNix et le coller dans le script, il se chargera du reste.

### Comment l'utiliser ?

Le script se base sur le nommage, sur les noms des fichiers, il est donc important de ne pas les nommer n'importe comment. <br>
Deux nommages sont pris en compte: 
- Nom de la serie S01E01.mp4
- Nom de la serie 01.mkv / Nom.de.la.serie.01.hevc / Nom de la serie #01.avi / Nom de la serie #01.webm / Nom de la serie [01].cequetuveux<br>
Il est important d'avoir un nom qu'il fasse une lettre ou plusieurs mots pour que ça fonctionne.<br>
##### `01.mp4` on fait un petit effort de nommage svp<br>
#### Si le numéro est entre parenthèse il ne sera pas pris en compte : `Nom de la serie (01).mkv` => pas bon<br>
Il faudra aussi que tout les fichiers utilisé porte le même nom, à l'exception du numéro qui change, un warning sera affiché si ça n'est pas le cas.

### Requirements

Python 3.4+
`pip install colorama`

### Bible d'un nommage propre

Donner un nom. <br>
Les dates sont entre parenthèse juste après le nom de la série.<br>
Si on décide de mettre des points à la place des espaces on s'y tient pour tout le nom du fichier.<br>
Préciser les codecs utilisés est apprécié, importance sur le codec vidéo que sur l'audio car ce dernier est souvent moins problématique.<br>
Aller du plus important au moins important, VOSTFR / VF > caractéristique vidéo > caractéristique audio.<br>

### For all of my english friends

Just use google translate :), the warnings are in english btw I'm not that big of a ~~monster~~ baguette
