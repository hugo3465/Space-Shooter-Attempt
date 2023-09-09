import pygame
from Enemies.Enemy import *
from Constants import *

class Asteroid(Enemy, pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(ASTEROID_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)

    def check_boaders(self): 
        if(self.rect.x > WINDOW_HEIGHT or self.rect.x < 0 or self.rect.y > WINDOW_WIDTH):
            self.kill()
    
    def movement(self):
        self.rect.y += 5

    def update(self):
        self.movement()
        self.check_boaders()