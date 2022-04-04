import pygame
def redrawWindow(fenetre, current_player):
    """
    Cette fonction sert à faire les animations.
    Pré-Conditions : left et right sont des booléens indiquant la position du joueur (vers la droite ou vers la gauche)
    """

    pos = (current_player.rect.x, current_player.rect.y)

    anim_left = current_player.left
    anim_right = current_player.right
    anim_jump = current_player.isJump
    anim_lookup = current_player.isLookingUp

    if current_player.walkCount <= len(current_player.left_assets)-1: 

        if anim_left: #on utilise chaque élément du tableau left_assets
            if anim_jump == True:
                fenetre.blit(
                    current_player.jumping_left, 
                    pos)
            else:                
                fenetre.blit(
                    current_player.left_assets[current_player.walkCount], 
                    pos)
                current_player.walkCount +=1

        elif anim_right: #on utilise chaque élément du tableau right_assets
            if anim_jump == True:
                fenetre.blit(
                    current_player.jumping_right, 
                    pos)
            else:
                fenetre.blit(
                    current_player.right_assets[current_player.walkCount], 
                    pos)
                current_player.walkCount += 1

        elif anim_jump:
            fenetre.blit(current_player.jumping, pos)
        
        elif current_player.isfalling:
            fenetre.blit(current_player.jumping, pos)

        elif anim_lookup:
            fenetre.blit(current_player.looking_up, pos)

        else:
            fenetre.blit(current_player.image, current_player.rect)
        
    else:
        current_player.walkCount = 0

class Parameters():
    """
    Parameters est la classe qui repertorie tout les paramètres générals du jeu. 
    """
    def __init__(self):
        self.HEIGHT = 720
        self.WIDTH = 1280
        self.fps = 60
        self.fenetre = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE)   
        self.caption = pygame.display.set_caption("Juan Adventures") 
        self.icon = pygame.display.set_icon(pygame.image.load("assets/textures/GUI/icon.png")) #on change l'icone de la fenêtre
        self.clock = pygame.time.Clock() 
        self.isGameActive = True
Game_Parameters = Parameters() #On créer Game_Parameters qui va nous servir pour récupérer et modifier ces paramètres. 


class platform_creation():
    """
    Cette classe permet de créer des plateformes plus efficacement.
    """
    def __init__(self, sprite, x = 0, y = 0):
        """
        Initialisation d'une plateforme avec : sprite : une image, x : la coordonnée en x, y : la coordonnée en y. 
        """
        self.rect = sprite.get_rect()
        self.rect.x = x
        self.rect.y = y

class Plains():
    """
    Cette classe permet de gérer toutes les subzones de la zone "Plaines". 
    """
    def __init__(self, subzone, fenetre, current_player):
        self.bg = pygame.image.load("assets/textures/background/fond_plaines_2.png").convert()
        self.dirt_platform = pygame.image.load("assets/textures/props/dirt_platform.png")
        self.dirt_wall = pygame.image.load("assets/textures/props/dirt_wall.png")
        self.light_platform = pygame.image.load("assets/textures/props/light_dirt_platform.png")

        self.fenetre = fenetre
        self.player = current_player
        self.subzone = subzone
        self.last_zone = 8

        self.plat1 = platform_creation(self.dirt_platform, 0, Game_Parameters.HEIGHT - self.dirt_platform.get_height())
        self.plat2 = platform_creation(self.dirt_platform, self.plat1.rect.width + 80, Game_Parameters.HEIGHT - self.dirt_platform.get_height())
        self.light_plat = platform_creation(self.light_platform, 100, Game_Parameters.HEIGHT - self.dirt_platform.get_height() - 80)
        self.light_plat2 = platform_creation(self.light_platform, 150, Game_Parameters.HEIGHT - self.dirt_platform.get_height() - 100)

        #On créer une liste de collisions
        self.collisions_list_plains = [
        [self.plat1.rect, self.plat2.rect, self.light_plat.rect, self.light_plat2.rect],
        [self.plat1.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect]
        ]

        self.collisions = self.collisions_list_plains[0]

    def window_refreshing(self, fenetre):
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)


    def subzone_0(self):
        self.collisions = self.collisions_list_plains[0]
        fenetre = self.fenetre
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   
        fenetre.blit(self.light_platform, (self.light_plat.rect.x, self.light_plat.rect.y))   
        fenetre.blit(self.light_platform, (self.light_plat2.rect.x, self.light_plat2.rect.y))   

        
    def subzone_1(self):
        print(self.collisions)
        self.collisions = self.collisions_list_plains[1]
        fenetre = self.fenetre
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   

    def subzone_2(self):
        self.collisions = self.collisions_list_plains[2]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   

    def subzone_3(self):
        self.collisions = self.collisions_list_plains[3]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.plat1.rect)

    def subzone_4(self):
        self.collisions = self.collisions_list_plains[4]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.fond_plaine_plateforme_pos)

    def subzone_5(self):
        self.collisions = self.collisions_list_plains[5]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.fond_plaine_plateforme_pos)

    def subzone_6(self):
        self.collisions = self.collisions_list_plains[6]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.fond_plaine_plateforme_pos)

    def subzone_7(self):
        self.collisions = self.collisions_list_plains[7]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.fond_plaine_plateforme_pos)

    def subzone_8(self):
        self.collisions = self.collisions_list_plains[8]
        fenetre = self.fenetre
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)
        fenetre.blit(self.fond_plaine_plateforme, self.fond_plaine_plateforme_pos)

