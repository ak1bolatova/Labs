import pygame, sys, random, time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Window dimensions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
CELL_SIZE = 20  # Size of each cell in the grid

# Grid dimensions based on window size and cell size
COLS = WINDOW_WIDTH // CELL_SIZE
ROWS = WINDOW_HEIGHT // CELL_SIZE

# Color definitions
BLACK = (0, 0, 0)       # Background
WHITE = (255, 255, 255) # Text
GREEN = (0, 255, 0)     # Snake
RED = (255, 0, 0)       # Regular food (10 points)
BLUE = (0, 0, 255)      # Premium food (20 points)
YELLOW = (255, 255, 0)  # Special food (30 points)

# Create game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()  # For controlling game speed

def generate_food(snake_body):
    """
    Generates food at random position that doesn't overlap with snake.
    Also assigns random type and expiration time to the food.
    
    Args:
        snake_body: List of (x,y) tuples representing snake segments
        
    Returns:
        Tuple containing (x, y, color, point_value, expiration_time)
    """
    while True:
        # Random position in grid
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        
        # Check if position is not occupied by snake
        if (x, y) not in snake_body:
            # Randomly choose food type with different colors and point values
            food_type = random.choice([
                (RED, 10),    # Regular food - 10 points
                (BLUE, 20),   # Premium food - 20 points
                (YELLOW, 30) # Special food - 30 points
            ])
            
            # Add random expiration time (5-10 seconds from now)
            expiration_time = time.time() + random.randint(5, 10)
            
            return (x, y, food_type[0], food_type[1], expiration_time)

# Initialize snake - starts in center of screen
snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)  # Initial direction - right

# Generate first food item
food = generate_food(snake)

# Game parameters
score = 0       # Player's score
level = 1       # Current level
foods_eaten = 0 # Count of foods eaten
speed = 6       # Game speed (frames per second)
running = True  # Game state

# Main game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            # Change direction based on key press
            # Prevent 180-degree turns
            if event.key == K_UP and direction != (0, 1):
                direction = (0, -1)
            elif event.key == K_DOWN and direction != (0, -1):
                direction = (0, 1)
            elif event.key == K_LEFT and direction != (1, 0):
                direction = (-1, 0)
            elif event.key == K_RIGHT and direction != (-1, 0):
                direction = (1, 0)

    # Move snake by creating new head position
    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    # Check for game over conditions
    if (new_head[0] < 0 or new_head[0] >= COLS or  # Hit left/right wall
        new_head[1] < 0 or new_head[1] >= ROWS or # Hit top/bottom wall
        new_head in snake):                        # Hit itself
        running = False

    # Add new head to snake
    snake.insert(0, new_head)

    # Check if current food has expired
    if time.time() > food[4]:  # Current time > expiration time
        food = generate_food(snake)  # Generate new food

    # Check if snake ate food
    if new_head[:2] == food[:2]:
        # Add food's point value to score
        score += food[3]  
        foods_eaten += 1
        
        # Generate new food
        food = generate_food(snake)  
        
        # Level up every 3 foods eaten
        if foods_eaten % 3 == 0:  
            level += 1
            speed += 2  # Increase game speed
    else:
        # Remove tail if no food was eaten
        snake.pop()  

    # Draw background
    screen.fill(BLACK)

    # Draw food (with its assigned color)
    food_rect = pygame.Rect(
        food[0] * CELL_SIZE, 
        food[1] * CELL_SIZE, 
        CELL_SIZE, 
        CELL_SIZE
    )
    pygame.draw.rect(screen, food[2], food_rect)  

    # Draw snake
    for segment in snake:
        seg_rect = pygame.Rect(
            segment[0] * CELL_SIZE, 
            segment[1] * CELL_SIZE, 
            CELL_SIZE, 
            CELL_SIZE
        )
        pygame.draw.rect(screen, GREEN, seg_rect)

    # Display score and level
    info_text = pygame.font.SysFont("Verdana", 20).render(
        f"Score: {score}  Level: {level}", 
        True, 
        WHITE
    )
    screen.blit(info_text, (10, 10))

    # Update display
    pygame.display.update()
    
    # Control game speed
    clock.tick(speed)

# Clean up pygame
pygame.quit()
sys.exit()