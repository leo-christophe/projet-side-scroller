import pygame
from pygame import mixer
from random import randint
from level_update import Main, Game_Parameters

pygame.init()

"""
Ce jeu a été crée par Léo.C lors d'un projet de Terminale. Il n'est pas totalement terminé puisqu'il n'a pas atteint les ambitions souhaitées mais il est assez avancé pour
donner un aperçu de ce qui aurait été fait pour le reste. Un menu est à disposition en appuyant sur "Echap", vous trouverez les différents contrôles ainsi que différents
paramètres que vous pourrez changer tel que les fps, la résolution, le son ou la musique (qui est désactivée par défault.). 
Note : Les changements de résolution ne sont pas efficaces du tout, pareil pour les changements de fps qui peuvent modifier la qualité de jeu. 

Juan Adventure 2022 ©
"""

class Sounds():
    """
    Cette classe permet de gérer les sons.
    """
    def __init__(self):
        """
        Méthode d'initialisation de la classe Sounds qui repertorie les sons, et les paramètres correspondant aux sons.
        """
        self.music_playing = False
        self.sounds_playing = True
        self.grass_steps = [mixer.Sound(f'assets/sounds/ambiant/grass-step-{i}.mp3') for i in range(1, 4)]
        self.button = mixer.Sound("assets/sounds/GUI/button.mp3")
        self.game_over = mixer.Sound("assets/sounds/music/menu/game_over.mp3")
        

    def music(self):
        """
        Cette méthode gère la musique du jeu. Elle prend en compte music_playing, un booléen représentant la volonté d'avoir de la musique dans le jeu et l'occupation
        de la "queue musicale". C'est-à-dire, que, si il y a déjà une musique en cours, on ne peut pas jouer de musique. 
        Elle prend en compte la zone du joueur : pour jouer de la musique correspondant à la zone du joueur. 
        Post-Condition : La fonction retourne 1 si il y a bien un changement de musique, sinon elle retourne 0. 
        """
        music_playing = self.music_playing
        #? Jouer la musique de jeu principale
        if music_playing == True and pygame.mixer.music.get_busy() == False and Game_Menu.menu_displaying == False: 
            mixer.music.pause()
            mixer.music.unload()
            mixer.music.load(f"assets/sounds/music/{current_player.zone}/grassy_plains-darren_curtis.mp3")
            mixer.music.play(-1)
            return 1
        #? Jouer la musique du menu
        elif Game_Menu.menu_displaying == True and music_playing == True:
            mixer.music.load("assets/sounds/music/menu/mindfulness-relaxation-john-kensy.mp3")
            mixer.music.play(-1)
            return 1
        return 0

    def play_sound_list(self, sounds = "grass", index = 0, volume = 0.25):
        """
        Joue le son d'un tableau. 
        Pré-Conditions : sounds est une chaine de caractères indiquant le son à jouer, index l'indice du tableau à choisir, volume est un float : le volume du son qui va être joué.
        """
        sounds_playing = self.sounds_playing
        if sounds_playing == True:
            if sounds == "grass":
                son = self.grass_steps[randint(0,2)]
            son.set_volume(volume)
            son.play()
    
    def play_sound(self, sound, volume = 0.25):
        """ Joue un son unique."""
        sounds_playing = self.sounds_playing
        if sounds_playing == True:
            sound.set_volume(volume)
            sound.play()        