class Mountains():
    """
    Cette classe permet de gérer toutes les subzones de la zone "Montagnes". 
    """
    def __init__(self, subzone, fenetre, current_player):
        self.zone = 2
        self.collisions = []

    def subzone_1(self):
        pass
    def subzone_2(self):
        pass
    def subzone_3(self):
        pass
    def subzone_4(self):
        pass
    def subzone_5(self):
        pass
    def subzone_6(self):
        pass
    def subzone_7(self):
        pass
    def subzone_8(self):
        pass

class Desert():
    """
    Cette classe permet de gérer toutes les subzones de la zone "Desert". 
    """
    def __init__(self, subzone, fenetre, current_player):
        self.zone = 3
        self.collisions = []
    def subzone_1(self):
        pass
    def subzone_2(self):
        pass
    def subzone_3(self):
        pass
    def subzone_4(self):
        pass
    def subzone_5(self):
        pass
    def subzone_6(self):
        pass
    def subzone_7(self):
        pass
    def subzone_8(self):
        pass

class Hell():
    """
    Cette classe permet de gérer toutes les subzones de la zone "Hell". 
    """
    def __init__(self, subzone, fenetre, current_player):
        self.zone = 4
        self.collisions = []
    def subzone_1(self):
        pass
    def subzone_2(self):
        pass
    def subzone_3(self):
        pass
    def subzone_4(self):
        pass
    def subzone_5(self):
        pass
    def subzone_6(self):
        pass
    def subzone_7(self):
        pass
    def subzone_8(self):
        pass

class Boss():
    """
    Cette classe permet de gérer tout ce qui est en rapport avec le boss, comme le fond ou les plateformes...
    """
    def __init__(self):
        self.zone = 5
        self.collisions = []
    
    def zone_boss(self):
        pass

class Main():
    """
    La Classe Main() est la classe qui repertorie et contrôle les niveaux.
    """
    def __init__(self, current_player, fenetre):
        subzone = current_player.subzone
        self.Plains_Levels = Plains(subzone, fenetre, current_player)
        self.Desert_Levels = Desert(subzone, fenetre, current_player)
        self.Mountains_Levels = Mountains(subzone, fenetre, current_player)
        self.Hell_Levels = Hell(subzone, fenetre, current_player)
        self.Boss_Level = Boss()

        
        self.collisions = []


    def choose(self, current_player):
        """
        Cette méthode permet de choisir la bonne classe et la bonne méthode selon la zone et la subzone du joueur. 
        Pré-Condition : Elle prend en argument l'objet current_player de la classe Sprite_Player. 
        """
        zonep = current_player.zone
        subzonep = current_player.subzone
        if zonep == 1:
            self.collisions = self.Plains_Levels.collisions
            zone_name = self.Plains_Levels
            if subzonep == 0:
                zone_name.subzone_0()
            elif subzonep == 1:
                zone_name.subzone_1()
            elif subzonep == 2:
                zone_name.subzone_2()
            elif subzonep == 3:
                zone_name.subzone_3()
            elif subzonep == 4:
                zone_name.subzone_4()
            elif subzonep == 5:
                zone_name.subzone_5()
            elif subzonep == 6:
                zone_name.subzone_6()
            elif subzonep == 7:
                zone_name.subzone_7()
            elif subzonep == 8:
                zone_name.subzone_8()
            "eval(f'zone_name.subzone_{subzonep}()') #! eval permet de transformer une chaine de caractère en code. "
            if subzonep > self.Plains_Levels.last_zone:
                current_player.zone = 2
                current_player.subzone = 0

        elif zonep == 2:
            self.collisions = self.Desert_Levels.collisions
            zone_name = self.Desert_Levels
            if subzonep == 1:
                zone_name.subzone_1
            elif subzonep == 2:
                zone_name.subzone_2
            elif subzonep == 3:
                zone_name.subzone_3
            elif subzonep == 4:
                zone_name.subzone_4
            elif subzonep == 5:
                zone_name.subzone_5
            elif subzonep == 6:
                zone_name.subzone_6
            elif subzonep == 7:
                zone_name.subzone_7
            elif subzonep == 8:
                zone_name.subzone_8
            elif subzonep > 8:
                current_player.zone = 3
                current_player.subzone = 0

        elif zonep == 3:
            self.collisions = self.Mountains_Levels.collisions
            zone_name = self.Mountains_Levels
            if subzonep == 1:
                zone_name.subzone_1
            elif subzonep == 2:
                zone_name.subzone_2
            elif subzonep == 3:
                zone_name.subzone_3
            elif subzonep == 4:
                zone_name.subzone_4
            elif subzonep == 5:
                zone_name.subzone_5
            elif subzonep == 6:
                zone_name.subzone_6
            elif subzonep == 7:
                zone_name.subzone_7
            elif subzonep == 8:
                zone_name.subzone_8
            elif subzonep > 8:
                current_player.zone = 4
                current_player.subzone = 0

        elif zonep == 4:
            self.collisions = self.Hell_Levels.collisions
            zone_name = self.Hell_Levels
            if subzonep == 1:
                zone_name.subzone_1
            elif subzonep == 2:
                zone_name.subzone_2
            elif subzonep == 3:
                zone_name.subzone_3
            elif subzonep == 4:
                zone_name.subzone_4
            elif subzonep == 5:
                zone_name.subzone_5
            elif subzonep == 6:
                zone_name.subzone_6
            elif subzonep == 7:
                zone_name.subzone_7
            elif subzonep == 8:
                zone_name.subzone_8
            elif subzonep > 8:
                current_player.zone = 5
                current_player.subzone = 0

        elif zonep == 5:
            self.collsiions = self.Boss_Level.collisions
            zone_name = self.Boss_Level
            if subzonep == 1:
                zone_name.subzone_1
            current_player.zone = 5
            current_player.subzone = 1


