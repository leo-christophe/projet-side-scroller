
from main import pygame, mixer
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
            self.selection = 0

        elif self.selection == 2:
            self.options()
            self.selection = 2

        elif self.selection == 3:
            pygame.quit()
            self.selection = 0
            quit()

    def options(self):
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
                        self.sound_playing()

                    elif txt_o4b.collidepoint(pos_click):
                        music_playing = False
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
        global sounds_playing
        if sounds_playing:
            button.play()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)
    return textrect

button = mixer.Sound("assets/sounds/GUI/button.mp3")