Game_Sounds = Sounds()

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

        ################################
        #    CHARGEMENT DES IMAGES     #
        ################################
        self.image = pygame.image.load("assets/textures/player/player.png")
        self.jumping = pygame.image.load("assets/textures/player/player_jumping.png")
        self.looking_up = pygame.image.load("assets/textures/player/player_looking_up.png")
        self.right_assets = [pygame.image.load(f'assets/textures/player/player_right_{x}.png') for x in range(1, 19)]
        self.left_assets = [pygame.image.load(f'assets/textures/player/player_left_{x}.png') for x in range(1, 19)]
        self.jumping_left = pygame.image.load("assets/textures/player/player_jumping_left_1.png")
        self.jumping_right = pygame.image.load("assets/textures/player/player_jumping_right_1.png")

        ##################
        #    ACTIONS     #
        ##################    
        self.left, self.right, self.isJump, self.isLookingUp  = False, False, False, False
        self.walkCount = 0

        ##################################################
        #    CARACTERISTIQUES DE L'IMAGE/ COLLISIONS     #
        ##################################################
        self.vely = 10
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = self.width
        self.rect.y = Game_Parameters.height - 150 - self.size[1]
        self.y_default = Game_Parameters.height - 150 - self.size[1]
        self.fps = Game_Parameters.fps
        self.width, self.height = Game_Parameters.width, Game_Parameters.height
        self.collisionp = False
        self.action = False

        ##############################
        #        STATISTIQUES        #
        ##############################
        self.speed = 5
        self.vie = 100
        self.att = 1
        self.zone = 1 #? la zone du joueur
        self.subzone = 0
        self.player_alive, self.gameover = True, False

    def goRight(self, marge = marge_x):
        """
        La méthode goRight permet de déplacer le joueur de marge pixels vers la droite. 
        Pré-Condition : La méthode goRight prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        #? Prévisualisation du joueur : où il va se trouver après le mouvement
        right_move = marge * self.speed + (60 / self.fps)
        if self.isJump == True:
            rect2 = pygame.Rect((self.rect.x + right_move, self.rect.y - self.vely * (2 + self.fps/60)), (self.rect.w, self.rect.h))
        else:
            rect2 = pygame.Rect((self.rect.x + right_move, self.rect.y), (self.rect.w, self.rect.h))
        collisions = main_levels_class.collisions
        indice_tab = rect2.collidelist(collisions)
        element_collision = collisions[indice_tab]

        #? Le mouvement
        if rect2.colliderect(element_collision) and self.rect.right >= rect2.left:
            self.rect.right = element_collision.left - 1
        else:
            self.rect.right += right_move
        Game_Sounds.play_sound_list(sounds = "grass", index = randint(0, 2))
        return self.rect

    def goLeft(self, marge = marge_x):
        """
        La méthode goLeft permet de déplacer le joueur de marge pixels vers la gauche. 
        Pré-Condition : La méthode goLeft prend en argument marge.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        #? Prévisualisation du joueur : où il va se trouver après le mouvement
        left_move = marge * self.speed + (60/self.fps)
        if self.isJump == True:
            rect2 = pygame.Rect((self.rect.x - left_move, self.rect.y - self.vely * (2 + self.fps/60)), (self.rect.w, self.rect.h))
        else:
            rect2 = pygame.Rect((self.rect.x - left_move, self.rect.y), (self.rect.w, self.rect.h))
        collisions = main_levels_class.collisions
        indice_tab = rect2.collidelist(collisions)
        element_collision = collisions[indice_tab]

        #? Le mouvement
        if rect2.colliderect(element_collision) and rect2.left <= element_collision.right:
            self.rect.left = element_collision.right - 1
        else:
            self.rect.left -= left_move
        Game_Sounds.play_sound_list(sounds = "grass", index = randint(0, 2))
        return self.rect

    def goJump(self):
        """
        La méthode goJump permet de faire sauter le joueur de jump pixels. 
        Pré-Condition : Elle prend en argument jump, qui sera pratiquemment tout le temps à 150.
        left permet de faire sauter le joueur vers la gauche et right permet de faire sauter le joueur vers la droite.
        Post-Condition : Elle retourne self.rect, la position du joueur. 
        """
        #? S'il y a collision, donc s'il est en position de sauter : 
        if self.collisionp == True:
            if self.vely < -10:
                self.vely = 10
            self.isJump = True
            Game_Sounds.play_sound(mixer.Sound(f'assets/sounds/ambiant/grass_jump.mp3'))
        return self.rect

    def check_jump(self):
        """
        check_jump est la méthode qui permet de "faire" le saut du joueur. Prenant en compte sa vélocité, elle permet de calculer ses déplacements en hauteur.
        """
        collisions = main_levels_class.collisions

        if self.isJump == True: 
            self.rect.y -= self.vely * (2 + self.fps/60)
            self.vely -= 1
            # Réinitialisation de la velocité
            if self.vely < - 10:
                self.isJump = False
                self.vely = 10
        else:
            self.collisionp = True
            rect_j = pygame.Rect((self.rect.x, self.rect.bottom + 10), (self.rect.w, self.rect.h))
            coll = rect_j.collidelist(collisions)
            #? s'il n y a collision, on calcul le "trajet" à faire pour atterir.
            if coll != -1: 
                self.rect.bottom += (collisions[coll].top - self.rect.bottom)
            else:
                self.rect.bottom += 10

    def controles(self):
        """
        La méthode controles permet de vérifier si un bouton est appuyé : si le joueur appuie sur echap : il affiche un menu, s'il appuie sur la flèche de gauche,
        il va à gauche...
        Cette méthode est répétée dans la boucle principale du jeu pour vérifier à chaque tour de boucle. 
        """
        ############################################
        # TOUCHE NE RESTE PAS APPUYÉE / EVENEMENTS #
        ############################################
        for event in pygame.event.get(): 
            #? pour quitter
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            #? Pour sauter
            elif event.type == pygame.KEYDOWN: 
                if (event.key == pygame.K_UP) or (event.key == pygame.K_SPACE):
                    self.walkCount = 0
                    self.goJump()

                #? Pour aller dans le menu : echap
                elif event.key == pygame.K_ESCAPE:
                    Game_Menu.menu_displaying = True
                    Game_Sounds.music()

                else:
                    self.walkCount = 0
            #? Si l'on minimise la fenêtre, le jeu se met en pause.
            elif event.type == pygame.WINDOWMINIMIZED:
                Game_Menu.menu_displaying = True
                Game_Sounds.music()

            elif event.type == pygame.KEYUP:
                if (event.key == pygame.K_e):
                    self.action = False
        ##############################
        #    TOUCHE RESTE APPUYÉE    #
        ##############################
        keys = pygame.key.get_pressed()
        #? pour aller à gauche
        if keys[pygame.K_LEFT] or keys[pygame.K_q]: 
            self.left, self.right, self.isLookingUp = True, False, False

            self.goLeft(Sprite_Player.marge_x)

        #? pour aller à droite
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
            self.left, self.right, self.isLookingUp = False, True, False

            self.goRight(Sprite_Player.marge_x)

        #? pour regarder en haut
        elif keys[pygame.K_z]: 
            self.left, self.right, self.isLookingUp = False, False, True

        else:
            self.isLookingUp = False
            self.walkCount = 0
        
        if keys[pygame.K_e]:
            self.action = True

    def update(self):
        """
        Cette méthode est exécutée dans la boucle à chaque fois si le joueur n'est pas dans un menu. Elle contient tout les éléments qui ont besoin d'être
        appelé régulièrement.
        """
        ##############################
        #        COLLISIONS          #
        ##############################
        collisions = main_levels_class.collisions
        indice_tab = self.rect.collidelist(collisions)
        element_collision = collisions[indice_tab]

        #? Collisions avec plateformes
        if self.rect.colliderect(collisions[indice_tab]):          

            #si le joueur n'est pas en capacité d'atterir sur la plateforme et qu'il y a collision.
            if self.rect.bottom >= element_collision.top: 
                if  self.rect.left >= element_collision.right:
                    self.rect.left = element_collision.right + 2
                    
                elif self.rect.right <= element_collision.left:
                    self.rect.right = element_collision.left - 2

                #Il n'y a pas collision si le joueur ne peut pas atterir : il tombe.
                self.isJump = False
                self.collisionp = False    
            else:
                #S'il est en capacité d'atterir, le bas du joueur est égal au haut de la plateforme.
                self.rect.bottom = element_collision.top + 1
                self.collisionp = True

        #? on verifie si il y a saut du joueur
        self.check_jump()

        #? Afficher l'écran de Gamer Over
        if (self.rect.bottom > Game_Parameters.height and not(self.gameover)) or (self.player_alive == False or self.vie <= 0):
            self.gameover = True
            self.player_alive = False
            self.collisionp = False
            return Game_Menu.game_over()

        #? si le joueur atteint la limite tout à gauche (du début)
        if self.subzone == 0: 
            if self.rect.x <= 0:
                self.rect = self.rect.move(10, 0)

        ##############################
        # CHANGEMENT DE ZONE / SUB   #
        ##############################
        #? changement de zone vers la droite
        if self.rect.centerx >= Game_Parameters.width:
            self.rect.center = (0, self.rect.y)
            self.subzone += 1
        
        #? changement de zone vers la gauche
        elif self.subzone >= 1 and self.rect.centerx <= 0:
            self.rect.center = (Game_Parameters.width, self.rect.y) 
            self.subzone -= 1

        ##############################
        # DEGATS MONSTRES - JOUEUR   #
        ##############################

        if self.rect.collidelist(main_levels_class.ennemies) != -1:
            ennemie = main_levels_class.ennemies[self.rect.collidelist(main_levels_class.ennemies)]
            if ennemie.dmg != 0:
                self.degat(ennemie.dmg)

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
        return self.vie
