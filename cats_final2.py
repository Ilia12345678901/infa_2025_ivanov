import pygame
import sys
import random

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
cat_width = 30
cat_height = 30
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
#для органичения по времени
t=0
limit=60


# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление ловушкой (рамкой) с помощью стрелок
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and frame_x > 0:
        frame_x -= frame_speed
    if keys[pygame.K_RIGHT] and frame_x < screen_width - frame_width:
        frame_x += frame_speed
    if keys[pygame.K_DOWN]: #Уменьшаем частоту
               if FPS>1:
                  FPS = FPS-1

    if keys[pygame.K_UP]:   #Увеличиваем частоту           
                  FPS = FPS+1
    multiplier=FPS/start_FPS              


    # Создание новых кошек
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn > spawn_rate:
        cat_x = random.randint(0, screen_width - cat_width)
        cat_y = 0
        # Случайная горизонтальная скорость в заданном диапазоне
        h_speed = random.uniform(cat_speed_h_range[0], cat_speed_h_range[1])
        cat_color = random.choice(game_color)
        cat_type = random.choice(cats_)
        try:
             cat_image = pygame.image.load(cat_type)
             cat_image = pygame.transform.scale(cat_image, (cat_width, cat_height))
        except:
             cat_image = None 
             cat_type = None
        cats.append({
            'square': pygame.Rect(cat_x, cat_y, cat_width, cat_height),
            'h_speed': h_speed,
            'cat_color' : cat_color,
            'cat_image' : cat_image,
            'cat_type' : cat_type
        })
        last_spawn = current_time

    # Движение кошек
    for cat in cats[:]:  
        # Движение по вертикали
        cat['square'].y += cat_speed_y
        
        # Движение по горизонтали
        cat['square'].x += cat['h_speed']
        
        # Отскок от краёв экрана
        if cat['square'].x + cat['square'].width >= screen_width:
            cat['square'].x = screen_width - cat['square'].width
            cat['h_speed'] = - cat['h_speed']
        if cat['square'].x <= 0 :
            cat['square'].x = 0
            cat['h_speed'] = - cat['h_speed']
    
    # Удаление кошек, улетевших за экран
    cats = [cat for cat in cats if cat['square'].y < screen_height]

    # Проверка столкновений (поймали кошку?)
    for cat in cats[:]: 
        if cat['cat_image'] != None :
             if cat['square'].colliderect(pygame.Rect(frame_x, frame_y, frame_width, frame_height)) and cat['cat_type'] != cat_image_bad:
                 cats.remove(cat)
                 score += 10*multiplier  # Добавляем баллы за пойманную кошку
             elif cat['square'].colliderect(pygame.Rect(frame_x, frame_y, frame_width, frame_height)) and cat['cat_type'] == cat_image_bad :
                 cats.remove(cat)
                 score -= 10*multiplier #Отнимаем баллы за карсный квадрат и первую кошку
        elif cat['cat_image'] == None :
             if cat['square'].colliderect(pygame.Rect(frame_x, frame_y, frame_width, frame_height)) and cat['cat_color'] != RED :
                 cats.remove(cat)
                 score += 10*multiplier #Отнимаем баллы за карсный квадрат и первую кошку
             elif cat['square'].colliderect(pygame.Rect(frame_x, frame_y, frame_width, frame_height)) and cat['cat_color'] == RED :
                 cats.remove(cat)
                 score -= 10*multiplier #Отнимаем баллы за карсный квадрат и первую кошку
    # Очистка экрана
    screen.fill(BLACK)

    # Рисование элементов
    # Ловушка (рамка)
    pygame.draw.rect(screen, BLUE, (frame_x, frame_y, frame_width, frame_height), 3)
    # Кошки
    for cat in cats:
        if cat_image:
            screen.blit(cat['cat_image'], cat['square'])  # Рисуем изображение кошки
        else:
            pygame.draw.rect(screen, cat['cat_color'] , cat['square'])  # Рисуем прямоугольник
    
    # Отображение времени
    if cats:
        info_text = font.render(f"Время: {int(60-t//1)}", True, WHITE)
        screen.blit(info_text, (10, 60))
    
    # Счёт
    score_text = font.render(f"Счёт: {int(score//1)}", True, WHITE)
    screen.blit(score_text, (10, 20))
    # Множитель
    multiplier_text = font.render(f"Множитель: x {round(multiplier,2)}", True, WHITE)
    screen.blit(multiplier_text, (10, 40))
    # Инструкция по управлению ловушкой
    control_text1 = font.render("Движение ловушки: влево/вправо", True, WHITE)
    screen.blit(control_text1, (screen_width-300, 20))
    
    # Инструкция по изменению FPS
    control_text2 = font.render("Изменение FPS: вверх/вниз ", True, WHITE)
    screen.blit(control_text2, (screen_width-300, 40))
    # Информация про красные шарики
    control_text3 = font.render("Злые кошки отнимают очки!", True, RED)
    screen.blit(control_text3, (screen_width - 300, 80))
    control_text3 = font.render("Красные квадраты отнимают очки!", True, RED)
    screen.blit(control_text3, (screen_width - 300, 60))
   #Ограничение по времени
    if t>limit:
      pygame.quit()
      sys.exit()
    
         

    # Обновление экрана
    pygame.display.flip()
    t=t+1/FPS
    clock.tick(FPS)  # 60 FPS

# Завершение Pygame
pygame.quit()
sys.exit()