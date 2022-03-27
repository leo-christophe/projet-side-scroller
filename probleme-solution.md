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
- Solution possible : Une solution est d'augmenter la vitesse du joueur pour qu'on ne voit pas le clignotement 

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
- Il fallait appeler la fonction music() au bon moment. 