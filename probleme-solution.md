# Fiche problèmes - solutions :

### Problème 1 : On peut sauter à l'infini en spammant la touche de saut / La gravité ne marche pas vraiment. 
- En appuyant très rapidement sur la même touche de saut, on peut monter très très haut. 
- J'ai trouvé la solution quand j'ai réfléchi aux collisions. Mon raisonnement était qu'on peut faire en sorte que le joueur ne puisse pas sauter tant qu'il n'y a pas collision avec le sol. 
- Solution : Utilisation de .colliderect qui permet d'enregistrer des collisions effiacement. Grace à cela, j'ai pu faire en sorte que si le joueur n'est pas en collision, il ne peut pas sauter. 

### Problème 2 : L'animation est presque invisible.
- Lorsque le joueur est animé, on ne le voit pas vraiment. 
- J'ai trouvé la solution en regardant un tutoriel.
- Solution : Il faut plus d'images à animer. Quelques images ne suffisent pas car le jeu met à jour les affichages très rapidement. J'ai donc refait toutes les textures et j'ai fait en sorte d'avoir 18 images lorsque le joueur marche vers la droite ou vers la gauche. 

### Problème 3 : L'animation clignote. 
- Lorsque le joueur est animé, il clignote. 
- J'ai trouvé cette solution en recherchant sur Internet. Beaucoup disent qu'il faut limiter les lignes `pygame.display.flip` mais, même avec une limitation, ça clignote toujours. 
- Solution possible : Une solution est d'augmenter la vitesse du joueur pour qu'on ne voit pas le clignotement : **rejetée car cela deviendrait trop impossible à gérer**

### Problème 4 : Faire un menu.
- Je ne sais pas vraiment comment faire un menu sous pygame, ou plus generalement afficher du texte. 
- J'ai trouvé la solution en regardant la documentation officielle et quelques tutoriels. 
- Solution trouvée : On gère cela avec une classe et des textes de la même forme que les plateformes.

### Problème 5 : Le défilement.
- Il y a très peu de solutions qui arrangent par rapport au défilement. On peut faire un défilement automatique mais ça enlève de la liberté au joueur. On peut faire un travail sur la caméra suivant le joueur mais je crains ne pas pouvoir y arriver ou on peut, à la place du défilement faire un système de "chambres", c'est-à-dire, que lorsqu'on arrive à la limite de la carte, le joueur est comme "téléporté" dans une autre carte et ainsi de suite. Ce serait la solution la plus simple et rapide.
- J'ai trouvé la solution en réfléchissant sur le sujet pendant un bon moment.
- On va choisir la solution des chambres car j'ai perdu trop de temps à essayer de produire le défilement, il reste encore beaucoup de choses à faire tel que les ennemis.  

### Problème 6 : La musique.
- En implémentant mon idée de menu, j'ai essayé d'implémenter un menu d'options, pour changer des paramètres. A ce moment la, je n'ai pas réussi à configurer la musique correctement et elle a tout simplement arrêté d'être jouée.
- J'ai trouvée la solution en revenant en arrière et en repensant le concept du code. J'ai remarqué cela en testant : la fonction music marche parfaitement donc c'est quand on l'appel qu'il faut changer. Solution : l'appeler quand on change un paramètre : musique activée, musique désactivée. 
- Il fallait appeler la fonction `music()` au bon moment. 

### Problème 7 : Les collisions.
- Les collisions ne marchent pas du tout. 
- J'ai trouvé cette solution en revenant beaucoup de fois sur mon code, en retestant...
- Il faut tester si le joueur est dans les bonnes positions en x et y (s'il est trop à droite ou trop à gauche, il ne faut pas qu'il y ait de collisions)
Puis il faut tester si le joueur est à l'intérieur du bloc, parce que si c'est le cas, il faut qu'il ne puisse pas sauter.

### Problème 8 : Problème de croix.
- La croix de selection dans le menu est vraiment mal placée.
- J'ai modifié la taille de la croix pour qu'elle soit plus petite et je la place à droite du texte au lieu d'au dessus. 

### Problème 9 : FPS
- Lorsqu'on change les FPS, le joueur ralentis ou accélère.
- J'ai trouvé la solution en cherchant sur Internet et en regardant des tutoriels. Enfaite, c'est du 
- Il faut adapter la vitesse de marche selon les FPS. Si les FPS sont à `144`, la vitesse sera égal à `VITESSE / 144` (par exemple)

### Problème 10 : Le saut
- Le saut est ne paraît pas vraiment naturel. 
- J'ai trouvé la solution en regardant des tutoriels. (https://www.youtube.com/watch?v=am2Tb_tj8zM)
- La solution consiste à utiliser une variable de `velocité` que l'on va baisser, ce qui va permettre d'avoir un saut plus naturel. 

### Problème 11 : Dans l'écran "Game Over"
- Le saut jouait plusieurs fois en même temps.
- J'ai trouvé la solution en paufinant un peu le code, en ajoutant une boucle while. 
- La solution : Je joue le son de Game Over avant de répéter l'écran Game Over dans une boucle. De ce fait, le son est joué indépendamment de boucle et ne peut être répété qu'unu seule fois. 