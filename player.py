import pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, sky_surface_height, screen_width):
        super().__init__()
        player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, sky_surface_height))
        self.gravity = 0
        self.position_x = self.rect.x
        self.position_y = self.rect.y

        self.sky_surface_height = sky_surface_height
        self.screen_width = screen_width

    def player_input(self, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.sky_surface_height:
            self.gravity = -1000

        if keys[pygame.K_a]:
            self.position_x -= 200 * delta_time
            if self.position_x < 0:
                self.position_x = 0
            self.rect.x = self.position_x

        if keys[pygame.K_d]:
            self.position_x += 200 * delta_time

            if self.position_x > self.screen_width - self.rect.width:
                self.position_x = self.screen_width - self.rect.width

            self.rect.x = self.position_x

    def apply_gravity(self, delta_time):
        self.position_y += self.gravity * delta_time
        self.rect.y = self.position_y
        if self.rect.bottom >= self.sky_surface_height:
            self.rect.bottom = self.sky_surface_height
            self.gravity = 0
        self.gravity += 3000 * delta_time

    def animation_state(self, delta_time):
        if self.rect.bottom < self.sky_surface_height:
            self.image = self.player_jump
            return

        self.player_index += delta_time * 5
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self, **kwargs):
        self.player_input(kwargs['delta_time'])
        self.apply_gravity(kwargs['delta_time'])
        self.animation_state(kwargs['delta_time'])