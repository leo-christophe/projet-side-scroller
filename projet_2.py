import pygame

pygame.init()

#chargement de la fenêtre
taille = (1080, 720)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures")

clock = pygame.time.Clock()

image_fond = pygame.image.load("fond_plaines.png").convert()
fenetre.blit(image_fond, (0,0))

plateforme_principale_x = 165

pygame.display.flip()

image_joueur = pygame.image.load("bonhomme.png").convert_alpha()
size_player = image_joueur.get_size()
fenetre.blit(image_joueur, (size_player[1], 720 - size_player[1] - plateforme_principale_x))
position_perso = image_joueur.get_rect()

marge_x = 10
pygame.display.flip()
jeu = True
first_running = 0

import time

######################################################################? BOUCLE
while jeu:
    if first_running == 0:
        pygame.display.flip()
        position_perso.y = 720 - plateforme_principale_x
        fenetre.blit(image_joueur, (50, 720 - size_player[0] - plateforme_principale_x))
        first_running = 1
        pygame.display.flip()


    ######################################################################? CONTROLES
    if  pygame.key.get_pressed()[pygame.K_LEFT]:
        position_perso = position_perso.move(-marge_x, 0)
        fenetre.blit(image_joueur, position_perso)

    if  pygame.key.get_pressed()[pygame.K_RIGHT]:
        position_perso = position_perso.move(marge_x, 0)
        fenetre.blit(image_joueur, position_perso)

    """if pygame.key.get_pressed()[pygame.K_UP]:
        position_perso = position_perso.move(0, -marge_x)
        fenetre.blit(image_joueur, position_perso)"""


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()        
        
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                position_perso = position_perso.move(0, -marge_x-100)
                fenetre.blit(image_joueur, position_perso)
                print(1)


    #if pygame.key.get_pressed()[pygame.K_DOWN]:
        #position_perso = position_perso.move(0, 5)

    ######################################################################? COLLISIONS
    if position_perso[0] >= 1080 - size_player[0]:  #? Collisions d'à droite
        position_perso = position_perso.move(-10, 0)

    elif position_perso[0] <= 0 - size_player[0]: #? Collisions d'à gauche
        position_perso = position_perso.move(10, 0)

    elif position_perso[1] <= 0: #? Collisions du haut
        position_perso = position_perso.move(0, 10)

    elif position_perso[1] >= (720 - size_player[1] - plateforme_principale_x): #? Collision du bas (platforme)
        position_perso = position_perso.move(0, -10)

    elif position_perso[1] < (720 - size_player[1] - plateforme_principale_x):
        while position_perso[1] < (720 - size_player[1] - plateforme_principale_x -5):
            position_perso = position_perso.move(0, 1)

    fenetre.blit(image_fond, (0,0))
    fenetre.blit(image_joueur, position_perso)

    pygame.display.flip()
    clock.tick(120)




pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/