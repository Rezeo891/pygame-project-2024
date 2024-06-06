# Pygame Project - Survivor Game
# Lucas Zhang

import pygame
import random
import math

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

player_image = pygame.transform.scale(player_image, (50, 50))
player_image.set_colorkey(WHITE)
enemy_image = pygame.transform.scale(enemy_image, (50, 50))
enemy_image.set_colorkey(WHITE)
boss_image = pygame.transform.scale(enemy_image, (250, 250))
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
       self.health = 250

   def update(self):
       keys = pygame.key.get_pressed()
       if keys[pygame.K_a]:
           self.rect.x -= self.speed
       if keys[pygame.K_d]:
           self.rect.x += self.speed
       if keys[pygame.K_w]:
           self.rect.y -= self.speed
       if keys[pygame.K_s]:
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

# Bullet class
class Bullet(pygame.sprite.Sprite):
   def __init__(self, x, y, direction):
       super().__init__()
       self.image = pygame.Surface((10, 10))
       self.image.fill(WHITE)
       self.rect = self.image.get_rect()
       self.rect.center = (x, y)
       self.speed = 10
       self.direction = direction

   def update(self):
       if self.direction == 'up':
           self.rect.y -= self.speed
       elif self.direction == 'down':
           self.rect.y += self.speed
       elif self.direction == 'left':
           self.rect.x -= self.speed
       elif self.direction == 'right':
           self.rect.x += self.speed

       # Remove bullet if it goes off screen
       if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
           self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.x = random.choice([-30, SCREEN_WIDTH + 30])
        self.rect.y = random.choice([-30, SCREEN_HEIGHT + 30])
        self.speed = random.uniform(1, 3)
        self.health = 2  # Set enemy health

    def update(self):
        direction = pygame.math.Vector2(player.rect.centerx - self.rect.centerx,
                                        player.rect.centery - self.rect.centery)
        if direction.length() != 0:  # Check if the vector length is not zero
            direction = direction.normalize()
            self.rect.x += direction.x * self.speed
            self.rect.y += direction.y * self.speed

        # Avoid stacking
        for other in enemies:
            if other != self and pygame.sprite.collide_rect(self, other):
                self.avoid(other)

    def avoid(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        distance = math.sqrt(dx * dx + dy * dy)
        if distance == 0:
            distance = 0.1
        move_x = (dx / distance) * self.speed
        move_y = (dy / distance) * self.speed
        self.rect.x += move_x
        self.rect.y += move_y

# Boss class
class Boss(Enemy):
   def __init__(self):
       super().__init__()
       self.image = boss_image
       self.rect = self.image.get_rect()
       self.rect.x = random.choice([-60, SCREEN_WIDTH + 60])
       self.rect.y = random.choice([-60, SCREEN_HEIGHT + 60])
       self.speed = 4.5  # Set boss speed
       self.health = 50 # Set boss health

   def update(self):
       super().update()

# Function to display text
def draw_text(text, font, color, surface, x, y):
   textobj = font.render(text, True, color)
   textrect = textobj.get_rect()
   textrect.topleft = (x, y)
   surface.blit(textobj, textrect)

# Function to display game over screen
def game_over_screen():
   screen.fill(BLACK)
   font = pygame.font.Font(None, 74)
   draw_text('GAMEOVER', font, WHITE, screen, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 - 50)
   font = pygame.font.Font(None, 50)
   draw_text('Try Again', font, WHITE, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10)
   pygame.display.flip()

   waiting = True
   while waiting:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()
               if SCREEN_WIDTH // 2 - 100 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 100 and SCREEN_HEIGHT // 2 + 10 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 60:
                   waiting = False
                   main()

# Function to display congratulations screen
def congratulations_screen():
   screen.fill(BLACK)
   font = pygame.font.Font(None, 74)
   draw_text('CONGRATULATIONS', font, WHITE, screen, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50)
   font = pygame.font.Font(None, 50)
   draw_text('You Won!', font, WHITE, screen, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10)
   draw_text('Quit', font, WHITE, screen, SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 + 70)
   pygame.display.flip()

   waiting = True
   while waiting:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               exit()
           if event.type == pygame.MOUSEBUTTONDOWN:
               mouse_pos = pygame.mouse.get_pos()
               if SCREEN_WIDTH // 2 - 30 <= mouse_pos[0] <= SCREEN_WIDTH // 2 + 70 and SCREEN_HEIGHT // 2 + 70 <= mouse_pos[1] <= SCREEN_HEIGHT // 2 + 120:
                   pygame.quit()
                   exit()

# Main game function
def main():
   global all_sprites, enemies, bullets, player, score, boss_spawned, game_over

   # Sprite groups
   all_sprites = pygame.sprite.Group()
   enemies = pygame.sprite.Group()
   bullets = pygame.sprite.Group()
   player = Player()
   all_sprites.add(player)

   # Game variables
   score = 0
   boss_spawned = False
   game_over = False
   bullet_cooldown = 10  # Cooldown period in frames
   bullet_timer = 0
   boss_damage_cooldown = 30  # Cooldown period for boss damage to player
   boss_damage_timer = 0

   # Keep track of pressed keys
   key_state = {
       pygame.K_UP: False,
       pygame.K_DOWN: False,
       pygame.K_LEFT: False,
       pygame.K_RIGHT: False
   }

   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False
           elif event.type == pygame.KEYDOWN:
               if event.key in key_state:
                   key_state[event.key] = True
           elif event.type == pygame.KEYUP:
               if event.key in key_state:
                   key_state[event.key] = False

       # Shoot bullets based on key state and cooldown
       if bullet_timer == 0:
           if key_state[pygame.K_UP]:
               bullet = Bullet(player.rect.centerx, player.rect.centery, 'up')
               all_sprites.add(bullet)
               bullets.add(bullet)
           if key_state[pygame.K_DOWN]:
               bullet = Bullet(player.rect.centerx, player.rect.centery, 'down')
               all_sprites.add(bullet)
               bullets.add(bullet)
           if key_state[pygame.K_LEFT]:
               bullet = Bullet(player.rect.centerx, player.rect.centery, 'left')
               all_sprites.add(bullet)
               bullets.add(bullet)
           if key_state[pygame.K_RIGHT]:
               bullet = Bullet(player.rect.centerx, player.rect.centery, 'right')
               all_sprites.add(bullet)
               bullets.add(bullet)
           bullet_timer = bullet_cooldown
       else:
           bullet_timer -= 1

       # Spawn enemies
       if not boss_spawned and len(enemies) < 35:
           enemy = Enemy()
           all_sprites.add(enemy)
           enemies.add(enemy)


       if score >= 99 and not boss_spawned:
           boss = Boss()
           all_sprites.add(boss)
           enemies.add(boss)
           boss_spawned = True

       # Update all sprites
       all_sprites.update()

       # Check for collisions
       hits = pygame.sprite.spritecollide(player, enemies, False)
       for hit in hits:
           if isinstance(hit, Boss):
               if boss_damage_timer == 0:
                   player.health -= 10
                   boss_damage_timer = boss_damage_cooldown
           else:
               player.health -= 1
           if player.health <= 0:
               game_over = True
               running = False

       if boss_damage_timer > 0:
           boss_damage_timer -= 1

       bullet_hits = pygame.sprite.groupcollide(bullets, enemies, True, False)
       for bullet, hits in bullet_hits.items():
           for hit in hits:
               hit.health -= 1
               if hit.health <= 0:
                   hit.kill()
                   score += 1

       # Check if player wins
       if boss_spawned and not enemies:
           running = False
           congratulations_screen()

       # Clear the screen
       screen.fill(BLACK)

       # Draw the background image
       screen.blit(background_image, (0, 0))

       # Draw all sprites
       all_sprites.draw(screen)

       # Draw the score and player's lives
       font = pygame.font.Font(None, 36)
       draw_text(f"Score: {score}", font, WHITE, screen, 10, 10)
       draw_text(f"Lives: {player.health}", font, WHITE, screen, 10, 50)

       # Flip the display
       pygame.display.flip()

       # Cap the frame rate
       clock.tick(60)

   if game_over:
       game_over_screen()

# Run the game
main()
pygame.quit()