import pygame
from pygame import mixer
from random import randint
from menu_GUI import Game_Menu

grass_steps = [mixer.Sound(f'assets/sounds/ambiant/grass-step-{i}.mp3') for i in range(1, 4)]
sounds_playing = True


class Sprite_Player(pygame.sprite.Sprite):
    """
    La classe Sprite_Player prenant en argument pygame.sprite.Sprite est la classe permettant du joueur. Elle permet de récupérer des informations sur ce dernier,
    d'en modifier...
    """
    marge_x = 1
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
        self.right_assets = [pygame.image.load(f'assets/textures/player/player_right_{x}.png') for x in range(1, 19)]
        self.left_assets = [pygame.image.load(f'assets/textures/player/player_left_{x}.png') for x in range(1, 19)]
        
        self.left, self.right, self.isJump, self.isLookingUp, self.isStanding = False, False, False, False, False

        self.walkCount = 0

        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.x = self.size[0]
        self.rect.y = 720 - 150 - self.size[1]
        self.xoffset = self.rect.x
        self.yoffset = self.rect.y

        #? statistiques
        self.speed = 3
        self.vie = 100
        self.att = 1
        self.zone = 1 #? la zone du joueur

    def goRight(self, marge = marge_x):
        """
        La méthode goRight permet de déplacer le joueur de marge pixels vers la droite. 
        Pré-Condition : La méthode goRight prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        self.rect.x += marge * self.speed
        if sounds_playing == True:
            son = grass_steps[randint(0,2)]
            son.set_volume(0.25)
            son.play()
        return self.rect

    def goLeft(self, marge = marge_x):
        """
        La méthode goLeft permet de déplacer le joueur de marge pixels vers la gauche. 
        Pré-Condition : La méthode goLeft prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        self.rect.x -= marge * self.speed
        if sounds_playing == True:
            son = grass_steps[randint(0,2)]
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
        if self.rect.colliderect(fond_plaine_plateforme_pos) == 1:
            decalement_x = 120
            if self.isLookingUp or self.isStanding:
                self.rect.y -= jump * 1.5
            else:
                if self.left == True:
                    decalement_x = -(decalement_x) #? On change decalement_x en négatif s'il faut partir vers la gauche, sinon pas besoin (puisqu'il est positif)
                if self.left == False and self.right == False:
                    decalement_x = 0
                self.rect.y -= jump
                self.rect.x += decalement_x
            if sounds_playing == True:
                son = mixer.Sound(f'assets/sounds/ambiant/grass_jump.mp3')
                son.set_volume(0.25)
                son.play()
        return self.rect

    def controles(self):
        #! dans ces evenements, on ne peut pas rester appuyer sur la touche pour répéter l'évenement, il ne se produit qu'une fois à chaque touche appuyée. 
        for event in pygame.event.get(): #!pour quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN: #! sauter
                if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                    self.left, self.right, self.isJump, self.isLookingUp, self.isStanding = False, False, True, False, False
                    self.walkCount = 0
                    self.goJump()
                elif event.key == pygame.K_ESCAPE:
                    Game_Menu.menu_displaying = True

                else:
                    self.isJump = False
                    self.walkCount = 0
        
        #! dans ces evenements, on peut rester avec la touche appuyée pour continuer l'evenement qui s'arrête une fois que la touche n'est plus appuyée. 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: #!gauche
            self.left, self.right, self.isJump, self.isLookingUp, self.isStanding = True, False, False, False, False

            self.goLeft(Sprite_Player.marge_x)

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: #!droite
            self.left, self.right, self.isJump, self.isLookingUp, self.isStanding = False, True, False, False, False

            self.goRight(Sprite_Player.marge_x)

        elif keys[pygame.K_z]: #!regarder en haut (animation)
            self.left, self.right, self.isJump, self.isLookingUp, self.isStanding = False, False, False, True, False

        else:
            self.isJump, self.isLookingUp, self.isStanding = False, False, False
            self.walkCount = 0

    def collisions(self):
        #! COLLISIONS ET GRAVITÉ

        if self.rect.colliderect(fond_plaine_plateforme_pos) == 1: #! Collisions d'en bas
            self.rect.bottom = fond_plaine_plateforme_pos.top
        else:
            self.rect.y += 1
        
        if self.rect.x >= bg.get_width() - self.size[1]:             #! Collisions d'à droite
            self.rect = self.rect.move(-10, 0)

        elif self.rect.x <= 0:                                       #! Collisions d'à gauche
            self.rect = self.rect.move(10, 0)

        elif (self.rect.colliderect(fond_plaine_plateforme_pos)) == 0:
            self.rect = self.rect.move(0, 5)

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

collisions = []
bg = pygame.image.load("assets/textures/background/fond_plaines_2.png").convert()

fond_plaine_plateforme = pygame.image.load("assets/textures/background/fond_plaines_plateforme.png")
fond_plaine_plateforme_pos = fond_plaine_plateforme.get_rect()
collisions.append(fond_plaine_plateforme_pos)
fond_plaine_plateforme_pos.y = 546 #la position y de la plateforme qui du bas qui va servir de collision