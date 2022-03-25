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