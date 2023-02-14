import pygame
import time
import random

from player import Player
from enemy import Enemy

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
player_group.add(Player(sky_surface_height, SCREEN_WIDTH))

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
                    player_group.add(Player(sky_surface_height, SCREEN_WIDTH))
                    game_over = False

        else:
            if event.type == enemy_timer:
                enemy_group.add(Enemy(random.choice(['fly', 'snail']), sky_surface_height))

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
