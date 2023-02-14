import pygame

def display_score(screen: pygame.Surface, start_time: int, pixel_font: pygame.font.Font):
    current_score = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = pixel_font.render(f"{current_score}", False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(400, 50))
    screen.blit(score_surface, score_rect)

def collision_sprite(player_group: pygame.sprite.GroupSingle, enemy_group: pygame.sprite.Group) -> bool:
    if pygame.sprite.spritecollide(player_group.sprite, enemy_group, False):
        enemy_group.empty()
        player_group.empty()
        return True
    return False
