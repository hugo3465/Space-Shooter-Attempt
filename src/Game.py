import pygame
import sys
import time
from random import randint

from Constants import *
from Player import *
from Enemies.Asteroid import Asteroid
from Enemies.Airship import Airship


class Game:
    def __init__(self):
        pygame.init()

        self.game_active = True

        self.screen = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))

        self.clock = pygame.time.Clock()

        self.background_image = pygame.image.load(
            'imgs/background.png').convert()

        self.imagetest = pygame.image.load(
            'imgs/Enemies/Asteroid/asteroid.png').convert_alpha()

        # timer
        self.asteroid_enemy_timer = pygame.USEREVENT + 1
        # vai ser chamado de 1500 milisegundos
        pygame.time.set_timer(self.asteroid_enemy_timer, 1500)

        self.airship_enemy_timer = pygame.USEREVENT + 2
        # vai ser chamado de 2500 milisegundos
        pygame.time.set_timer(self.airship_enemy_timer, 2500)

        # Death animations
        self.death_image = pygame.image.load(
            'imgs/Player/exceperotion.gif').convert_alpha()
        self.death_sound = pygame.mixer.Sound('audio/exceperotion.mp3')
        self.death_sound.set_volume(0.3)

        self.new_game()

    def new_game(self):  # cria instacias de classes, ou quase
        # Player
        player_sprite = Player(self, (4, 2), PLAYER_SPEED)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Enemies
        self.asteroid_enemy_list = pygame.sprite.Group()
        self.airship_enemy_list = pygame.sprite.Group()

    def check_events(self):
        for event in pygame.event.get():
            # close buttom
            if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()

            # spawn asteroids
            if event.type == self.asteroid_enemy_timer:
                self.asteroid_enemy_list.add(
                    Asteroid(self, (randint(90, WINDOW_HEIGHT - 15), 0)))

            # spawn airships
            if event.type == self.airship_enemy_timer:
                self.airship_enemy_list.add(
                    Airship(self, (randint(90, WINDOW_HEIGHT - 15), 0)))

    def explosion(self):  # TODO não está a funcionar
        x, y = self.player.sprite.get_coordinates()

        self.explosion_group = pygame.sprite.Group()
        explosion = Explosion(x + 50, y + 50)
        self.explosion_group.add(explosion)

    def end_game(self):
        self.death_sound.play()
        self.explosion()
        self.game_active = False
    
    def check_colision(self):
        if not self.game_active:
            return

        # colision with asteroids
        if pygame.sprite.spritecollideany(self.player.sprite, self.asteroid_enemy_list):
            self.end_game()

        # colision with airships
        if pygame.sprite.spritecollideany(self.player.sprite, self.airship_enemy_list):
            self.end_game()

        # Check collision between enemy airship lasers and the player
        for enemy in self.airship_enemy_list:
            if pygame.sprite.spritecollide(self.player.sprite, enemy.lasers, True): # The True flag will remove the sprite in block_list  
                self.end_game()

        # Player lasers
        if self.player.sprite.lasers:
            # Check collision between player lasers and enemies
            for laser in self.player.sprite.lasers:
                # enemy list and laser collision
                asteroid_hit = pygame.sprite.spritecollide(
                    laser, self.asteroid_enemy_list, True)  # remove o asteroid quando colide
                if asteroid_hit:
                    laser.kill()

                airship_hit = pygame.sprite.spritecollide(
                    laser, self.airship_enemy_list, True)  # remove a airship quando colide
                if airship_hit:
                    laser.kill()


    def draw(self):
        # Background
        self.screen.blit(self.background_image, (0, 0))

        # Player Lasers
        self.player.sprite.lasers.draw(self.screen)

        # Player
        self.player.draw(self.screen)

        # Enemies
        self.asteroid_enemy_list.draw(self.screen)
        self.airship_enemy_list.draw(self.screen)

        # enemy airship lasers
        for enemy in self.airship_enemy_list:
            enemy.lasers.draw(self.screen)

    def update(self):
        pygame.display.flip()
        self.clock.tick(FPS)  # limita os fps a 60

    def run(self):
        self.check_events()
        self.update()
        self.draw()

        if self.game_active:
            # player
            self.player.update()  # draw player

            # Enemies
            self.asteroid_enemy_list.update()
            self.airship_enemy_list.update()

            self.check_colision()

# TODO explosion class not working
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"imgs/Player/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0

    def update(self):
        explosion_speed = 4
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, reset animation index
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


if __name__ == '__main__':  # o que executa o programa
    game = Game()

    while True:
        game.run()
