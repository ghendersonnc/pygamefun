import pygame
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, sky_surface_height):
        super().__init__()
        self.type = enemy_type
        if enemy_type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png')
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png')
            self.frames = [fly_1, fly_2]
            position_y = sky_surface_height - 100
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            position_y = sky_surface_height

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(random.randint(900, 1100), position_y))
        self.position_x = self.rect.x
        self.position_y = self.rect.y

    def animation_state(self, delta_time):
        if self.type == 'fly':
            self.animation_index += delta_time * 5
        else:
            self.animation_index += delta_time * 2

        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def move(self, delta_time):
        self.position_x -= 400 * delta_time
        self.rect.x = self.position_x

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self, **kwargs):
        self.animation_state(kwargs['delta_time'])
        self.move(kwargs['delta_time'])
        self.destroy()
