import pygame
from pygame import mixer
from random import randint
pygame.init()

#chargement de la fenêtre
WIDTH = 1080
HEIGHT = 720
taille = (WIDTH, HEIGHT)
fenetre = pygame.display.set_mode(taille)   
pygame.display.set_caption("Juan Adventures") 
icon = pygame.image.load("assets/textures/player/player.png")
pygame.display.set_icon(icon) #on change l'icone de la fenêtre
collisions = []

bg = pygame.image.load("assets/textures/background/fond_plaines_2.png")
bgX = 0
bgX2 = 3000
fond_plaine_plateforme = pygame.image.load("assets/textures/background/fond_plaines_plateforme.png")
fond_plaine_plateforme_pos = fond_plaine_plateforme.get_rect()
collisions.append(fond_plaine_plateforme_pos)
fond_plaine_plateforme_pos.y = 546 #la position y de la plateforme qui du bas qui va servir de collision

clock = pygame.time.Clock() #on va pouvoir changer les fps

grass_sound = True
grass_steps = [mixer.Sound(f'assets/sounds/ambiant/grass-step-{i}.mp3') for i in range(1, 4)]

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
        
        self.left = False
        self.right = False
        self.isJump = False
        self.isLookingUp = False
        self.isStanding = False
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
        if grass_sound == True:
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
        if grass_sound == True:
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
            if grass_sound == True:
                son = mixer.Sound(f'assets/sounds/ambiant/grass_jump.mp3')
                son.set_volume(0.25)
                son.play()
        return self.rect

    def controles(self):
        #! dans ces evenements, on ne peut pas rester appuyer sur la touche pour répéter l'évenement, il ne se produit qu'une fois à chaque touche appuyée. 
        for event in pygame.event.get(): #!pour quitter
            if event.type == pygame.QUIT:
                jeu = False
                pygame.quit()
                quit()
            
            elif event.type == pygame.KEYDOWN: #! sauter
                if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                    current_player.isJump = True
                    current_player.walkCount = 0
                    current_player.goJump()
                else:
                    current_player.isJump = False
                    current_player.walkCount = 0
        
        #! dans ces evenements, on peut rester avec la touche appuyée pour continuer l'evenement qui s'arrête une fois que la touche n'est plus appuyée. 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: #!gauche
            current_player.right = False
            current_player.left = True
            current_player.isLookingUp = False
            current_player.isStanding = False
            current_player.isJump = False

            current_player.goLeft(Sprite_Player.marge_x)

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: #!droite
            current_player.left = False
            current_player.right = True
            current_player.isLookingUp = False
            current_player.isStanding = False
            current_player.isJump = False

            current_player.goRight(Sprite_Player.marge_x)

        elif keys[pygame.K_z]: #!regarder en haut (animation)
            current_player.isLookingUp = True
            current_player.isStanding = False
            current_player.right = False
            current_player.left = False
            current_player.isJump = False

        else:
            current_player.isStanding = False
            current_player.isLookingUp = False
            current_player.isJump = False
            current_player.walkCount = 0

    def collisions(self):
        #! COLLISIONS ET GRAVITÉ
        if current_player.rect.colliderect(fond_plaine_plateforme_pos) == 1: #! Collisions d'en bas
            current_player.rect.bottom = fond_plaine_plateforme_pos.top
        else:
            current_player.rect.y -= 1
        
        if current_player.rect.x >= bg.get_width() - current_player.size[1]:             #! Collisions d'à droite
            current_player.rect = current_player.rect.move(-10, 0)

        elif current_player.rect.x <= 0:                                       #! Collisions d'à gauche
            current_player.rect = current_player.rect.move(10, 0)

        elif (current_player.rect.colliderect(fond_plaine_plateforme_pos)) == False or (
            current_player.rect.x > fond_plaine_plateforme_pos.get_size()[0] or current_player.rect.x < 0
        ): #! Gravité
            current_player.rect = current_player.rect.move(0, 5)

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
current_player = Sprite_Player()


music_playing = True
def music():
    """
    Cette fonction gère la musique du jeu. Elle prend en compte music_playing, un booléen représentant la volonté d'avoir de la musique dans le jeu et l'occupation
    de la "queue musicale". C'est-à-dire, que, si il y a déjà une musique en cours, on ne peut pas jouer de musique. 
    Elle prend en compte la zone du joueur : pour jouer de la musique correspondant à la zone du joueur. 
    Post-Condition : La fonction retourne 1 si il y a bien un changement de musique, sinon elle retourne 0. 
    """
    if music_playing == True and pygame.mixer.music.get_busy: #jouer de la musique
        mixer.music.load(f"assets/sounds/music/{current_player.zone}/grassy_plains-darren_curtis.mp3")
        mixer.music.play(-1)
        return 1
    return 0


def redrawWindow():
    """
    Cette fonction sert à faire les animations.
    Pré-Conditions : left et right sont des booléens indiquant la position du joueur (vers la droite ou vers la gauche)
    """

    fenetre.fill('black')
    fenetre.blit(bg, (0,0))
    fenetre.blit(fond_plaine_plateforme, (bgX, fond_plaine_plateforme_pos.y))

    pos = (current_player.rect.x, current_player.rect.y)

    anim_left = current_player.left
    anim_right = current_player.right
    anim_jump = current_player.isJump
    anim_lookup = current_player.isLookingUp

    if current_player.walkCount <= len(current_player.left_assets)-1: 
        if anim_left: #on utilise chaque élément du tableau left_assets
            fenetre.blit(
                current_player.left_assets[current_player.walkCount], 
                pos)
            current_player.walkCount +=1

        elif anim_right: #on utilise chaque élément du tableau right_assets
            fenetre.blit(
                current_player.right_assets[current_player.walkCount], 
                pos)
            current_player.walkCount += 1

        elif anim_jump:
            fenetre.blit(current_player.jumping, pos)

        elif anim_lookup:
            fenetre.blit(current_player.looking_up, pos)
        else:
            fenetre.blit(current_player.image, current_player.rect)
        
    else:
        current_player.walkCount = 0


def jeu(fps = 60):
    """
    Cette fonction est la fonction principale du jeu, elle contient la boucle qui le fait tourner. Elle prend en argument fps, qui sera habituellement à 60. 
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    jeu = True

    while jeu:

        current_player.controles()
        current_player.collisions()

        global bgX
        global bgX2
        if bgX <  bg.get_width() * -1:
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        redrawWindow() #animations
        
        pygame.display.flip() #rafraichissement de la fenêtre

        clock.tick(fps) #change les fps du jeu.
    pygame.quit()
if __name__ == "__main__":
    music()
    jeu()

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

