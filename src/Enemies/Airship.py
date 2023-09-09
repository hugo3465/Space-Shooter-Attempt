import pygame
from Enemies.Enemy import *
from Constants import *
from laser import Laser

class Airship(Enemy, pygame.sprite.Sprite):
    def __init__(self, game, pos):
        super().__init__(game, pos)
        pygame.sprite.Sprite.__init__(self)

        self.clock = pygame.time.Clock()

        self.image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect(midbottom=pos)

        # lasers
        self.lasers = pygame.sprite.Group()

        # attack timer
        self.airship_attack_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.airship_attack_timer, 1500)

        self.speed = ENEMY_AIRSHIP_SPEED

    def check_boaders(self):
        if (self.rect.x > WINDOW_HEIGHT or self.rect.x < 0 or self.rect.y > WINDOW_WIDTH):
            self.kill()

    def movement(self):
        self.rect.y += 2

        # moving to the side TODO: not working properly
        self.rect.x += self.speed
        if self.rect.x == 650 or self.rect.x == 15:
            self.speed = -self.speed

    def attack(self):
        for event in pygame.event.get():
            if event.type == self.airship_attack_timer:
                self.shoot_laser()

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, LASER_SPEED, WINDOW_HEIGHT))

    def update(self):
        self.movement()
        self.check_boaders()
        self.attack()
        self.lasers.update()
