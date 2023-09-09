import pygame
from Constants import *
from laser import Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, game, pos, speed):
        super().__init__()

        self.game = game

        self.x, self.y = pos

        self.SPEED = speed

        # Laser
        self.ready = True 
        self.lasers = pygame.sprite.Group()
        self.laser_time = 0
        self.laser_cooldown = LASER_COOLDOWN
        self.laser_sound = pygame.mixer.Sound('audio/laser.wav')
        self.laser_sound.set_volume(0.5)

        # Um player precisa de ter duas vars, a imagem e a hitbox
        # Assign to 'image' attribute
        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)

    def check_border(self, x, y):
        return x >= 0 and x < (WINDOW_HEIGHT - PLAYER_SIZE) and y >= 0 and y < (WINDOW_WIDTH - PLAYER_SIZE)

    def check_border_colision(self, dx, dy):
        if self.check_border((self.x + dx), self.y):
            self.x += dx
        if self.check_border(self.x, (self.y + dy)):
            self.y += dy

    def get_input(self):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_DOWN]):
            dy += self.SPEED
        if (keys[pygame.K_UP]):
            dy -= self.SPEED
        if (keys[pygame.K_LEFT]):
            dx -= self.SPEED
        if (keys[pygame.K_RIGHT]):
            dx += self.SPEED
        if (keys[pygame.K_SPACE] and self.ready):
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

        self.check_border_colision(dx, dy)

        self.rect.x = self.x
        self.rect.y = self.y

        print(self.x, ',', self.y)

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center,-LASER_SPEED,self.rect.bottom))

    def update(self):
        self.get_input()
        self.recharge()
        self.lasers.update()




    def get_coordinates(self):
        return (self.rect.x, self.rect.y)
