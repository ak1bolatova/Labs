import pygame
import os

# Инициализация pygame
pygame.init()
pygame.mixer.init()

# Папка с музыкой
MUSIC_FOLDER = "C:Users/bolat/OneDrive/Desktop/PP2_LAB/lab7"  # Укажите папку с вашими треками
tracks = [f for f in os.listdir("C:Users/bolat/OneDrive/Desktop/PP2_LAB/lab7") if f.endswith(".mp3")]

# Проверяем, есть ли файлы
if not tracks:
    print("Нет музыкальных файлов в папке!")
    exit()

current_track = 0

def play_music():
    pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, tracks[current_track]))
    pygame.mixer.music.play()
    print(f"Играет: {tracks[current_track]}")

def next_track():
    global current_track
    current_track = (current_track + 1) % len(tracks)
    play_music()

def prev_track():
    global current_track
    current_track = (current_track - 1) % len(tracks)
    play_music()

def toggle_pause():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        print("Пауза")
    else:
        pygame.mixer.music.unpause()
        print("Продолжаем")

def stop_music():
    pygame.mixer.music.stop()
    print("Остановлено")

# Запускаем первый трек
play_music()

# Основной цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                toggle_pause()
            elif event.key == pygame.K_s:
                stop_music()
            elif event.key == pygame.K_n:
                next_track()
            elif event.key == pygame.K_b:
                prev_track()

pygame.quit()
