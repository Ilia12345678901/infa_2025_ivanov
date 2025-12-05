import pygame
import sys
import random

# Импорт функций из файла 'cats_functions2.py'
from cats_functions2 import (
    create_cat,
    move_cats,
    handle_collisions,
    handle_trap_input,
    adjust_fps,
    draw_trap,
    draw_cats,
    draw_hud,
    enforce_time_limit,
    update_screen,
)

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ловим кошек!")
start_FPS=60
FPS=start_FPS
# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
game_color = [WHITE, RED, BLUE, YELLOW]
cats_ = ['cat.jpeg', 'cat1.jpeg', 'cat3.jpeg', 'cat4.jpeg']
# Настройки ловушки (рамки)
frame_width = 100
frame_height = 20
frame_x = screen_width // 2 - frame_width // 2
frame_y = screen_height - 50
frame_speed = 5

# Настройки кошек
cat_width = 60
cat_height = 60
cats = []  # Теперь будет список словарей: {'square': pygame.Rect, 'h_speed': горизонтальная скорость}
cat_speed_y = 3  # Вертикальная скорость
cat_speed_h_range = (-3, 3)  # Диапазон горизонтальной скорости
spawn_rate = 1000  # мс между появлениями кошек
last_spawn = pygame.time.get_ticks()

cat_image_bad = 'cat4.jpeg'

# Счётчик баллов
score = 0
font = pygame.font.SysFont(None, 25)

# Часы для контроля FPS
clock = pygame.time.Clock()

# Для органичения по времени
t=0
limit=60

# Функции вынесены в файл 'cats_functions2.py' и импортируются выше.


# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление ловушкой (рамкой) и ее движение
    keys = pygame.key.get_pressed()
    frame_x = handle_trap_input(keys, frame_x, frame_speed, frame_width, screen_width)

    # Изменение FPS
    FPS = adjust_fps(keys, FPS, min_fps=1)

    # Изменение множителя
    multiplier = FPS / start_FPS

    # Создание новых кошек
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn > spawn_rate:
        cats.append(create_cat(screen_width, cat_width, cat_height, cat_speed_h_range, game_color, cats_))
        last_spawn = current_time

    # Движение кошек и удаление кошек, вышедших за нижнюю границу экрана
    cats = move_cats(cats, cat_speed_y, screen_width, screen_height)

    # Проверка столкновений (поймали кошку?)
    frame_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
    cats, delta = handle_collisions(cats, frame_rect, cat_image_bad, multiplier, RED)
    score += delta

    # Очистка экрана
    screen.fill(BLACK)

    # Рисование элементов
    # Ловушка (рамка)
    draw_trap(screen, frame_x, frame_y, frame_width, frame_height, BLUE)
    # Кошки
    draw_cats(screen, cats, WHITE)
    
    # Отображение текста
    draw_hud(screen, font, score, multiplier, t, limit, cats, screen_width, WHITE, RED)

    # Ограничение по времени
    enforce_time_limit(t, limit)
    
    # Обновление экрана
    t = update_screen(screen, clock, FPS, t) 

# Завершение Pygame
pygame.quit()
sys.exit()