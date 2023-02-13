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

            if self.position_x > 800 - self.rect.width:
                self.position_x = 800 - self.rect.width

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
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == 'fly':
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

            if self.animation_index >= len(self.frames):
                self.animation_index = 0
            self.image = self.frames[int(self.animation_index)]

    def update(self, **kwargs):
        self.animation_state(kwargs['delta_time'])


def display_score():
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = pixel_font.render(f"{current_score}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    SCREEN.blit(score_surface, score_rect)


# def enemy_movement(enemy_list, delta_times):
#     # 0 = rect
#     # 1 = X position
#     # 2 = Y position
#     if enemy_list:
#         for enemy in enemy_list:
#             enemy[1] -= enemy_speed * delta_times
#             enemy[0].x = enemy[1]
#
#             if enemy[0].bottom == sky_surface_height:
#                 SCREEN.blit(snail_surface, enemy[0])
#             else:
#                 SCREEN.blit(fly_surface, enemy[0])
#
#         # Recreate enemy_list with enemies that are on the screen
#         # This essentially "Deletes" enemies whose bottom right X coordinate is greater than 0
#         #     since if that coordinate is 0 or less, it is not within the viewport
#         enemy_list = [enemy for enemy in enemy_list if enemy[0].bottomright[0] > 0]
#
#         return enemy_list
#     return []


def collisions(player, enemies):
    if enemies:
        for enemy in enemies:
            if player.colliderect(enemy[0]):
                return True
    return False


def player_animation(delta_times):
    global player_surface, player_index

    # player walkin

    # jumpin :o
    if player_rectangle.bottom < sky_surface_height:
        player_surface = player_jump
    else:
        player_index += delta_times * 5
        if player_index >= len(player_walk):
            player_index = 0
        player_surface = player_walk[int(player_index)]


pygame.init()

SCREEN = pygame.display.set_mode((800, 400))
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
# text_surface = test_font.render('game', False, (42, 42, 42))
# text_rectangle = text_surface.get_rect(center=(400, 50))

# Snail
# snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_frames = [snail_1, snail_2]
# snail_index = 0
# snail_surface = snail_frames[snail_index]

# Fly
# fly_1 = pygame.image.load('graphics/Fly/Fly1.png')
# fly_2 = pygame.image.load('graphics/Fly/Fly2.png')
# fly_frames = [fly_1, fly_2]
# fly_index = 0
# fly_surface = fly_frames[fly_index]

# snail_rectangle = snail_surface.get_rect(bottomleft=(1000, sky_surface_height))
# snail_position_x = snail_rectangle.x
# snail_position_y = snail_rectangle.y

enemy_rectangles = []

enemy_speed = 250.0
enemy_speed_multiplier = 1.3

player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_index = 0
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_surface = player_walk[player_index]
player_rectangle = player_surface.get_rect(bottomleft=(80, sky_surface_height))
player_position_x = player_rectangle.x
player_position_y = player_rectangle.y

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
# player_stand_scaled = pygame.transform.scale2x(player_stand)
player_stand_scaled = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rectangle = player_stand_scaled.get_rect(center=(400, 200))

gravity = 0

enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1400)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

previous_time = time.time()
while running:
    if not running:
        pygame.quit()
        break

    # Calculate delta time so that we can use that to ensure stuff moves X pixels every second rather than every frame
    delta_time = time.time() - previous_time
    previous_time = time.time()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False

                    # Reset to left side of screen
                    player_position_x = 80
                    player_rectangle.x = player_position_x

                    # Reset to ground
                    player_position_y = sky_surface_height
                    player_rectangle.y = player_position_y

                    # general stuff I guess
                    enemy_speed = 200.0
                    enemy_speed_multiplier = 1.3
                    gravity = 0
        else:
            if event.type == enemy_timer:
                x_coordinate = random.randint(900, 1000)
                enemy_group.add(Enemy('fly'))
                # if random.randint(0, 2):
                #     snail_rectangle = snail_surface.get_rect(bottomleft=(x_coordinate, sky_surface_height))
                #     snail_position_x = snail_rectangle.x
                #     snail_position_y = snail_rectangle.y
                #     enemy_rectangles.append([snail_rectangle, snail_position_x, snail_position_y])
                # else:
                #     fly_rectangle = fly_surface.get_rect(bottomleft=(x_coordinate, sky_surface_height - 100))
                #     fly_position_x = fly_rectangle.x
                #     fly_position_y = fly_rectangle.y
                #     enemy_rectangles.append([fly_rectangle, fly_position_x, fly_position_y])
            # if event.type == snail_animation_timer:
            #     if snail_index == 0:
            #         snail_index = 1
            #     else:
            #         snail_index = 0
            #     snail_surface = snail_frames[snail_index]
            # if event.type == fly_animation_timer:
            #     if fly_index == 0:
            #         fly_index = 1
            #     else:
            #         fly_index = 0
            #     fly_surface = fly_frames[fly_index]
    if not game_over:
        SCREEN.blit(sky_surface, (0, 0))
        SCREEN.blit(ground_surface, ground_position)

        display_score()

        # Snail Stuff
        # snail_position_x -= enemy_speed * delta_time
        #
        # if snail_position_x < -100:
        #     enemy_speed *= enemy_speed_multiplier
        #     if enemy_speed_multiplier > 1.0:
        #         enemy_speed_multiplier -= 0.03
        #
        #     snail_position_x = 800
        #
        # snail_rectangle.x = snail_position_x

        # Character stuffs
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_d]:
        #     player_position_x += 200 * delta_time
        #     player_rectangle.x = player_position_x
        #
        # if keys[pygame.K_a]:
        #     player_position_x -= 200 * delta_time
        #     player_rectangle.x = player_position_x
        #
        # if keys[pygame.K_SPACE] and player_position_y + player_rectangle.h >= sky_surface_height:
        #     gravity = -1000

        if gravity != 0:
            player_position_y += gravity * delta_time

            if player_position_y + player_rectangle.h >= sky_surface_height:
                player_position_y = sky_surface_height - player_rectangle.h
                gravity = 0

            player_rectangle.y = player_position_y
        gravity += 3000 * delta_time
        player_animation(delta_time)
        # SCREEN.blit(player_surface, player_rectangle)

        player_group.draw(SCREEN)
        player_group.update(delta_time=delta_time)
        enemy_group.draw(SCREEN)
        enemy_group.update(delta_time=delta_time)

        # enemy_rectangles = enemy_movement(enemy_rectangles, delta_time)

        game_over = collisions(player_rectangle, enemy_rectangles)

    else:
        enemy_rectangles.clear()
        start_time = int(pygame.time.get_ticks() / 1000)
        SCREEN.fill('#007a7a')
        SCREEN.blit(player_stand_scaled, player_stand_rectangle)

    pygame.display.update()
print('bye')
