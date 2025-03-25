import pygame

pygame.init()

screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Red Ball")

x = 400 // 2
y = 400 // 2
speed = 20

running = True
while running:

    pygame.time.delay(60)
    
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x - 20 - 25 >= 0:
        x -= speed
    elif keys[pygame.K_RIGHT] and x + 20 + 25 <= 400:
        x += speed
    elif keys[pygame.K_UP] and y - 20 - 25 >= 0:
        y -= speed
    elif keys[pygame.K_DOWN] and y + 20 + 25 <= 400:
        y += speed
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type  == pygame.KEYDOWN:
    #         if event.key == pygame.K_LEFT and x - 25 - 20 >= 0:
    #             x -= speed
    #         elif event.key == pygame.K_RIGHT and x + 25 + 20 <= 400:
    #             x += speed
    #         elif event.key == pygame.K_UP and y - 25 - 20 >= 0:
    #             y -= speed
    #         elif event.key == pygame.K_DOWN and y + 25 + 20 <= 400:
    #             y += speed

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 25)
    pygame.display.update()
