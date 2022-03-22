import pygame
pygame.init()

#chargement de la fenêtre
WIDTH = 1080
HEIGHT = 720
taille = (WIDTH, HEIGHT)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures")

right = [
    pygame.image.load('assets/player_right_1.png'),
    pygame.image.load('assets/player_right_2.png')
]

left = [
    pygame.image.load('assets/player_left_1.png'),
    pygame.image.load('assets/player_left_2.png')
]

standing = pygame.image.load("assets/player.png")

plateforme_principale_x = 165

marge_x = 10
marge_y = 40

#fps
clock = pygame.time.Clock()

#chargement de la texture de fond d'écran
image_fond = pygame.image.load("assets/fond_plaines.png").convert()
fenetre.blit(image_fond, (0,0))

import pygame

class Sprite_Player(pygame.sprite.Sprite):
    def __init__(self, longueur=32, largeur=32):
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
        return self.rect

    def goLeft(self, marge):
        self.rect.x -= marge
        return self.rect

    def goJump(self, jump):
        self.rect.y -= jump
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

def redrawWindow():
    global walkCount
    fenetre.blit(image_fond, (0, 0))
    pygame.display.flip()

first_running = 0
jeu = True
while jeu:
    """
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    pygame.time.delay(1)
    if first_running == 0: #first running sert à spawn le joueur au correct endroit
        current_player.y = 720 - plateforme_principale_x
        fenetre.blit(current_player.image, (50, 720 - current_player.size[1] - plateforme_principale_x))
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

    elif current_player.rect[1] >= (720 - current_player.size[1] - plateforme_principale_x): #? Collision du bas (platforme)
        left = False
        right = False
        current_player.rect = current_player.rect.move(0, -10)

    #? Gravité
    elif current_player.rect[1] < (plateforme - 20):
        left = False
        right = False
        current_player.rect = current_player.rect.move(0, 5)

    all_sprites.update()
    all_sprites.draw(fenetre)
    clock.tick(60)
    fenetre.blit(image_fond, (0,0))
    fenetre.blit(current_player.image, current_player.rect)

    pygame.display.flip()
    clock.tick(60)

    redrawWindow()
pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/