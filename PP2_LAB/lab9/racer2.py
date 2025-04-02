import pygame
import sys
import time
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Colors
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)
BLUE = pygame.Color(0, 0, 255)
WHITE = pygame.Color(255, 255, 255)
YELLOW = pygame.Color(255, 255, 0)

# Game settings
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
INITIAL_SPEED = 5
SPEED_INCREMENT = 1  # How much to increase speed when threshold is reached
COIN_THRESHOLD = 5  # Number of coins to collect before speed increases

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(WHITE)
pygame.display.set_caption('Enhanced Car Game')
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over_text = font_large.render("Game Over", True, BLACK)

class Enemy(pygame.sprite.Sprite):
    """Enemy car that moves down the screen"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(RED)  # Placeholder for enemy.png
        self.rect = self.image.get_rect()
        self.reset_position()
        
    def reset_position(self):
        """Reset enemy to top of screen at random x position"""
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
    def move(self, speed):
        """Move enemy down the screen at given speed"""
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()

class Player(pygame.sprite.Sprite):
    """Player controlled car"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 80))
        self.image.fill(BLUE)  # Placeholder for player.png
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
        
    def move(self):
        """Move player based on keyboard input"""
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    """Collectible coins with different weights/values"""
    def __init__(self):
        super().__init__()
        
        # Randomly assign coin value (weight)
        self.value = random.choice([1, 2, 3])  # 3 types of coins
        
        # Create different colored coins based on value
        if self.value == 1:
            color = YELLOW  # Standard coin
            size = 30
        elif self.value == 2:
            color = GREEN  # More valuable
            size = 25
        else:
            color = BLUE  # Most valuable
            size = 20
            
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(30, SCREEN_WIDTH - 30), 0)
        
    def move(self):
        """Move coin down the screen"""
        self.rect.move_ip(0, 5)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def game_over(score):
    """Display game over screen with final score"""
    screen.fill(RED)
    
    # Game Over text
    game_over_surface = font_large.render("Game Over", True, WHITE)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    screen.blit(game_over_surface, game_over_rect)
    
    # Score text
    score_surface = font_small.render(f'Final Score: {score}', True, WHITE)
    score_rect = score_surface.get_rect()
    score_rect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    screen.blit(score_surface, score_rect)
    
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    sys.exit()

def main():
    """Main game loop"""
    # Create player and enemy
    player = Player()
    enemy = Enemy()
    
    # Create sprite groups
    enemies = pygame.sprite.Group(enemy)
    all_sprites = pygame.sprite.Group(player, enemy)
    coins = pygame.sprite.Group()
    
    # Game variables
    score = 0
    coins_collected = 0
    speed = INITIAL_SPEED
    
    # Custom events
    INC_SPEED = pygame.USEREVENT + 1
    SPAWN_COIN = pygame.USEREVENT + 2
    
    # Set timers for events
    pygame.time.set_timer(INC_SPEED, 1000)  # Check speed increase every second
    pygame.time.set_timer(SPAWN_COIN, 1000)  # Spawn new coin every second
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # Check if we should increase enemy speed
            if event.type == INC_SPEED and coins_collected >= COIN_THRESHOLD:
                speed += SPEED_INCREMENT
                coins_collected = 0  # Reset counter after speed increase
                print(f"Speed increased to {speed}")  # Debug output
            
            # Spawn new coin if less than 3 on screen
            if event.type == SPAWN_COIN and len(coins) < 3:
                new_coin = Coin()
                coins.add(new_coin)
                all_sprites.add(new_coin)
        
        # Clear screen
        screen.fill(WHITE)
        
        # Display current score
        score_surface = font_small.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surface, (10, 10))
        
        # Display current speed
        speed_surface = font_small.render(f'Speed: {speed}', True, BLACK)
        screen.blit(speed_surface, (10, 40))
        
        # Move and draw all sprites
        for entity in all_sprites:
            if isinstance(entity, Enemy):
                entity.move(speed)
            elif isinstance(entity, Coin):
                entity.move()
            else:
                entity.move()
            screen.blit(entity.image, entity.rect)
        
        # Check for coin collection
        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            score += coin.value
            coins_collected += 1
           
        
        # Check for collisions with enemies
        if pygame.sprite.spritecollideany(player, enemies):
            
            game_over(score)
        
        pygame.display.update()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()