import pygame
from pygame import mixer
from random import randint
from level_update import Main, Plains, Desert, Mountains, Boss

pygame.init()
jeu = True
#chargement de la fenêtre
WIDTH = 1280
HEIGHT = 720
taille = (WIDTH, HEIGHT)
fenetre = pygame.display.set_mode(taille, pygame.RESIZABLE)   
pygame.display.set_caption("Juan Adventures") 
icon = pygame.image.load("assets/textures/player/player.png")
pygame.display.set_icon(icon) #on change l'icone de la fenêtre

clock = pygame.time.Clock() #on va pouvoir changer les fps

music_playing = False
sounds_playing = True

grass_steps = [mixer.Sound(f'assets/sounds/ambiant/grass-step-{i}.mp3') for i in range(1, 4)]
button = mixer.Sound("assets/sounds/GUI/button.mp3")

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
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = self.width
        self.rect.y = HEIGHT - 150 - self.size[1]
        self.y_default = HEIGHT - 150 - self.size[1]
        self.xoffset = self.rect.x
        self.yoffset = self.rect.y
        self.collisionp = False

        #? statistiques
        self.speed = 7
        self.vie = 100
        self.player_alive = True
        self.att = 1
        self.zone = 1 #? la zone du joueur
        self.subzone = 0

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
        if self.collisionp == True:
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
                    music()

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

    def test_collisions(self, plateforme_bas):
        """Cette méthode teste la collision entre le joueur et une plateforme du bas.
        Pré-Condition : plateforme_bas est une plateforlme"""

        if self.rect.left > plateforme_bas.right: #! si le joueur est trop à droite, il n'a pas de collision
            self.collisionp = False
            return False

        elif self.rect.left < plateforme_bas.left: #! si le joueur est trop à gauche, pas de collision.
            self.collisionp = False
            return False

        else:
            self.collisionp = True
            return True
 
    def collisions(self):
        """
        Cette méthode permet de gérer les collisions entre le joueur et l'environnement ou une plateforme. 
        """
        #! COLLISIONS ET GRAVITÉ
        collisions = main_levels_class.collisions
        indice_tab = self.rect.collidelist(collisions)
        
        if indice_tab != -1:
            self.collisionp = True
            self.test_collisions(collisions[indice_tab])
        else:
            self.rect.y += 2
            self.collisionp = False

        if self.subzone == 0 and self.rect.x <= 0:                                       #! Collisions d'à gauche
            self.rect = self.rect.move(10, 0)

        if self.rect.y > HEIGHT:
            print("Game OVER!")
            pygame.QUIT()

        if self.rect.x >= WIDTH + 0.5 * self.width:
            self.rect = self.rect.move(-(WIDTH + 0.5 * self.width), 0)
            self.subzone += 1

        elif self.subzone >= 1 and self.rect.x < 0:
            self.rect = self.rect.move((WIDTH + 0.5 * self.width), 0)
            self.subzone -= 1

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
            self.player_alive = False
current_player = Sprite_Player()
main_levels_class = Main(current_player, fenetre)

def music():
    """
    Cette fonction gère la musique du jeu. Elle prend en compte music_playing, un booléen représentant la volonté d'avoir de la musique dans le jeu et l'occupation
    de la "queue musicale". C'est-à-dire, que, si il y a déjà une musique en cours, on ne peut pas jouer de musique. 
    Elle prend en compte la zone du joueur : pour jouer de la musique correspondant à la zone du joueur. 
    Post-Condition : La fonction retourne 1 si il y a bien un changement de musique, sinon elle retourne 0. 
    """
    if music_playing == True and pygame.mixer.music.get_busy() == False and Game_Menu.menu_displaying == False: #jouer de la musique
        mixer.music.pause()
        mixer.music.unload()
        mixer.music.load(f"assets/sounds/music/{current_player.zone}/grassy_plains-darren_curtis.mp3")
        mixer.music.play(-1)
        return 1
    elif Game_Menu.menu_displaying == True and music_playing == True:
        mixer.music.load("assets/sounds/music/menu/mindfulness-relaxation-john-kensy.mp3")
        mixer.music.play(-1)
    return 0

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect


