import pygame
import sys
import random


def create_cat(screen_width, cat_width, cat_height, cat_speed_h_range, game_color, cats_):
    """Создаёт и возвращает словарь, описывающий новую кошку"""
    cat_x = random.randint(0, screen_width - cat_width)
    cat_y = 0
    h_speed = random.uniform(cat_speed_h_range[0], cat_speed_h_range[1])
    cat_color = random.choice(game_color)
    cat_type = random.choice(cats_)
    try:
        cat_image = pygame.image.load(cat_type)
        cat_image = pygame.transform.scale(cat_image, (cat_width, cat_height))
    except Exception:
        cat_image = None
        cat_type = None

    return {
        'square': pygame.Rect(cat_x, cat_y, cat_width, cat_height),
        'h_speed': h_speed,
        'cat_color': cat_color,
        'cat_image': cat_image,
        'cat_type': cat_type
    }


def move_cats(cats, speed_y, screen_w, screen_h):
    """Обновляет позиции кошек, обрабатывает отскоки по горизонтали и удаляет
    кошек, вышедших за нижнюю границу экрана"""
    for cat in cats[:]:
        cat['square'].y += speed_y
        cat['square'].x += cat['h_speed']

        # Отскок от краёв экрана
        if cat['square'].x + cat['square'].width >= screen_w:
            cat['square'].x = screen_w - cat['square'].width
            cat['h_speed'] = -cat['h_speed']
        if cat['square'].x <= 0:
            cat['square'].x = 0
            cat['h_speed'] = -cat['h_speed']

    return [cat for cat in cats if cat['square'].y < screen_h]


def handle_collisions(cats, frame_rect, bad_type, multiplier, red_color):
    """Обрабатывает столкновения кошек с ловушкой (рамкой)

    Возвращает (cats, score_delta)"""
    score_delta = 0
    for cat in cats[:]:
        if cat['cat_image'] is not None:
            if cat['square'].colliderect(frame_rect):
                cats.remove(cat)
                if cat['cat_type'] != bad_type:
                    score_delta += 10 * multiplier
                else:
                    score_delta -= 10 * multiplier
        else:
            if cat['square'].colliderect(frame_rect):
                cats.remove(cat)
                if cat['cat_color'] != red_color:
                    score_delta += 10 * multiplier
                else:
                    score_delta -= 10 * multiplier

    return cats, score_delta


def handle_trap_input(keys, frame_x, frame_speed, frame_width, screen_width):
    """Обновляет позицию рамки ловушки (frame_x)

    Возвращает новое значение frame_x"""
    if keys[pygame.K_LEFT] and frame_x > 0:
        frame_x -= frame_speed
    if keys[pygame.K_RIGHT] and frame_x < screen_width - frame_width:
        frame_x += frame_speed
    return frame_x


def adjust_fps(keys, FPS, min_fps=1):
    """Обновляет FPS
    
    Возвращает новое значение FPS"""
    if keys[pygame.K_DOWN]:
        if FPS > min_fps:
            FPS -= 1
    if keys[pygame.K_UP]:
        FPS += 1
    return FPS


def draw_trap(surface, frame_x, frame_y, frame_width, frame_height, color):
    pygame.draw.rect(surface, color, (frame_x, frame_y, frame_width, frame_height), 3)


def draw_cats(surface, cats_list, default_color):
    """Рисует кошек"""
    for cat in cats_list:
        if cat.get('cat_image') is not None:
            surface.blit(cat['cat_image'], cat['square'])
        else:
            pygame.draw.rect(surface, cat.get('cat_color', default_color), cat['square'])


def draw_hud(surface, font, score, multiplier, t, limit, cats_list, screen_w, white_color, red_color):
    """Отображает текст"""
    if cats_list:
        info_text = font.render(f"Время: {int(limit - t//1)}", True, white_color)
        surface.blit(info_text, (10, 60))

    score_text = font.render(f"Счёт: {int(score//1)}", True, white_color)
    surface.blit(score_text, (10, 20))

    multiplier_text = font.render(f"Множитель: x {round(multiplier,2)}", True, white_color)
    surface.blit(multiplier_text, (10, 40))

    control_text1 = font.render("Движение ловушки: влево/вправо", True, white_color)
    surface.blit(control_text1, (screen_w-300, 20))
    control_text2 = font.render("Изменение FPS: вверх/вниз ", True, white_color)
    surface.blit(control_text2, (screen_w-300, 40))
    control_text_bad1 = font.render("Красные квадраты отнимают очки!", True, red_color)
    surface.blit(control_text_bad1, (screen_w - 300, 60))
    control_text_bad2 = font.render("Злые кошки отнимают очки!", True, red_color)
    surface.blit(control_text_bad2, (screen_w - 300, 80))


def enforce_time_limit(t, limit):
    """Ограничение по времени"""
    if t > limit:
        pygame.quit()
        sys.exit()


def update_screen(surface, clock, FPS, t):
    """Обновление экрана

    Возвращает t"""
    pygame.display.flip()
    t = t + 1 / FPS if FPS != 0 else t
    clock.tick(FPS)
    return t
