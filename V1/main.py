import pygame
from pygame import mixer
pygame.init()

#chargement de la fenêtre
WIDTH = 1080
HEIGHT = 720
taille = (WIDTH, HEIGHT)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures") 
icon = pygame.image.load("assets/textures/player/player.png")
pygame.display.set_icon(icon) #on change l'icone de la fenêtre

image_fond = pygame.image.load("assets/textures/background/fond_plaines.png").convert()
fond_plaine_plateforme = pygame.image.load("assets/textures/background/fond_plaines_plateforme.png")
fond_plaine_plateforme_pos = fond_plaine_plateforme.get_rect()
fond_plaine_plateforme_pos.y = 546 #la position y de la plateforme qui du bas qui va servir de collision

grass_step = [
    mixer.Sound('assets/sounds/ambiant/grass-step-1.mp3'),
    mixer.Sound('assets/sounds/ambiant/grass-step-2.mp3'),
    mixer.Sound('assets/sounds/ambiant/grass-step-3.mp3')
]
grass_sound = False

clock = pygame.time.Clock() #on va pouvoir changer les fps
from random import randint
class Sprite_Player(pygame.sprite.Sprite):
    """
    La classe Sprite_Player prenant en argument pygame.sprite.Sprite est la classe permettant du joueur. Elle permet de récupérer des informations sur ce dernier,
    d'en modifier...
    """
    marge_x = 3
    marge_y = 80
    def __init__(self):
        """
        La méthode __init__ permet d'initialiser le joueur. 
        """
        super().__init__() #appel du constructeur de la classe parente Sprite
        pygame.sprite.Sprite.__init__(self)

        #? image et coordonnées
        self.image = pygame.image.load("assets/textures/player/player.png")
        self.jumping = pygame.image.load("assets/textures/player/player_jumping.png")
        self.looking_up = pygame.image.load("assets/textures/player/player_looking_up.png")
        self.right_assets = [
    pygame.image.load('assets/textures/player/player_right_1.png'), pygame.image.load('assets/textures/player/player_right_2.png'),
    pygame.image.load('assets/textures/player/player_right_3.png'), pygame.image.load('assets/textures/player/player_right_4.png'),
    pygame.image.load('assets/textures/player/player_right_5.png'), pygame.image.load('assets/textures/player/player_right_6.png'),
    pygame.image.load('assets/textures/player/player_right_7.png'), pygame.image.load('assets/textures/player/player_right_8.png'),
    pygame.image.load('assets/textures/player/player_right_9.png'), pygame.image.load('assets/textures/player/player_right_10.png'),
    pygame.image.load('assets/textures/player/player_right_11.png'), pygame.image.load('assets/textures/player/player_right_12.png'),
    pygame.image.load('assets/textures/player/player_right_13.png'), pygame.image.load('assets/textures/player/player_right_14.png'),
    pygame.image.load('assets/textures/player/player_right_15.png'), pygame.image.load('assets/textures/player/player_right_16.png'),
    pygame.image.load('assets/textures/player/player_right_17.png'), pygame.image.load('assets/textures/player/player_right_18.png')
]
        self.left_assets = [
    pygame.image.load('assets/textures/player/player_left_1.png'), pygame.image.load('assets/textures/player/player_left_2.png'),
    pygame.image.load('assets/textures/player/player_left_3.png'), pygame.image.load('assets/textures/player/player_left_4.png'),
    pygame.image.load('assets/textures/player/player_left_5.png'), pygame.image.load('assets/textures/player/player_left_6.png'),
    pygame.image.load('assets/textures/player/player_left_7.png'), pygame.image.load('assets/textures/player/player_left_8.png'),
    pygame.image.load('assets/textures/player/player_left_9.png'), pygame.image.load('assets/textures/player/player_left_10.png'),
    pygame.image.load('assets/textures/player/player_left_11.png'), pygame.image.load('assets/textures/player/player_left_12.png'),
    pygame.image.load('assets/textures/player/player_left_13.png'), pygame.image.load('assets/textures/player/player_left_14.png'),
    pygame.image.load('assets/textures/player/player_left_15.png'), pygame.image.load('assets/textures/player/player_left_16.png'),
    pygame.image.load('assets/textures/player/player_left_17.png'), pygame.image.load('assets/textures/player/player_left_18.png')
]
        self.size = self.image.get_size()

        self.rect = self.image.get_rect()
        self.rect.x = self.size[0]
        self.rect.y = 720 - 150 - self.size[1]

        #? statistiques
        self.speed = 3
        self.vie = 100
        self.att = 1
    
    def goRight(self, marge):
        """
        La méthode goRight permet de déplacer le joueur de marge pixels vers la droite. 
        Pré-Condition : La méthode goRight prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        self.rect.x += marge * self.speed
        if grass_sound == True:
            son = grass_step[randint(0,2)]
            son.set_volume(0.25)
            son.play()
        return self.rect

    def goLeft(self, marge):
        """
        La méthode goLeft permet de déplacer le joueur de marge pixels vers la gauche. 
        Pré-Condition : La méthode goLeft prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        self.rect.x -= marge * self.speed
        if grass_sound == True:
            son = grass_step[randint(0,2)]
            son.set_volume(0.25)
            son.play()
        return self.rect

    def goJump(self, jump = 60):
        """
        La méthode goJump permet de faire sauter le joueur de jump pixels. 
        Pré-Condition : Elle prend en argument jump, qui sera pratiquemment tout le temps à 150.
        left permet de faire sauter le joueur vers la gauche et right permet de faire sauter le joueur vers la droite.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        if self.rect.colliderect(fond_plaine_plateforme_pos) == True:
            decalement_x = 60
            if isLookingUp or isStanding:
                self.rect.y -= jump
            else:
                if left == True:
                    decalement_x = -(decalement_x) #? On change decalement_x en négatif s'il faut partir vers la gauche, sinon pas besoin (puisqu'il est positif)
                if left == False and right == False:
                    decalement_x = 0
                self.rect.y -= jump
                self.rect.x += decalement_x
        return self.rect

    def soin(self, soin):
        """
        Cette méthode permet de soigner le joueur.
        Pré-Condition : soin est un float correspondant aux points de vie ajoutés à la vie du joueur.
        """
        assert type(soin) == float
        if self.soin < 100:
            self.soin += soin
        else:
            print("Il n'y a rien à soigner.")

    def degat(self, degats):
        """
        Cette méthode permet d'infliger des dégâts au joueur.
        Pré-Condition : degats est un float correspondant aux points de dégat infligés au joueur, enlevant de la vie. 
        """
        assert type(degats) == float
        self.vie -= degats
        if self.vie < 0:
            self.vie = 0

#! Le joueur 
fps = 60
current_player = Sprite_Player()

def redrawWindow(left, right):
    """
    Cette fonction sert à faire les animations.
    Pré-Conditions : left et right sont des booléens indiquant la position du joueur (vers la droite ou vers la gauche)
    """
    global walkCount

    pos = (current_player.rect.x, current_player.rect.y)
    if walkCount <= 17: 
        if left: #on utilise chaque élément du tableau left_assets
            fenetre.blit(current_player.left_assets[walkCount], pos)
            walkCount +=1

        elif right: #on utilise chaque élément du tableau right_assets
            fenetre.blit(current_player.right_assets[walkCount], pos)
            walkCount += 1

        elif isJump:
            fenetre.blit(current_player.jumping, pos)

        elif isLookingUp:
            fenetre.blit(current_player.looking_up, pos)
        else:
            fenetre.blit(current_player.image, current_player.rect)
    else:
        walkCount = 0

music = False
if music == True: #jouer de la musique
    mixer.music.load("assets/sounds/music/grassy_plains-darren_curtis.mp3")
    mixer.music.play(-1)

left = False
right = False
isJump = False
isLookingUp = False
isStanding = False
walkCount = 0

######################################################################! BOUCLE
jeu = True
while jeu:
    """
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    for event in pygame.event.get(): #!pour quitter
        if event.type == pygame.QUIT:
            jeu = False
            pygame.quit()
        
        elif event.type == pygame.KEYDOWN: #! sauter
            if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                isJump = True
                walkCount = 0
                current_player.goJump()
            else:
                isJump = False
                walkCount = 0
        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_q]: #!gauche
        right = False
        left = True
        
        isLookingUp = False
        isStanding = False
        isJump = False
        current_player.goLeft(Sprite_Player.marge_x)

    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: #!droite
        left = False
        right = True
        isLookingUp = False
        isStanding = False
        isJump = False
        current_player.goRight(Sprite_Player.marge_x)

    elif keys[pygame.K_z]: #!regarder en haut (animation)
        isLookingUp = True
        isStanding = False
        right = False
        left = False
        isJump = False

    else:
        isLookingUp = False
        isJump = False
        walkCount = 0

    #! COLLISIONS ET GRAVITÉ
    if current_player.rect.colliderect(fond_plaine_plateforme_pos) == True: #! Collisions d'en bas
        current_player.rect.bottom = fond_plaine_plateforme_pos.top

    if current_player.rect.x >= 1080 - current_player.size[1]:             #! Collisions d'à droite
        current_player.rect = current_player.rect.move(-10, 0)

    elif current_player.rect.x <= 0:                                       #! Collisions d'à gauche
        current_player.rect = current_player.rect.move(10, 0)

    elif not(current_player.rect.colliderect(fond_plaine_plateforme_pos)): #! Gravité
        current_player.rect = current_player.rect.move(0, 5)

    fenetre.blit(image_fond, (0,0))

    redrawWindow(left, right) #animations
    
    pygame.display.flip() #rafraichissement de la fenêtre

    #Rafraichissement des différentes images.
    fenetre.blit(fond_plaine_plateforme, fond_plaine_plateforme_pos)
    
    clock.tick(fps) #change les fps du jeu.
    
pygame.QUIT()

#(Des liens pour des tutos)
#TODO https://pygame-gui.readthedocs.io/en/latest/quick_start.html
#TODO http://sdz.tdct.org/sdz/interface-graphique-pygame-pour-python.html 
#TODO https://coderslegacy.com/python/pygame-gravity-and-jumping/
#TODO #https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/pygame-animation/
#TODO pygame.transform très intéréssant
#TODO SONS https://www.youtube.com/watch?v=pcdB2s2y4Qc
#TODO défilement http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
#TODO MENU https://www.reddit.com/r/pygame/duplicates/rwbfl3/make_a_menu_in_pygame_and_python_in_5_min_using/
#TODO https://www.geeksforgeeks.org/how-to-create-a-text-input-box-with-pygame/?ref=rp
#TODO PLATEFORMES QUI BOUGENT http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
#TODO Examples cool http://programarcadegames.com/index.php?chapter=introduction_to_sprites
#TODO https://sciences-du-numerique.fr/tuto-pygame/sprites.html