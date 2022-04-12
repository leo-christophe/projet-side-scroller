import pygame
class Ennemies():
    """
    Cette classe gère les ennemis du jeu.
    """
    def __init__(self, img, particle, x, y, width, height, type_m = "commun", bool_project = False):
        """ 
        Initialisation de la classe, img est le nom de l'image, particle à "" si n'y en a pas, sinon le nom de la particule qui est affichée quand le joueur rentre
        en collision avec l'ennemi, x, y, width : la longueur, height : la largeur, type_m : le type de l'ennemi, bool_project : le booléen vrai ou faux si c'est un
        projectile.
        """
        ################
        # STATISTIQUES #
        ################
        self.vie = 20
        self.dmg = 1.0
        self.speed = 2
        self.type_m = type_m

        self.spawn = (x, y)
        self.index_t = 0

        ####################
        # CARACTERISTIQUES #
        ####################
        self.img_name = img
        self.img = pygame.image.load(f"assets/textures/ennemies/{img}.png")
        if particle != "":    
            self.particle = pygame.image.load(f"assets/textures/particles/{particle}.png")
        else:
            self.particle = ""
        self.rect = pygame.Rect((x, y), (width, height))

        self.projectile = bool_project

    def ennemies_update(self, collisions, player, fenetre):
        """
        cette méthode s'exécute à chaque tour de boucles pour gérer les ennemis. 
        la liste des collisions du jeu, le joueur et la fenêtre sont en argument.
        """
        if self.img_name == "arrow":
            if self.rect.x < 0:
                self.rect.x = self.spawn[0]
            self.rect.x -= 5

        if self.type_m == "air" or self.img_name == "spike":
            if self.index_t < 260:
                self.rect = self.rect.move(self.speed, self.rect.y)
            else:
                if self.projectile:
                    if self.rect.left < player.rect.right + 5:
                        self.rect.y += 10
                self.index_t = 0
                self.speed = self.speed * -1
            self.index_t += 1

        if self.type_m == "commun":
            if self.rect.collidelist(collisions) != -1 and (self.rect.left <= collisions[self.rect.collidelist(collisions)].right or self.rect.right >= collisions[self.rect.collidelist(collisions)].left):
                self.speed = self.speed * -1
            self.rect.x -= 1.5 * self.speed
            
        if self.rect.colliderect(player.rect):
            if self.particle != "":
                fenetre.blit(self.particle, self.rect)