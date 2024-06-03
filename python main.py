# Pygame Project
# Lucas Zhang

import pygame
import random
# Initialize Pygame
pygame.init()
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Basket dimensions
BASKET_WIDTH = 100
BASKET_HEIGHT = 20
# Star dimensions
STAR_WIDTH = 20
STAR_HEIGHT = 20
# Game settings
STAR_FALL_SPEED = 5
BASKET_SPEED = 10
LIVES = 3
# Fonts
FONT = pygame.font.SysFont(None, 36)
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")
# Basket class
class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BASKET_WIDTH, BASKET_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - BASKET_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - BASKET_HEIGHT - 10
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= BASKET_SPEED
        if keys[pygame.K_RIGHT] and self.rect.x < SCREEN_WIDTH - BASKET_WIDTH:
            self.rect.x += BASKET_SPEED
# Star class
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((STAR_WIDTH, STAR_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - STAR_WIDTH)
        self.rect.y = -STAR_HEIGHT
    def update(self):
        self.rect.y += STAR_FALL_SPEED
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
# Function to draw text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    basket = Basket()
    all_sprites = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    all_sprites.add(basket)
    score = 0
    lives = LIVES
    star_event = pygame.USEREVENT + 1
    pygame.time.set_timer(star_event, 1000)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == star_event:
                star = Star()
                all_sprites.add(star)
                stars.add(star)
        all_sprites.update()
        # Check for collisions
        hits = pygame.sprite.spritecollide(basket, stars, True)
        if hits:
            score += len(hits)
        # Check for missed stars
        for star in stars:
            if star.rect.y > SCREEN_HEIGHT:
                lives -= 1
                star.kill()
                if lives == 0:
                    running = False
        # Clear the screen
        screen.fill(WHITE)
        # Draw all sprites
        all_sprites.draw(screen)
        # Draw score and lives
        draw_text(f"Score: {score}", FONT, BLACK, screen, 10, 10)
        draw_text(f"Lives: {lives}", FONT, BLACK, screen, 10, 50)
        # Flip the display
        pygame.display.flip()
        # Cap the frame rate
        clock.tick(60)
    # Game over
    screen.fill(WHITE)
    draw_text("GAME OVER", FONT, BLACK, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 20)
    draw_text(f"Final Score: {score}", FONT, BLACK, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
if __name__ == "__main__":
    main()