class Menu():
    """
    La Classe menu permet de faire la gestion des menus accessibles avec la touche "ÉCHAP".
    """
    def __init__(self):
        """
        Méthode d'initialisation de la classe menu.
        """
        self.selection = 0
        self.font_name = pygame.font.Font("assets/font/CreamyPeach.TTF", 30)
        self.menu_bg = pygame.image.load("assets/textures/background/menu.png").convert()
        self.cross = pygame.image.load("assets/textures/GUI/cross.png").convert_alpha()
        self.menu_displaying = False

    def main_menu(self):
        """
        Méthode qui gère le menu principal. 
        """
        if self.selection == 2:
            self.options()
        fenetre.blit(self.menu_bg, (0, 0))

        txt_r = draw_text("Menu principal", pygame.font.Font("assets/font/CreamyPeach.TTF", 50), "white", fenetre, WIDTH / 2, 100)
        txt_r2 = draw_text("Retour au jeu", self.font_name, "white", fenetre, WIDTH / 2, 200)
        txt_r3 = draw_text("Options", self.font_name, "white", fenetre, WIDTH / 2, 300)
        txt_r4 = draw_text("Quitter", self.font_name, "white", fenetre, WIDTH / 2, 400)    

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_displaying = False
                    mixer.music.stop()
                    music()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos_click = pygame.mouse.get_pos()
                    if pos_click[0] > 540 and pos_click[0] < 729:
                        pygame.mixer.Sound.stop(button)
                        if pos_click[1] >= 157 and pos_click[1] < 246:
                            self.selection = 1
                            self.sound_playing()

                        elif pos_click[1] >= 246 and pos_click[1] < 345:
                            self.selection = 2
                            self.sound_playing()

                        elif pos_click[1] >= 345 and pos_click[1] < 437:
                            self.selection = 3
                            self.sound_playing()

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if self.selection == 1:
            self.menu_displaying = False
            mixer.music.stop()
            music()
            self.selection = 0

        elif self.selection == 2:
            self.options()

        elif self.selection == 3:
            self.selection = 0
            pygame.quit()
            quit()

    def options(self):
        """
        options est la méthode qui gère le menu des options. 
        """
        global fenetre
        global HEIGHT
        global WIDTH
        global music_playing
        global sounds_playing
        fenetre.blit(self.menu_bg, (0, 0))
        txt_o = draw_text("Menu principal", pygame.font.Font("assets/font/CreamyPeach.TTF", 50), "white", fenetre, WIDTH / 2, 100)
        txt_o2 = draw_text(f"Résolution actuelle : {WIDTH, HEIGHT}", pygame.font.Font("assets/font/CreamyPeach.TTF", 23), "white", fenetre, WIDTH / 2, 200)
        txt_o2a = draw_text("480x720", pygame.font.Font("assets/font/CreamyPeach.TTF", 16), "gray", fenetre, WIDTH * 1/5, 225)
        txt_o2b = draw_text("720x1280", pygame.font.Font("assets/font/CreamyPeach.TTF", 16), "gray", fenetre, WIDTH * 2/5, 225)
        txt_o2c = draw_text("1080x1920", pygame.font.Font("assets/font/CreamyPeach.TTF", 16), "gray", fenetre, WIDTH * 3/5, 225)
        txt_o2d = draw_text("1440x2560", pygame.font.Font("assets/font/CreamyPeach.TTF", 16), "gray", fenetre, WIDTH * 4/5, 225)
        txt_o3 = draw_text("Plein écran", pygame.font.Font("assets/font/CreamyPeach.TTF", 16), "gray", fenetre, WIDTH / 2, 250)
        txt_o4 = draw_text("Musiques :", pygame.font.Font("assets/font/CreamyPeach.TTF", 23), "white", fenetre, WIDTH / 2, 300)
        txt_o4a = draw_text("OUI", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH * (3/5), 300)
        txt_o4b = draw_text("NON", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH * (4/5), 300)
        txt_o5 = draw_text("Sons :", pygame.font.Font("assets/font/CreamyPeach.TTF", 23), "white", fenetre, WIDTH / 2, 350)
        txt_o5a = draw_text("OUI", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH * (3/5), 350)
        txt_o5b = draw_text("NON", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH * (4/5), 350)
        txt_o6 = draw_text("Controles", pygame.font.Font("assets/font/CreamyPeach.TTF", 23), "white", fenetre, WIDTH /2, 400)
        txt_o6a = draw_text("Aller à droite : D / Flèche de droite ", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH /2, 425)
        txt_o6b = draw_text("Aller à gauche : Q / Flèche de gauche", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH /2, 450)
        txt_o6c = draw_text("Sauter : barre d'espace / Flèche du haut", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH /2, 475)
        txt_o6d = draw_text("Regarder en l'air : Z", pygame.font.Font("assets/font/CreamyPeach.TTF", 15), "gray", fenetre, WIDTH /2, 500)
        txt_o7 = draw_text("RETOUR", pygame.font.Font("assets/font/CreamyPeach.TTF", 25), "white", fenetre, WIDTH /2, 600)
        
        cross_rect = self.cross.get_rect()
        if music_playing == True:
            cross_rect = (txt_o4a.x, txt_o4a.y)
            fenetre.blit(self.cross, cross_rect)
        else:
            cross_rect = (txt_o4b.x, txt_o4b.y)
            fenetre.blit(self.cross, cross_rect)

        if sounds_playing == True:
            cross_rect = (txt_o5a.x, txt_o5a.y)
            fenetre.blit(self.cross, cross_rect)
        else:
            cross_rect = (txt_o5b.x, txt_o5b.y)
            fenetre.blit(self.cross, cross_rect)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selection = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos_click = pygame.mouse.get_pos()
                    pygame.mixer.Sound.stop(button)
                    if txt_o3.collidepoint(pos_click):
                        fenetre = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                        self.sound_playing()

                    elif txt_o2a.collidepoint(pos_click):
                        HEIGHT = 480
                        WIDTH = 720
                        fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
                        self.sound_playing()

                    elif txt_o2b.collidepoint(pos_click):
                        HEIGHT = 720
                        WIDTH = 1280
                        fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
                        self.sound_playing()

                    elif txt_o2c.collidepoint(pos_click):
                        HEIGHT = 1080
                        WIDTH = 1920
                        fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
                        self.sound_playing()

                    elif txt_o2d.collidepoint(pos_click):
                        HEIGHT = 1440
                        WIDTH = 2560
                        fenetre = pygame.display.set_mode((WIDTH, HEIGHT))
                        self.sound_playing()

                    elif txt_o4a.collidepoint(pos_click):
                        music_playing = True
                        mixer.music.stop()
                        music()
                        self.sound_playing()

                    elif txt_o4b.collidepoint(pos_click):
                        music_playing = False
                        mixer.music.stop()
                        music()
                        self.sound_playing()

                    elif txt_o5a.collidepoint(pos_click):
                        sounds_playing = True
                        self.sound_playing()

                    elif txt_o5b.collidepoint(pos_click):
                        sounds_playing = False
                        self.sound_playing()

                    elif txt_o7.collidepoint(pos_click):
                        self.selection = 0
                        self.sound_playing()
    
    def sound_playing(self):
        """
        Petite méthode qui permet de jouer le son du clique de bouton si le son est activé. 
        """
        global sounds_playing
        if sounds_playing:
            button.play()

Game_Menu = Menu()




def jeu(fps = 60):
    """
    Cette fonction est la fonction principale du jeu, elle contient la boucle qui le fait tourner. Elle prend en argument fps, qui sera habituellement à 60. 
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    while jeu:
        if Game_Menu.menu_displaying == False:
            #! si on n'est pas dans le menu, il y a le jeu qui s'affiche. 
            main_levels_class.choose(current_player)
            current_player.controles() #update controles
            current_player.collisions() #update collisions


        else:
            #! si on est dans le menu, on l'affiche
            Game_Menu.main_menu()

        pygame.display.flip() #rafraichissement de la fenêtre

        clock.tick(fps) #change les fps du jeu.
    
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

