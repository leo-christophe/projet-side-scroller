import pygame

class Sprite_Player(pygame.sprite.Sprite):
    
    def __init__(self, longueur=32, largeur=32):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("assets/player.png")
        self.size = self.image.get_size()
        self.rect = self.image.get_rect()
        self.vie = 100
        self.att = 1
        self.pos = (self.size[1], 720 - self.size[1] - 165)

    def goRight(self, marge):
        self.rect.x += marge
        return self.rect

    def goLeft(self, marge):
        self.rect.x -= marge
        self.pos = self.pos.move(-marge, 0)

    def Jump(self, jump):
        self.rect.y -= jump

 


