import pygame
import time
from pygame.locals import *

pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

# Load images
mickey = pygame.image.load("C:/Users/bolat/OneDrive/Desktop/PP2_LAB/lab7/clock.png")
minute_hand = pygame.image.load("C:/Users/bolat/OneDrive/Desktop/PP2_LAB/lab7/rightarm.png")
second_hand = pygame.image.load("C:/Users/bolat/OneDrive/Desktop/PP2_LAB/lab7/leftarm.png")

# Resize images
mickey = pygame.transform.scale(mickey, (600, 500))
minute_hand = pygame.transform.scale(minute_hand, (680, 680))
second_hand = pygame.transform.scale(second_hand, (63, 480))

# Clock center
clock_x, clock_y = WIDTH // 2, HEIGHT // 2

# Colors
WHITE = (255, 255, 255)

running = True
while running:
    screen.fill(WHITE)
    
    # Get system time
    t = time.localtime()
    sec_angle = -6 * t.tm_sec  # 360 degrees / 60 seconds
    min_angle = -6 * t.tm_min  # 360 degrees / 60 minutes
    
    # Rotate hands
    rotated_minute = pygame.transform.rotate(minute_hand, min_angle)
    rotated_second = pygame.transform.rotate(second_hand, sec_angle)
    
    # Get rects for positioning
    mickey_rect = mickey.get_rect(center=(clock_x, clock_y))
    minute_rect = rotated_minute.get_rect(center=(clock_x, clock_y))
    second_rect = rotated_second.get_rect(center=(clock_x, clock_y))
    
    # Draw clock
    screen.blit(mickey, mickey_rect.topleft)
    screen.blit(rotated_minute, minute_rect.topleft)
    screen.blit(rotated_second, second_rect.topleft)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()