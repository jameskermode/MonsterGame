import asyncio
import pygame
import random
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Monster Hunter")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
BLACK = (0, 0, 0)
player_size = 50
player_pos = [WIDTH // 2, HEIGHT - player_size]
player_speed = 5
player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
health = 3  # Player health

# Virtual buttons for touchscreen
button_left = pygame.Rect(20, HEIGHT - 70, 60, 50)
button_right = pygame.Rect(100, HEIGHT - 70, 60, 50)
button_shoot = pygame.Rect(WIDTH - 80, HEIGHT - 70, 60, 50)

# Bullet
bullet_size = 5
bullets = []
bullet_speed = 14
ammo = 100

# Monster
monster_size = 50
monsters = []
monster_speed = 2
spawn_delay = 1000  # milliseconds
last_spawn_time = pygame.time.get_ticks()

# Load monster image
monster_image = pygame.image.load(os.path.join("assets", "monster.png")).convert_alpha()
monster_image = pygame.transform.scale(monster_image, (monster_size, monster_size))


player_image = pygame.image.load(os.path.join("assets", "player.png")).convert_alpha()
player_image = pygame.transform.scale(player_image, (player_size, player_size))

# Score
score = 0
font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()


def spawn_monster():
    x = random.randint(0, WIDTH - monster_size)
    y = -monster_size
    monsters.append(pygame.Rect(x, y, monster_size, monster_size))


def draw_window():
    screen.fill(WHITE)

    # Draw player
    screen.blit(player_image, player_rect)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, RED, bullet)

    # Draw monsters
    for monster in monsters:
        screen.blit(monster_image, monster)

    # Draw score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Draw health
    health_text = font.render(f"Health: {health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 50))

    # Draw ammo
    ammo_text = font.render(f"Ammo: {ammo}", True, (0, 0, 0))
    screen.blit(ammo_text, (10, 90))

    # Left button
    pygame.draw.rect(screen, (180, 180, 180), button_left)
    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (30, HEIGHT - 45),  # Tip of arrow
            (60, HEIGHT - 70),  # Top rear
            (60, HEIGHT - 20),  # Bottom rear
        ],
    )

    # Right button
    pygame.draw.rect(screen, (180, 180, 180), button_right)
    pygame.draw.polygon(
        screen,
        BLACK,
        [
            (140, HEIGHT - 45),  # Tip of arrow (right side)
            (110, HEIGHT - 70),  # Top rear
            (110, HEIGHT - 20),  # Bottom rear
        ],
    )
    pygame.draw.rect(screen, (200, 100, 100), button_shoot)
    shoot_text = font.render("FIRE", True, WHITE)
    screen.blit(shoot_text, (WIDTH - 75, HEIGHT - 55))

    pygame.display.update()


async def main():
    global score, health, last_spawn_time, ammo
    running = True

    while running:
        clock.tick(60)  # Limit to 60 FPS

        # Input flags
        move_left = move_right = shoot = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                pos = pygame.mouse.get_pos()
                if button_left.collidepoint(pos):
                    move_left = True
                if button_right.collidepoint(pos):
                    move_right = True
                if button_shoot.collidepoint(pos):
                    shoot = True

        # Apply movement
        if move_left and player_rect.left > 0:
            player_rect.x -= player_speed
        if move_right and player_rect.right < WIDTH:
            player_rect.x += player_speed
        if shoot:
            bullet = pygame.Rect(
                player_rect.centerx - bullet_size // 2, player_rect.top, bullet_size, 10
            )
            bullets.append(bullet)
            ammo -= 1

        # Player movement
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT] and player_rect.left > 0:
        #     player_rect.x -= player_speed
        # if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
        #     player_rect.x += player_speed
        # if keys[pygame.K_SPACE] and ammo > 0:
        #     bullet = pygame.Rect(player_rect.centerx - bullet_size//2, player_rect.top, bullet_size, 10)
        #     bullets.append(bullet)
        #     ammo -= 1

        # Move bullets
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn monsters
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > spawn_delay:
            spawn_monster()
            last_spawn_time = current_time

        # Move monsters
        for monster in monsters[:]:
            monster.y += monster_speed
            if monster.y > HEIGHT:
                monsters.remove(monster)
            elif monster.colliderect(player_rect):
                health -= 1
                monsters.remove(monster)
                if health <= 0:
                    print("Game Over!")
                    running = False

        # Check collisions
        for bullet in bullets[:]:
            for monster in monsters[:]:
                if bullet.colliderect(monster):
                    bullets.remove(bullet)
                    monsters.remove(monster)
                    ammo += 10
                    score += 1
                    break

        draw_window()
        await asyncio.sleep(0)


asyncio.run(main())
