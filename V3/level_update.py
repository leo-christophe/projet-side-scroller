import pygame
from ennemie_objects import Ennemies

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
        self.height = 720
        self.width = 1280
        self.fps = 60
        self.fenetre = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)   
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
    def __init__(self, subzone, fenetre, current_player, menu):
        self.bg = pygame.image.load("assets/textures/background/fond_plaines.png").convert()
        self.bg = pygame.transform.scale(self.bg, (Game_Parameters.width, Game_Parameters.height))
        self.dirt_platform = pygame.image.load("assets/textures/props/dirt_platform.png")
        self.dirt_wall = pygame.image.load("assets/textures/props/dirt_wall.png").convert()
        self.light_platform = pygame.image.load("assets/textures/props/light_dirt_platform.png")
        self.summer_tree = pygame.image.load("assets/textures/props/summer_tree_1.png").convert_alpha()

        self.fenetre = fenetre
        self.player = current_player
        self.Game_Menu = menu
        self.subzone = subzone
        self.last_zone = 8

        #######################
        # PLATEFORMES DE ZONE #
        #######################
        self.plat1 = platform_creation(self.dirt_platform, 0, Game_Parameters.height - self.dirt_platform.get_height())
        self.plat2 = platform_creation(self.dirt_platform, self.plat1.rect.width + 120, Game_Parameters.height - self.dirt_platform.get_height())

        self.plat1b = platform_creation(self.dirt_platform, -Game_Parameters.width*(1/4), Game_Parameters.height - self.dirt_platform.get_height())
        self.dirt_wallrect = platform_creation(self.dirt_wall, self.plat1b.rect.right + 100, y=Game_Parameters.height - self.dirt_platform.get_height())
        self.plat2b = platform_creation(self.dirt_platform, self.dirt_wallrect.rect.right + 100, Game_Parameters.height - self.dirt_platform.get_height())

        self.light_plat = platform_creation(self.light_platform, 100, Game_Parameters.height - self.dirt_platform.get_height() - 80)
        self.light_plat2 = platform_creation(self.light_platform, 150, Game_Parameters.height - self.dirt_platform.get_height() - 100)
        self.tree = platform_creation(self.summer_tree, 150, Game_Parameters.height - self.dirt_platform.get_height() - self.summer_tree.get_height())
        self.tree2 = platform_creation(self.summer_tree, 300, Game_Parameters.height - self.dirt_platform.get_height() - self.summer_tree.get_height())

        self.collisions_list_plains = [
        [self.plat1.rect, self.plat2.rect],
        [self.plat1b.rect, self.dirt_wallrect.rect, self.plat2b.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1b.rect, self.dirt_wallrect.rect, self.plat2b.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1.rect, self.plat2.rect],
        [self.plat1b.rect, self.dirt_wallrect.rect, self.plat2b.rect],
        [self.plat1.rect, self.plat2.rect]
        ]
        self.collisions = self.collisions_list_plains[0]

        ###################
        # ENNEMIS DE ZONE #
        ###################
        self.flowery = Ennemies("flowery", "attack_spores", Game_Parameters.width/2, Game_Parameters.height - self.dirt_platform.get_height() - 32, 32, 32)
        self.flowery2 = Ennemies("flowery", "attack_spores", Game_Parameters.width*(2/3), Game_Parameters.height - self.dirt_platform.get_height() - 32, 32, 32)
        self.cloudy = Ennemies("cloudlo", "", Game_Parameters.width * (2/5), Game_Parameters.height * (1/5), 32, 32, type_m="air")
        self.spike = Ennemies("spike", "", self.cloudy.rect.x, self.cloudy.rect.y, 32, 32, bool_project = True, type_m = "projectile")
        self.machine = Ennemies("machine", "", self.plat1b.rect.right + 100 + (1/2)*self.dirt_wallrect.rect.width, Game_Parameters.height - self.dirt_platform.get_height() - 64, 32, 64, bool_project = False, type_m = "machine")
        self.arrow = Ennemies("arrow", "", self.plat1b.rect.right + 100 + (1/2)*self.dirt_wallrect.rect.width, Game_Parameters.height - self.dirt_platform.get_height() - 32, 64, 8, bool_project = True, type_m = "projectile")

        self.ennemies_list_plains = [
        [self.flowery],
        [self.cloudy, self.spike],
        [self.flowery, self.flowery2],
        [],
        [self.machine, self.arrow],
        [],
        [],
        []
        ]
        self.ennemies = self.ennemies_list_plains[0]

    def window_refreshing(self, fenetre):
        """
        Petite méthode répétée à chaque fois que le joueur se trouve dans une subzone, elle sert à rafraichir le fond et placer le joueur.
        """
        fenetre.blit(self.bg, (0, 0))
        redrawWindow(self.fenetre, self.player)

    def subzone_0(self):
        """
        La première sous-zone de tout le jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        ####################
        # INITIALISATIONS  #
        ####################
        self.collisions = self.collisions_list_plains[0]
        self.ennemies = self.ennemies_list_plains[0]
        fenetre = self.fenetre
        
        ######################
        # CHARGEM. FENETRES  #
        ######################
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   
        fenetre.blit(self.summer_tree, self.tree)
        fenetre.blit(self.summer_tree, self.tree2)
        
        #######################
        # CHARGEM. ENNEMIES   #
        #######################
        self.flowery.ennemies_update(self.collisions, self.player, fenetre)
        fenetre.blit(self.flowery.img, self.flowery.rect)
        #fenetre.blit(self.dirt_wall, (self.dirt_wallrect.rect.x, self.dirt_wallrect.rect.y))   

    def subzone_1(self):
        """
        La deuxième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        ####################
        # INITIALISATIONS  #
        ####################
        self.collisions = self.collisions_list_plains[1]
        self.ennemies = self.ennemies_list_plains[1]
        fenetre = self.fenetre
        
        ######################
        # CHARGEM. FENETRES  #
        ######################
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1b.rect.x, self.plat1b.rect.y))  
        fenetre.blit(self.dirt_wall, (self.dirt_wallrect.rect.x, self.dirt_wallrect.rect.y)) 
        fenetre.blit(self.dirt_platform, (self.plat2b.rect.x, self.plat2b.rect.y))   
        fenetre.blit(self.summer_tree, self.tree)
        
        #######################
        # CHARGEM. ENNEMIES   #
        #######################
        fenetre.blit(self.cloudy.img, self.cloudy.rect)
        fenetre.blit(self.spike.img, self.spike.rect)
        self.cloudy.ennemies_update(self.collisions, self.player, fenetre)
        self.spike.ennemies_update(self.collisions, self.player, fenetre)
        
    def subzone_2(self):
        """
        La troisième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        ####################
        # INITIALISATIONS  #
        ####################
        self.collisions = self.collisions_list_plains[2]
        self.ennemies = self.ennemies_list_plains[2]
        fenetre = self.fenetre
        
        ######################
        # CHARGEM. FENETRES  #
        ######################
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.summer_tree, self.tree)
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   
        
        #######################
        # CHARGEM. ENNEMIES   #
        #######################
        fenetre.blit(self.flowery.img, self.flowery.rect)
        self.flowery.ennemies_update(self.collisions, self.player, fenetre)
        fenetre.blit(self.flowery2.img, self.flowery2.rect)
        self.flowery2.ennemies_update(self.collisions, self.player, fenetre)

    def subzone_3(self):
        """
        La quatrième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        ####################
        # INITIALISATIONS  #
        ####################
        self.collisions = self.collisions_list_plains[3]
        self.ennemies = self.ennemies_list_plains[3]
        fenetre = self.fenetre
        
        ######################
        # CHARGEM. FENETRES  #
        ######################
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))

    def subzone_4(self):
        """
        La cinquième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        ####################
        # INITIALISATIONS  #
        ####################
        self.collisions = self.collisions_list_plains[4]
        self.ennemies = self.ennemies_list_plains[4]
        fenetre = self.fenetre

        ######################
        # CHARGEM. FENETRES  #
        ######################
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1b.rect.x, self.plat1b.rect.y))  
        fenetre.blit(self.dirt_wall, (self.dirt_wallrect.rect.x, self.dirt_wallrect.rect.y)) 
        fenetre.blit(self.dirt_platform, (self.plat2b.rect.x, self.plat2b.rect.y))   
        fenetre.blit(self.summer_tree, self.tree)
        fenetre.blit(self.summer_tree, self.tree2)

        #######################
        # CHARGEM. ENNEMIES   #
        #######################
        fenetre.blit(self.machine.img, self.machine.rect)
        fenetre.blit(self.arrow.img, self.arrow.rect)
        self.machine.ennemies_update(self.collisions, self.player, fenetre)
        self.arrow.ennemies_update(self.collisions, self.player, fenetre)

    def subzone_5(self):
        """
        La sixième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        self.collisions = self.collisions_list_plains[5]
        self.ennemies = self.ennemies_list_plains[5]
        fenetre = self.fenetre
        
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   

    def subzone_6(self):
        """
        La septième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        self.collisions = self.collisions_list_plains[6]
        self.ennemies = self.ennemies_list_plains[6]
        fenetre = self.fenetre

        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   

    def subzone_7(self):
        """
        La huitième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        self.collisions = self.collisions_list_plains[7]
        self.ennemies = self.ennemies_list_plains[7]
        fenetre = self.fenetre

        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1b.rect.x, self.plat1b.rect.y))  
        fenetre.blit(self.dirt_wall, (self.dirt_wallrect.rect.x, self.dirt_wallrect.rect.y)) 
        fenetre.blit(self.dirt_platform, (self.plat2b.rect.x, self.plat2b.rect.y))   

    def subzone_8(self):
        """
        La neuvième sous-zone du jeu, elle place les décors, les plateformes, le joueur et les ennemis.
        """
        #? Initialisations
        self.collisions = self.collisions_list_plains[8]
        fenetre = self.fenetre
        
        #? affichage des plateformes et rafraichissements
        self.window_refreshing(fenetre)
        fenetre.blit(self.dirt_platform, (self.plat1.rect.x, self.plat1.rect.y))   
        fenetre.blit(self.dirt_platform, (self.plat2.rect.x, self.plat2.rect.y))   

        #? Afficher la fin du jeu
        if self.player.rect.x > Game_Parameters.width:
            return self.Game_Menu.temporary_end()

