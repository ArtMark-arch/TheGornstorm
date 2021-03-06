"""menu.py - отвечает за меню и связку модулей."""

# импорты
import pygame
import pygame_gui

from main import start_game
from funcs import load_image

# Константы
SIZE = WIDTH, HEIGHT = 800, 600
WINDOW_TITLE = "The Gornstorm v. pre alpha"
FPS = 15  # количество кадров в секунду
btn = int(25 * WIDTH / 100), int(12.5 * HEIGHT / 100)  # размер кнопки
btn_distance = int(1 * HEIGHT / 100)  # расстояние между кнопками (1% от высоты окна)

# Инициализация библиотеки и создание необходимых объектов управления
pygame.init()
clock = pygame.time.Clock()
manager = pygame_gui.UIManager(SIZE, "theme.json")
all_sprites = pygame.sprite.Group()

# Цвета
orange = pygame.Color("orange")


def draw_our_epic_title():
    """Рисование названия"""
    font = pygame.font.Font("Fonts/GothicPixels.ttf", 50)
    text = font.render("The Gornstorm", True, orange)
    text_x = WIDTH // 2 - text.get_width() // 2
    text_y = HEIGHT // 4 - text.get_height() // 2
    screen.blit(text, (text_x, text_y))


if __name__ == '__main__':
    # Настройка окна
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    screen.fill(pygame.Color((0, 0, 0)))

    # Рисование фона
    background_image = load_image("MainMenu.png")
    background = pygame.sprite.Sprite(all_sprites)
    background.image = background_image
    background.rect = background_image.get_rect()
    background.rect.topleft = (1, 1)

    # Установка кнопок
    play = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 - btn[0] // 2, HEIGHT // 2 - btn[1] // 2), btn),
        text="Play",
        manager=manager
    )

    off = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(
            (WIDTH // 2 - btn[0] // 2, HEIGHT // 2 + btn_distance + btn[1] // 2), btn),
        text="Exit",
        manager=manager
    )

    # Главный игровой цикл
    running = True
    while running:

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == off:
                        running = False
                    if event.ui_element == play:
                        start_game()
                        screen.fill(pygame.Color((0, 0, 0)))
            manager.process_events(event)
        manager.update(FPS / 1000.0)

        # Смена кадра
        all_sprites.draw(screen)
        draw_our_epic_title()
        manager.draw_ui(screen)
        pygame.display.flip()

        # Задержка
        clock.tick(FPS)

    # Отключение библиотеки
    pygame.quit()
