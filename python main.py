# Pygame Project - Survivor Game
# Lucas Zhang

import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Survivor Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Load images
player_image = pygame.image.load('./images/player.png')
enemy_image = pygame.image.load('./images/enemy.jpg')
boss_image = pygame.image.load('./images/enemy.jpg')
background_image = pygame.image.load('./images/background.jpg')

player_image = pygame.transform.scale(player_image,(50,50))
player_image.set_colorkey(WHITE)
enemy_image = pygame.transform.scale(enemy_image,(50,50))
enemy_image.set_colorkey(WHITE)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5
        self.health = 10

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-30, SCREEN_WIDTH + 30])
        self.rect.y = random.choice([-30, SCREEN_HEIGHT + 30])
        self.speed = random.uniform(1, 3)

    def update(self):
        direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                        player.rect.centery - self.rect.centery)
        direction = direction.normalize()
        self.rect.x += direction.x * self.speed
        self.rect.y += direction.y * self.speed

# Boss class
class Boss(Enemy):
    def __init__(self):
        super().__init__()
        self.image = boss_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-60, SCREEN_WIDTH + 60])
        self.rect.y = random.choice([-60, SCREEN_HEIGHT + 60])
        self.speed = 2
        self.health = 20

    def update(self):
        super().update()

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Game variables
wave = 1
enemies_spawned = 0
boss_spawned = False
game_over = False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn enemies
    if not boss_spawned:
        if enemies_spawned < wave * 5:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemies_spawned += 1
        elif len(enemies) == 0:
            boss = Boss()
            all_sprites.add(boss)
            enemies.add(boss)
            boss_spawned = True

    # Update all sprites
    all_sprites.update()

    # Check for collisions
    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 1
        if player.health <= 0:
            game_over = True
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Draw all sprites
    all_sprites.draw(screen)

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
