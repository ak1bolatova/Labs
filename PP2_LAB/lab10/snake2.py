import pygame, sys, random, time, psycopg2
from pygame.locals import *

# ------------------ DATABASE SETUP ------------------
conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="2955492Frybtn"
)
cur = conn.cursor()
def get_top_scores():
    cur.execute("""
        SELECT u.username, us.level, us.score, us.saved_at
        FROM user_score us
        JOIN users u ON us.user_id = u.id
        ORDER BY us.score DESC
        LIMIT 5;
    """)
    return cur.fetchall()

def get_user_and_level(username):
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    user = cur.fetchone()

    if user is None:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        level = 1
    else:
        user_id = user[0]
        cur.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1;", (user_id,))
        last_save = cur.fetchone()
        level = last_save[0] if last_save else 1

    conn.commit()
    return user_id, level

def save_score(user_id, level, score):
    cur.execute("INSERT INTO user_score (user_id, level, score) VALUES (%s, %s, %s);",
                (user_id, level, score))
    conn.commit()

# ----------------------------------------------------

# Initialize pygame
pygame.init()
pygame.mixer.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 400, 400
CELL_SIZE = 20
COLS, ROWS = WINDOW_WIDTH // CELL_SIZE, WINDOW_HEIGHT // CELL_SIZE
BLACK, WHITE, GREEN, RED, BLUE, YELLOW = (0,0,0), (255,255,255), (0,255,0), (255,0,0), (0,0,255), (255,255,0)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)
input_box = pygame.Rect(100, 150, 200, 40)
play_button = pygame.Rect(150, 220, 100, 40)
username = ""
entering_name = True

while entering_name:
    screen.fill(BLACK)
    txt_surface = font.render(username, True, WHITE)
    pygame.draw.rect(screen, WHITE, input_box, 2)
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

    pygame.draw.rect(screen, GREEN, play_button)
    play_text = font.render("Play", True, RED)
    screen.blit(play_text, (play_button.x + 20, play_button.y + 5))
    top_scores = get_top_scores()

    # Отображаем таблицу с рекордами
    y_offset = 280
    screen.blit(font.render("Top Scores:", True, WHITE), (120, y_offset))
    y_offset += 30
    for name, lvl, scr, date in top_scores:
        text = f"{name} | Level: {lvl} | Score: {scr}"
        screen.blit(font.render(text, True, WHITE), (50, y_offset))
        y_offset += 25

    pygame.display.flip()
 

    

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_RETURN:
                if username:
                    entering_name = False
            elif event.key == K_BACKSPACE:
                username = username[:-1]
            else:
                username += event.unicode
        elif event.type == MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos) and username:
                entering_name = False

# Load user
user_id, level = get_user_and_level(username)

snake = [(COLS // 2, ROWS // 2)]
direction = (1, 0)

def generate_food(snake_body):
    while True:
        x, y = random.randint(0, COLS-1), random.randint(0, ROWS-1)
        if (x, y) not in snake_body:
            color, points = random.choice([(RED, 10), (BLUE, 20), (YELLOW, 30)])
            expiration_time = time.time() + random.randint(5, 10)
            return (x, y, color, points, expiration_time)

food = generate_food(snake)
score, foods_eaten = 0, 0
speed = 6 + (level - 1) * 2
running, paused = True, False

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_p:
                paused = not paused
                if paused:
                    save_score(user_id, level, score)
                    print("Game paused. Progress saved.")
            if event.key == K_UP and direction != (0, 1): direction = (0, -1)
            elif event.key == K_DOWN and direction != (0, -1): direction = (0, 1)
            elif event.key == K_LEFT and direction != (1, 0): direction = (-1, 0)
            elif event.key == K_RIGHT and direction != (-1, 0): direction = (1, 0)

    if paused:
        continue

    head_x, head_y = snake[0]
    new_head = (head_x + direction[0], head_y + direction[1])

    if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS or new_head in snake:
        print("Game over!")
        save_score(user_id, level, score)
        break

    snake.insert(0, new_head)

    if time.time() > food[4]:
        food = generate_food(snake)

    if new_head[:2] == food[:2]:
        score += food[3]
        foods_eaten += 1
        food = generate_food(snake)
        if foods_eaten % 3 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    screen.fill(BLACK)
    pygame.draw.rect(screen, food[2], pygame.Rect(food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    info = font.render(f"Score: {score} Level: {level}", True, WHITE)
    screen.blit(info, (10, 10))
    pygame.display.update()
    clock.tick(speed)

pygame.quit()
cur.close()
conn.close()
sys.exit()
