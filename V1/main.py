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

plateforme_principale_x = 165

marge_x = 10
marge_y = 80

#fps
clock = pygame.time.Clock()

#chargement de la texture de fond d'écran
image_fond = pygame.image.load("assets/fond_plaines.png").convert()
fenetre.blit(image_fond, (0,0))


import pygame

class Sprite_Player(pygame.sprite.Sprite):
    def __init__(self, longueur=64, largeur=64):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
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
        return self.rect

    def goLeft(self, marge):
        self.rect.x -= marge
        self.x -= marge
        return self.rect

    def goJump(self, jump):
        if current_player.rect.colliderect(fond_plaine_plateforme_pos) == True:
            self.rect.y -= jump
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
left = False
right = False

def redrawWindow(player, left, right):
    global walkCount
    fenetre.blit(image_fond, (0, 0))
    if left == True:
        fenetre.blit(left_assets[0], (player.x, player.y))  
    elif right == True:
        fenetre.blit(right_assets[0], (player.x, player.y))
    elif right == False and left == False:
        fenetre.blit(player.image, (player.x, player.y))
    pygame.display.flip()


fond_plaine_plateforme = pygame.image.load("assets/fond_plaines_plateforme.png")
fenetre.blit(fond_plaine_plateforme, (0, 0))
fond_plaine_plateforme_pos = fond_plaine_plateforme.get_rect()


pygame.display.flip()

first_running = 0
jeu = True
while jeu:
    """
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    if first_running == 0: #first running sert à spawn le joueur au correct endroit
        current_player.rect.y = 490
        fond_plaine_plateforme_pos.y = 547
        first_running = 1
    ######################################################################?
    for event in pygame.event.get(): #pour quitter
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN: #? Sauter
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                current_player.goJump(marge_y)
    #https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_q]:
        left = True
        right = False
        current_player.goLeft(marge_x)

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        right = True
        left = False
        current_player.goRight(marge_x)

    #current_player.rect
    #fond_plaine_plateforme_pos
    print(fond_plaine_plateforme_pos.bottom)
    if current_player.rect.colliderect(fond_plaine_plateforme_pos) == True:
        current_player.rect.bottom = fond_plaine_plateforme_pos.top
        print("i")

    ######################################################################? COLLISIONS
    if current_player.rect[0] >= 1080 - current_player.size[1]:
        left = True
        right = False          #? Collisions d'à droite
        current_player.rect = current_player.rect.move(-10, 0)

    elif current_player.rect[0] <= 0 - current_player.size[1]:
        right = True
        left = False          #? Collisions d'à gauche
        current_player.rect = current_player.rect.move(10, 0)

    elif current_player.rect[1] <= 0:   
        left = False
        right = False                         #? Collisions du haut
        current_player.rect = current_player.rect.move(0, 10)

    if current_player.rect.colliderect(fond_plaine_plateforme_pos) == False:
        left = False
        right = False
        current_player.rect = current_player.rect.move(0, 10)

    """elif current_player.rect[1] >= (720 - current_player.size[1] - plateforme_principale_x): #? Collision du bas (platforme)
        left = False
        right = False
        current_player.rect = current_player.rect.move(0, -10)"""

    #? Gravité
    

    all_sprites.update()
    all_sprites.draw(fenetre)

    fenetre.blit(image_fond, (0,0))
    fenetre.blit(fond_plaine_plateforme, fond_plaine_plateforme_pos)
    fenetre.blit(current_player.image, current_player.rect)

    pygame.display.flip()
    clock.tick(60)

    """redrawWindow(current_player, left, right)"""

pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/