current_player = Sprite_Player()



def draw_text(text, font, color, surface, x, y):
    """
    Cette fonction permet de dessiner un texte.
    Pré-Conditions : text est une chaine de caractères représentant le texte à afficher.
    font est une chaine de caractères représentant le chemin à emprunter pour trouver le fichier de la police (en TTF).
    color est la couleur du texte
    surface correspond à la surface sur laquelle le texte va être dessiner
    x représente l'axe des abscisses et y l'axe des ordonnées. 
    Post-Condition : le rect du texte est renvoyé, textrect. 
    """
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

class GUI():
    """
    La Classe GUI permet de faire la gestion des GUIS, ce qui apparaît dans l'écran du joueur lorsqu'il est en jeu. Elle est très courte car c'était prévu d'y
    rajouter des choses. 
    """
    def displaying_gui(self):
        """
        Cette méthode permet d'afficher le GUI dans le jeu, en continu : un texte en haut à gauche de l'écran indiquant la vie du joueur. 
        """
        draw_text(f"Vie : {current_player.vie}/100", pygame.font.Font("assets/font/CreamyPeach.TTF", 20), "black", Game_Parameters.fenetre, 80, 20)
Game_GUI = GUI()

class Menu():
    """
    La Classe menu permet de faire la gestion des menus accessibles avec la touche "ÉCHAP".
    """
    def __init__(self):
        """
        Méthode d'initialisation de la classe menu.
        """
        self.selection = 0
        self.font_str = "assets/font/CreamyPeach.TTF"
        self.font_name = pygame.font.Font("assets/font/CreamyPeach.TTF", 30)
        self.menu_bg = pygame.image.load("assets/textures/background/menu.png").convert()
        self.cross = pygame.image.load("assets/textures/GUI/cross.png").convert_alpha()
        self.menu_displaying = False

    def game_over(self):
        """
        Méthode qui permet d'afficher l'écran de Gamer Over lorsque le joueur meurt. 
        Elle retourne -1 dès que le joueur quitte. 
        """
        if Game_Sounds.sounds_playing == True:
            Game_Sounds.game_over.set_volume(0.2)
            Game_Sounds.game_over.play()

        gameover = True
        while gameover == True:
            Game_Parameters.fenetre.fill('black')
            draw_text("GAME   OVER", pygame.font.Font("assets/font/GhostOfTheWildWest.TTF", 60), "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 100)
            draw_text("Bougez la souris pour quitter le jeu", pygame.font.Font("assets/font/GhostOfTheWildWest.TTF", 30), "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 250)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pygame.quit()
                    gameover = False
                    return -1
            pygame.display.flip()

    def temporary_end(self):
        """
        La méthode temporary_end permet d'afficher la fin "temporaire" du jeu, c'est-à-dire, la fin du jeu à ce stade. 
        Elle retourne -1 lorsque le joueur choisi de quitter. 
        """
        temp = True
        while temp == True:
            Game_Parameters.fenetre.fill('black')

            draw_text(
                "FIN DU JEU", 
                pygame.font.Font("assets/font/GhostOfTheWildWest.TTF", 60), 
                "white", 
                Game_Parameters.fenetre, 
                Game_Parameters.width / 2, 
                100
                )

            draw_text(
                "Bougez la souris pour quitter le jeu", 
                pygame.font.Font("assets/font/GhostOfTheWildWest.TTF", 30), 
                "white", 
                Game_Parameters.fenetre, 
                Game_Parameters.width / 2, 
                300
                )

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    pygame.quit()
                    temp = False
                    return -1

            pygame.display.flip()

    def main_menu(self):
        """
        Méthode qui gère le menu principal. 
        """
        if self.selection == 2:
            self.options()
        Game_Parameters.fenetre.blit(self.menu_bg, (0, 0))

        draw_text("Menu principal", pygame.font.Font("assets/font/CreamyPeach.TTF", 50), "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 100)
        txt_r2 = draw_text("Retour au jeu", self.font_name, "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 200)
        txt_r3 = draw_text("Options", self.font_name, "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 300)
        txt_r4 = draw_text("Quitter", self.font_name, "white", Game_Parameters.fenetre, Game_Parameters.width / 2, 400)    

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.menu_displaying = False
                    mixer.music.stop()
                    Game_Sounds.music()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos_click = pygame.mouse.get_pos()
                    pygame.mixer.Sound.stop(Game_Sounds.button)
                    if txt_r2.collidepoint(pos_click):
                        self.selection = 1
                        self.sound_playing()

                    elif txt_r3.collidepoint(pos_click):
                        self.selection = 2
                        self.sound_playing()

                    elif txt_r4.collidepoint(pos_click):
                        self.selection = 3
                        self.sound_playing()

            elif event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if self.selection == 1:
            self.menu_displaying = False
            mixer.music.stop()
            Game_Sounds.music()
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
        music_playing = Game_Sounds.music_playing
        sounds_playing = Game_Sounds.sounds_playing

        fenetre = Game_Parameters.fenetre
        fps = Game_Parameters.fps
        height = Game_Parameters.height

        fenetre.blit(self.menu_bg, (0, 0))
        draw_text("Menu principal", pygame.font.Font(self.font_str, 50), "white", fenetre, Game_Parameters.width / 2, 0.1 * height)

        draw_text(f"Résolution actuelle : {Game_Parameters.height, Game_Parameters.width}", pygame.font.Font(self.font_str, 23), "white", fenetre, Game_Parameters.width / 2, 0.2 * height)
        txt_o2a = draw_text("480x720", pygame.font.Font(self.font_str, 16), "gray", fenetre, Game_Parameters.width * 1/5, 0.25 * height)
        txt_o2b = draw_text("720x1280", pygame.font.Font(self.font_str, 16), "gray", fenetre, Game_Parameters.width * 2/5, 0.25 * height)
        txt_o2c = draw_text("1080x1920", pygame.font.Font(self.font_str, 16), "gray", fenetre, Game_Parameters.width * 3/5, 0.25 * height)
        txt_o2d = draw_text("1440x2560", pygame.font.Font(self.font_str, 16), "gray", fenetre, Game_Parameters.width * 4/5, 0.25 * height)
        txt_o3 = draw_text("Plein écran", pygame.font.Font(self.font_str, 16), "gray", fenetre, Game_Parameters.width / 2, 0.3 * height)

        draw_text(f"FPS / IPS actuel : {fps}", pygame.font.Font(self.font_str, 23), "white", fenetre, Game_Parameters.width * 0.5, 0.37 * height)
        txt_v3a = draw_text("15", pygame.font.Font(self.font_str, 20), "gray", fenetre, Game_Parameters.width * (2/10), 0.4 * height)
        txt_v3b = draw_text("30", pygame.font.Font(self.font_str, 20), "gray", fenetre, Game_Parameters.width * (4/10), 0.4 * height)
        txt_v3c = draw_text("45", pygame.font.Font(self.font_str, 20), "gray", fenetre, Game_Parameters.width * (5/10), 0.4 * height)
        txt_v3d = draw_text("60", pygame.font.Font(self.font_str, 20), "gray", fenetre, Game_Parameters.width * (6/10), 0.4 * height)
        txt_v3e = draw_text("144", pygame.font.Font(self.font_str, 20), "gray", fenetre, Game_Parameters.width * (8/10), 0.4 * height)

        draw_text("Musiques :", pygame.font.Font(self.font_str, 23), "white", fenetre, Game_Parameters.width / 2, 0.5 * height)
        txt_o4a = draw_text("OUI", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width * (3/5), 0.5 * height)
        txt_o4b = draw_text("NON", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width * (4/5), 0.5 * height)

        draw_text("Sons :", pygame.font.Font(self.font_str, 23), "white", fenetre, Game_Parameters.width / 2, 0.55 * height)
        txt_o5a = draw_text("OUI", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width * (3/5), 0.55 * height)
        txt_o5b = draw_text("NON", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width * (4/5), 0.55 * height)

        draw_text("Controles", pygame.font.Font(self.font_str, 23), "white", fenetre, Game_Parameters.width /2, 0.65 * height)
        draw_text("Aller à droite : D / Flèche de droite ", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width /2, 0.68 * height)
        draw_text("Aller à gauche : Q / Flèche de gauche", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width /2, 0.71 * height)
        draw_text("Sauter : barre d'espace / Flèche du haut", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width /2, 0.74 * height)
        draw_text("Regarder en l'air : Z", pygame.font.Font(self.font_str, 15), "gray", fenetre, Game_Parameters.width /2, 0.77 * height)

        txt_o7 = draw_text("RETOUR", pygame.font.Font(self.font_str, 25), "white", fenetre, Game_Parameters.width /2, 0.83 * height)
        
        cross_rect = self.cross.get_rect()
        ##############################
        # PLACER LA CROIX POUR MUSIC #
        ##############################
        if music_playing == True:
            cross_rect.x, cross_rect.y  = txt_o4a.x, txt_o4a.y
            cross_rect.left = cross_rect.right + 5
        else:
            cross_rect.x, cross_rect.y = txt_o4b.x, txt_o4b.y
            cross_rect.left = cross_rect.right + 5
        Game_Parameters.fenetre.blit(self.cross, cross_rect) 

        ##############################
        # PLACER LA CROIX POUR SOUNDS#
        ##############################
        if sounds_playing == True:
            cross_rect.x, cross_rect.y = txt_o5a.x, txt_o5a.y
            cross_rect.left = cross_rect.right + 5
        else:
            cross_rect.x, cross_rect.y = txt_o5b.x, txt_o5b.y
            cross_rect.left = cross_rect.right + 5
        Game_Parameters.fenetre.blit(self.cross, cross_rect) 

        ##############################
        #  PLACER LA CROIX POUR FPS  #
        ##############################
        if fps == 15:
            cross_rect.x, cross_rect.y = txt_v3a.x, txt_v3a.y
            cross_rect.left = cross_rect.right + 5

        elif fps == 30:
            cross_rect.x, cross_rect.y = txt_v3b.x, txt_v3b.y
            cross_rect.left = cross_rect.right + 5
            
        elif fps == 45:
            cross_rect.x, cross_rect.y = txt_v3c.x, txt_v3c.y
            cross_rect.left = cross_rect.right + 5

        elif fps == 60:
            cross_rect.x, cross_rect.y = txt_v3d.x, txt_v3d.y
            cross_rect.left = cross_rect.right + 5
 
        elif fps == 144:
            cross_rect.x, cross_rect.y = txt_v3e.x, txt_v3e.y
            cross_rect.left = cross_rect.right + 5
        Game_Parameters.fenetre.blit(self.cross, cross_rect) 

        #####################################
        #  PLACER LA CROIX POUR RESOLUTION  #
        #####################################
        if height == 480:
            cross_rect.x, cross_rect.y = txt_o2a.x, txt_o2a.y
            cross_rect.left = cross_rect.right + 5

        elif height == 720:
            cross_rect.x, cross_rect.y = txt_o2b.x, txt_o2b.y
            cross_rect.left = cross_rect.right + 5

        elif height == 1080:
            cross_rect.x, cross_rect.y = txt_o2c.x, txt_o2c.y
            cross_rect.left = cross_rect.right + 5

        elif height == 1440:
            cross_rect.x, cross_rect.y = txt_o2d.x, txt_o2d.y
            cross_rect.left = cross_rect.right + 5
        Game_Parameters.fenetre.blit(self.cross, cross_rect) 
        main_levels_class.Plains_Levels.bg = pygame.transform.scale(main_levels_class.Plains_Levels.bg, (Game_Parameters.width, Game_Parameters.height))

        #####################################
        #  ACTIONS POUR CLIQUE DE SOURIS    #
        #####################################
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selection = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_presses = pygame.mouse.get_pressed()
                if mouse_presses[0]:
                    pos_click = pygame.mouse.get_pos()
                    pygame.mixer.Sound.stop(Game_Sounds.button)
                    ############################
                    # CHANGEMENT DE RESOLUTION #
                    ############################
                    if txt_o3.collidepoint(pos_click):
                        Game_Parameters.fenetre = pygame.display.set_mode((Game_Parameters.width, Game_Parameters.height), pygame.FULLSCREEN)
                        self.sound_playing()

                    elif txt_o2a.collidepoint(pos_click):
                        Game_Parameters.height, Game_Parameters.width = 480, 720
                        Game_Parameters.fenetre = pygame.display.set_mode((Game_Parameters.width, Game_Parameters.height))
                        self.sound_playing()

                    elif txt_o2b.collidepoint(pos_click):
                        Game_Parameters.height, Game_Parameters.width = 720, 1280
                        Game_Parameters.fenetre = pygame.display.set_mode((Game_Parameters.width, Game_Parameters.height))
                        self.sound_playing()

                    elif txt_o2c.collidepoint(pos_click):
                        Game_Parameters.height, Game_Parameters.width = 1080, 1920
                        Game_Parameters.fenetre = pygame.display.set_mode((Game_Parameters.width, Game_Parameters.height))
                        self.sound_playing()

                    elif txt_o2d.collidepoint(pos_click):
                        Game_Parameters.height, Game_Parameters.width = 1440, 2560
                        Game_Parameters.fenetre = pygame.display.set_mode((Game_Parameters.width, Game_Parameters.height))
                        self.sound_playing()

                    #####################
                    # CHANGEMENT DE FPS #
                    #####################
                    elif txt_v3a.collidepoint(pos_click):
                        Game_Parameters.fps = 15
                        self.sound_playing()
                        
                    elif txt_v3b.collidepoint(pos_click):
                        Game_Parameters.fps = 30
                        self.sound_playing()

                    elif txt_v3c.collidepoint(pos_click):
                        Game_Parameters.fps = 45
                        self.sound_playing()

                    elif txt_v3d.collidepoint(pos_click):
                        Game_Parameters.fps = 60
                        self.sound_playing()   

                    elif txt_v3e.collidepoint(pos_click):
                        Game_Parameters.fps = 144
                        self.sound_playing()

                    #####################
                    # ACTIVATION MUSIC  #
                    #####################
                    elif txt_o4a.collidepoint(pos_click):
                        Game_Sounds.music_playing = True
                        mixer.music.stop()
                        Game_Sounds.music()
                        self.sound_playing()

                    elif txt_o4b.collidepoint(pos_click):
                        Game_Sounds.music_playing = False
                        mixer.music.stop()
                        Game_Sounds.music()
                        self.sound_playing()

                    #####################
                    # ACTIVATION SONS   #
                    #####################
                    elif txt_o5a.collidepoint(pos_click):
                        Game_Sounds.sounds_playing = True
                        self.sound_playing()

                    elif txt_o5b.collidepoint(pos_click):
                        Game_Sounds.sounds_playing = False
                        self.sound_playing()

                    # RETOUR 
                    elif txt_o7.collidepoint(pos_click):
                        self.selection = 0
                        self.sound_playing()
    
    def sound_playing(self):
        """
        Petite méthode qui permet de jouer le son du clique de bouton si le son est activé. 
        """
        sounds_playing = Game_Sounds.sounds_playing
        if sounds_playing:
            Game_Sounds.button.play()

Game_Menu = Menu()
main_levels_class = Main(current_player, Game_Parameters.fenetre, Game_Menu)
def jeu():
    """
    Cette fonction est la fonction principale du jeu, elle contient la boucle qui le fait tourner. Elle prend en argument fps, qui sera habituellement à 60. 
    Cette boucle infinie sert à faire marcher le jeu en continu. Tant que ALT-F4 ou que la fenêtre n'est pas fermée, le jeu continuera de marcher dès l'exécution du programme.
    """
    isGameActive = Game_Parameters.isGameActive
    while isGameActive:
        if Game_Menu.menu_displaying == False:
            #? si on n'est pas dans le menu, il y a le jeu qui s'affiche. 
            main_levels_class.choose(current_player)
            #update controles
            current_player.controles() 
            #update collisions
            current_player.update() 
            Game_GUI.displaying_gui()

        else:
            #? si on est dans le menu, on l'affiche
            Game_Menu.main_menu()
        #rafraichissement de la fenêtre
        pygame.display.flip() 

        #change les fps du jeu.
        Game_Parameters.clock.tick(Game_Parameters.fps) 
    
if __name__ == "__main__":
    Game_Sounds.music()
    jeu()
