from sys import float_repr_style
import pygame
pygame.init()

#chargement de la fenêtre
WIDTH = 1080
HEIGHT = 720
taille = (WIDTH, HEIGHT)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures") 
icon = pygame.image.load("assets/player.png")
pygame.display.set_icon(icon)

right_assets = [
    pygame.image.load('assets/player_right_1.png'),
    pygame.image.load('assets/player_right_2.png')
]

left_assets = [
    pygame.image.load('assets/player_left_1.png'),
    pygame.image.load('assets/player_left_2.png')
]

standing = pygame.image.load("assets/player.png")
jumping = pygame.image.load("assets/player_jumping.png")
looking_up = pygame.image.load("assets/player_looking_up.png")
image_fond = pygame.image.load("assets/fond_plaines.png").convert()
fond_plaine_plateforme = pygame.image.load("assets/fond_plaines_plateforme.png")
fond_plaine_plateforme_pos = fond_plaine_plateforme.get_rect()

plateforme_principale_x = 165

marge_x = 10
marge_y = 80

#fps
clock = pygame.time.Clock()

#chargement de la texture de fond d'écran




import pygame

class Sprite_Player(pygame.sprite.Sprite):
    def __init__(self, longueur=64, largeur=64):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.left= False
        self.right= False
        self.image = pygame.image.load("assets/player.png")
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.pos = (self.size[1], 720 - self.size[1] - 165)
        self.x = self.size[1]
        self.y = 720 - self.size[1] - 165

        fenetre.blit(self.image, self.pos)
        self.rect = self.image.get_rect()

        self.vie = 100
        self.att = 1

    def goRight(self, marge):
        self.rect.x += marge
        self.x += marge
        global right
        global left
        self.right = True
        self.left = False
        return self.rect

    def goLeft(self, marge):
        self.rect.x -= marge
        self.x -= marge
        global right
        global left
        self.left = True
        self.right = False
        return self.rect

    def goJump(self, jump=150, left=False, right=False):
        global isJump
        if current_player.rect.colliderect(fond_plaine_plateforme_pos) == True:
            decalement_x = 40
            if self.left == True:
                self.rect.y -= jump
                self.rect.x -= decalement_x
            elif self.right == True:
                self.rect.y -= jump
                self.rect.x += decalement_x
            else:
                self.rect.y -= jump
            isJump = True
        else:
            isJump = False
        self.y -= jump

        return self.rect

    def soin(self, vie):
        if self.vie < 100:
            self.vie += vie
        else:
            print("Il n'y a rien à soigner.")

    def degat(self, degats):
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0
    
pygame.display.flip()

#####################################################################?

all_sprites = pygame.sprite.Group()

current_player = Sprite_Player()
current_player.rect.x = current_player.size[1]
current_player.rect.y = 720 - 150 - current_player.size[1]

plateforme_x = 150
plateforme = (720 - current_player.size[1] - plateforme_principale_x)

all_sprites.add(current_player)

######################################################################? BOUCLE
walkCount = 0
from random import randint
def redrawWindow(player, left, right):
    """
    Cette fonction sert à faire les animations.
    """
    global walkCount
    fenetre.blit(image_fond, (0, 0))

    if walkCount > 1:
        walkCount = 0
    if left:
        clock.tick(45)
        fenetre.blit(left_assets[walkCount], (current_player.rect.x, current_player.rect.y))
        walkCount +=1
    elif right:
        clock.tick(45)
        fenetre.blit(right_assets[walkCount], (current_player.rect.x, current_player.rect.y))
        walkCount += 1
    elif isJump:
        fenetre.blit(jumping, (current_player.rect.x, current_player.rect.y))
    else:
        if randint(0,100) > 2:
            fenetre.blit(current_player.image, (current_player.rect.x, current_player.rect.y))
        else:
            fenetre.blit(looking_up, (current_player.rect.x, current_player.rect.y))

    pygame.display.flip()

pygame.display.flip()



fps = 60
left = False
right = False
isJump = False
isLookingUp = False
walkCount = 0
first_running = 0
jeu = True
while jeu:
    clock.tick(fps)
    """
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    if first_running == 0: #first running sert à tout placer au correct endroit
        current_player.rect.y = 490
        fond_plaine_plateforme_pos.y = 547
        first_running = 1
    ######################################################################?
    print(walkCount)
    pygame.time.delay(10)
    for event in pygame.event.get(): #pour quitter
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN: #! sauter
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                current_player.goJump(left=left, right=right)
            else:
                isJump = False
                walkCount = 0
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_q]: #!gauche
        left = True
        right = False
        isLookingUp = False
        current_player.goLeft(marge_x)

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: #!droite
        right = True
        left = False
        isLookingUp = False
        current_player.goRight(marge_x)
    elif keys[pygame.K_z]: #!regarder en haut (animation)
        right = False
        left = False
        isLookingUp = False
    else:
        right = False
        left = False
        if randint(0,10) > 7:
            isLookingUp = True
        walkCount = 0

    #COLLISIONS AVEC LA PLATEFORME
    if current_player.rect.colliderect(fond_plaine_plateforme_pos) == True:
        current_player.rect.bottom = fond_plaine_plateforme_pos.top

    ######################################################################? COLLISIONS
    if current_player.rect[0] >= 1080 - current_player.size[1]: #? Collisions d'à droite
        current_player.rect = current_player.rect.move(-10, 0)

    elif current_player.rect[0] <= 0 - current_player.size[1]:  #? Collisions d'à gauche
        current_player.rect = current_player.rect.move(10, 0)

    elif current_player.rect[1] <= 0:                         #? Collisions du haut
        current_player.rect = current_player.rect.move(0, 10)

    elif not(current_player.rect.colliderect(fond_plaine_plateforme_pos)):
        current_player.rect = current_player.rect.move(0, 10)
    else:
        left = False
        right = False
        walkCount = 0


    all_sprites.update()
    all_sprites.draw(fenetre)

    fenetre.blit(image_fond, (0,0))
    fenetre.blit(fond_plaine_plateforme, fond_plaine_plateforme_pos)
    fenetre.blit(current_player.image, current_player.rect)

    pygame.display.flip()
    

    redrawWindow(current_player, left, right)

pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/
#TODO #https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/