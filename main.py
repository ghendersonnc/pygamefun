import pygame
import time
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
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

    def player_input(self, delta_times):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= sky_surface_height:
            self.gravity = -1000

        if keys[pygame.K_a]:
            self.position_x -= 200 * delta_times
            if self.position_x < 0:
                self.position_x = 0
            self.rect.x = self.position_x

        if keys[pygame.K_d]:
            self.position_x += 200 * delta_times

            if self.position_x > SCREEN_WIDTH - self.rect.width:
                self.position_x = SCREEN_WIDTH - self.rect.width

            self.rect.x = self.position_x

    def apply_gravity(self, delta_times):
        self.position_y += self.gravity * delta_times
        self.rect.y = self.position_y
        if self.rect.bottom >= sky_surface_height:
            self.rect.bottom = sky_surface_height
            self.gravity = 0
        self.gravity += 3000 * delta_times

    def animation_state(self, delta_times):
        if self.rect.bottom < sky_surface_height:
            self.image = self.player_jump
            return

        self.player_index += delta_times * 5
        if self.player_index >= len(self.player_walk):
            self.player_index = 0
        self.image = self.player_walk[int(self.player_index)]

    def update(self, **kwargs):
        self.player_input(kwargs['delta_time'])
        self.apply_gravity(kwargs['delta_time'])
        self.animation_state(kwargs['delta_time'])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type):
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

    def animation_state(self, delta_times):
        if self.type == 'fly':
            self.animation_index += delta_times * 5
        else:
            self.animation_index += delta_times * 2

        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def move(self, delta_times):
        self.position_x -= 400 * delta_times
        self.rect.x = self.position_x

    def destroy(self):
        if self.rect.x < -100:
            self.kill()

    def update(self, **kwargs):
        self.animation_state(kwargs['delta_time'])
        self.move(kwargs['delta_time'])
        self.destroy()


def display_score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = pixel_font.render(f"{current_score}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    SCREEN.blit(score_surface, score_rect)


def collision_sprite():
    if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False):
        enemy_group.empty()
        player_group.empty()
        return True
    return False


pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
sky_surface = pygame.image.load('graphics/Sky.png').convert()
sky_surface_height = sky_surface.get_height()
ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_position = (0, sky_surface_height)
running = True
game_over = True
start_time = 0
clock = pygame.time.Clock()

# Groups
player_group = pygame.sprite.GroupSingle()
player_group.add(Player())

enemy_group = pygame.sprite.Group()

pixel_font = pygame.font.Font('font/Pixeltype.ttf', 50)

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand_scaled.get_rect(center=(400, 200))

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1200)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

previous_time = time.time()
while running:
    if not running:
        pygame.quit()
        break

    delta_time = time.time() - previous_time
    previous_time = time.time()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    player_group.add(Player())
                    game_over = False

        else:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(random.choice(['fly', 'snail'])))

    if not game_over:
        SCREEN.blit(sky_surface, (0, 0))
        SCREEN.blit(ground_surface, ground_position)

        display_score()

        player_group.draw(SCREEN)
        player_group.update(delta_time=delta_time)
        enemy_group.draw(SCREEN)
        enemy_group.update(delta_time=delta_time)
        game_over = collision_sprite()

    else:
        start_time = int(pygame.time.get_ticks() / 1000)
        SCREEN.fill('#007a7a')
        SCREEN.blit(player_stand_scaled, player_stand_rectangle)

    pygame.display.update()

print('bye')
