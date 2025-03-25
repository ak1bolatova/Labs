import pygame

x = 800
y = 600
fps = 60
timer = pygame.time.Clock()

screen = pygame.display.set_mode([x, y])
pygame.display.set_caption('Paint')

def draw_menu():
    pygame.draw.rect(screen, 'gray', [0, 0, x, 70])

running = True
while running:
    timer.tick(fps)
    screen.fill('white')

    draw_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()



