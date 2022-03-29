# Présentation
- Ce jeu est un **side-scroller** dans lequel on progresse dans un **environnement 2D**. Le jeu se décomposera en **5 "mondes"**. Le premier aura un univers assez *campagnard*, les plaines et les champs. Le deuxième aura un univers *désertique*, le sable et la sécheresse. Le troisième aura un univers *montagnard*, neigeux et froid. Le quatrième aura un univers très chaud, semblable *aux enfers* et enfin, le cinquième sera *le Boss finale* du jeu. Ce jeu aura donc une fin : le boss. 
- Dans le but d'y arriver le joueur aura la possibilité **de récupérer des équipements**, **d'augmenter son niveau**, sa vie, sa force. Il pourra aussi acheter ces équipements dans des boutiques à l'aide de pièces.


# Changelog 
## V2:
- Ajout des classes pour charger les niveaux. 
- Changement du système de collisions.
- Ajout d'un menu permettant de changer quelques paramètres tel que l'activation de la musique ou du son, la résolution ou de quitter. 
- Ajout d'un son lorsqu'on clique sur un bouton du menu. 

## V1:
- Le joueur est maintenant géré à l'aide de la classe `Sprite_Player`.
- Changement de méthode pour les collisions avec `colliderect`. Les collisions sont maintenant beaucoup plus efficaces.
- Changement de **toutes les textures** et **ajout de textures** *(qui sont maintenant au nombre de 39) 18 pour le joueur lorsqu'il marche à gauche, 18 pour le joueur lorsqu'il marche à droite, 1 lorsqu'il saute, 1 lorsqu'il ne fait rien et 1 lorsqu'il regarde en l'air.*
=> Le joueur est maintenant d'une résolution de 32x64. 
- Ajout d'une animation pour le joueur avec la fonction `redrawWindow`
- Ajout d'une musique de fond et de sons de marche (facultatifs). 
#### Controles :
- Ajout de controles en plus des flèches:
> `q` pour aller à gauche, `d` pour aller à droite, `z` pour regarder en l'air, `la barre d'espace` pour sauter.
- Modification du fonctionnement du saut. Si le joueur regarde à droite, il va sauter vers la droite, s'il regarde à gauche, il va sauter vers la gauche, sinon, s'il regarde en l'air (z) ou s'il reste normal (debout), il saute tout droit. 
- Ajout de documentations, de commentaires, debut de la fiche probleme-solution, optimisation du code.

### Réparation de bugs:
- Saut à l'infini.
---
## V0:
- Ajout du joueur
- Ajout de collisions pour empêcher le joueur de dépasser les limites
- Ajout de gravité pour que le joueur redescende après avoir sauté.
- Ajout des controles pour que le joueur puisse sauter et se déplacer.
- Ajout de textures pour le joueur et l'arrière plan
- Ajout d'un moyen de quitter

# Conception :
- L'interface graphique est gérée avec Pygame. 
_Le programme est construit en 2 grandes parties :_
1. **L'initialisation** : Dans cette première partie, les variables, fonctions, classes sont initialisées. ça permet de "désengorger" la boucle principale du jeu qui tournera beaucoup de fois pendant plus ou moins longtemps. Dans cette partie, on a une classe : `Sprite_Player` qui gère le joueur, une fonction `redrawWindow` qui gère l'animation et on initialise plein de variables qui serviront pour la 2ème partie. 
2. **La boucle principale** : Elle permet le fonctionnement du jeu. En répétant la même boucle beaucoup de fois en une seconde, on fait en sorte de mettre à jour les affichages, après avoir fait bouger le personnage par exemple. On procède à chaque tour de boucle de la même façon : on change certaines choses comme la position du joueur ou sa texture, on met à jour, ça s'affiche. 

### Les images :
Il faut savoir que positionner les images n'est pas si facile. En effet, les positions sont assez spéciales. 
![](https://i.imgur.com/3ldvk3N.png)
La position initiale, (0,0) se trouve en haut à gauche de la fenêtre. Donc, si on descend, y augmente et si on va à droite, x augmente. À l'inverse, si on monte, y baisse et si on va à gauche, x baisse. 

### L'animation :
Elle est gérée grace à la fonction `redrawWindow()` qui est peut être traduit par "redessinage de la fenêtre". En effet, cette fonction permet d'effectuer une animation par rapport au joueur. Elle se sert de la variable `walkCount` comptant les "pas" du joueur. A chaque pas, la fonction va détecter si le joueur marche vers la gauche grace à `left` ou la droite grace à `right` et va afficher l'animation correspondante en prenant dans le tableau right_assets ou left_assets correspondant l'indice `walkCount`. Pour le saut, on détecte si le joueur est en train de sauter grace à `isJump`. 
**Il y a donc des variables ayant comme donnée des booléens pour chaque "stade" d'animation:** 
* >`right` pour signaler que le joueur va à droite.
* >`left` pour signaler que le joueur va à gauche.
* >`isJump` pour signaler que le joueur saute.
* >`isLookingUp` pour signaler que le joueur regarde en haut.
* >`isStanding` pour signaler que le joueur se tient juste debout.

# Idées futures / Ambitions pour la V3 :
- Un défilement vers la gauche tel un Mario. 
- La possibilitée de changer d'univers. (les 4 mondes) 
- Créer des ennemis et donc un moyen de les battre.
=> cela implique un moyen de perdre donc un écran "Game Over", un moyen de mourir de chute ou lorsqu'on saute dans le vide? 
- Ajouter un menu principal de début de jeu. 