class Main():
    """
    La Classe Main() est la classe qui repertorie et contrôle les niveaux ainsi que les ennemis.
    """
    def __init__(self, current_player, fenetre, menu):
        subzone = current_player.subzone
        self.Plains_Levels = Plains(subzone, fenetre, current_player, menu)
        self.menu = menu
        
        self.collisions = []
        self.ennemies = []

    def choose(self, current_player):
        """
        Cette méthode permet de choisir la bonne classe et la bonne méthode selon la zone et la subzone du joueur. 
        Pré-Condition : Elle prend en argument l'objet current_player de la classe Sprite_Player. 
        """
        zonep = current_player.zone
        subzonep = current_player.subzone
        if zonep == 1:
            self.collisions = self.Plains_Levels.collisions
            self.ennemies = self.Plains_Levels.ennemies
            zone_name = self.Plains_Levels
            if subzonep == 0:
                return zone_name.subzone_0()
            elif subzonep == 1:
                return zone_name.subzone_1()
            elif subzonep == 2:
                return zone_name.subzone_2()
            elif subzonep == 3:
                return zone_name.subzone_3()
            elif subzonep == 4:
                return zone_name.subzone_4()
            elif subzonep == 5:
                return zone_name.subzone_5()
            elif subzonep == 6:
                return zone_name.subzone_6()
            elif subzonep == 7:
                return zone_name.subzone_7()
            elif subzonep == 8:
                return zone_name.subzone_8()

            if subzonep > self.Plains_Levels.last_zone:
                return self.menu.temporary_end()




