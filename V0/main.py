import pygame

pygame.init()

#chargement de la fenêtre
taille = (1080, 720)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures")

#fps
clock = pygame.time.Clock()

#chargement de la texture de fond d'écran
image_fond = pygame.image.load("assets/fond_plaines.png").convert()
fenetre.blit(image_fond, (0,0))

#chargement des textures du joueur (player_right et player_left ne servent pour l'instant à rien)
image_player = pygame.image.load("assets/player.png").convert_alpha()
image_player_right = pygame.image.load("assets/player_right_1.png").convert_alpha()
image_player_left = pygame.image.load("assets/player_left_1.png").convert_alpha()
#affichage du joueur et prise de stats
size_player = image_player.get_size()
plateforme_principale_x = 165
fenetre.blit(image_player, (size_player[1], 720 - size_player[1] - plateforme_principale_x))
position_perso = image_player.get_rect()

marge_x = 10
marge_y = 300

pygame.display.flip()

plateforme = (720 - size_player[1] - plateforme_principale_x)
first_running = 0

######################################################################? BOUCLE
jeu = True
while jeu:
    """
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, 
    le jeu continuera de marcher dès l'exécution du programme.
    """
    ######################################################################? CONTROLES
    if  pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_q]: #Q ou flèche de gauche pour aller à gauche
        position_perso = position_perso.move(-marge_x, 0)

    elif  pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]: #D ou flèche de droite pour aller à droite
        position_perso = position_perso.move(marge_x, 0)

    elif first_running == 0: #first running sert à spawn le joueur au correct endroit
        position_perso.y = 720 - plateforme_principale_x
        fenetre.blit(image_player, (50, 720 - size_player[0] - plateforme_principale_x))
        first_running = 1
    ######################################################################?
    for event in pygame.event.get(): #pour quitter
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN: #? Sauter
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                position_perso = position_perso.move(marge_x, -marge_y)
                fenetre.blit(image_player, position_perso)
    ######################################################################? COLLISIONS
    if position_perso[0] >= 1080 - size_player[0]:          #? Collisions d'à droite
        position_perso = position_perso.move(-10, 0)

    elif position_perso[0] <= 0 - size_player[0]:           #? Collisions d'à gauche
        position_perso = position_perso.move(10, 0)

    elif position_perso[1] <= 0:                            #? Collisions du haut
        position_perso = position_perso.move(0, 10)

    elif position_perso[1] >= (720 - size_player[1] - plateforme_principale_x): #? Collision du bas (platforme)
        position_perso = position_perso.move(0, -10)

    #? Gravité
    elif position_perso[1] < (plateforme - 20):
            position_perso = position_perso.move(0, 3)

    fenetre.blit(image_fond, (0,0))
    fenetre.blit(image_player, position_perso)

    pygame.display.flip()
    clock.tick(120)

pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/