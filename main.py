"""main.py -- отвечает за запуск игры"""

# импорты
import pygame
import os
import sys

# константы
FPS = 60
WIDTH = 800
HEIGHT = 600
BLOCKS = {
    0: {'name': 'air', 'sprite': 'air.png'},
    1: {'name': 'grass', 'sprite': 'grass.png'},
    2: {'name': 'ground', 'sprite': 'ground.png'},
    3: {'name': 'stone', 'sprite': 'stone.png'}
}
all_sprites = pygame.sprite.Group()
pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))


def load_image(name, colorkey=None):
    fullname = os.path.join('Sprites', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


image = load_image('background.png')
background = pygame.sprite.Sprite(all_sprites)
background.image = image
background.rect = image.get_rect()
background.rect.topleft = (1, 1)


class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.field = [[0] * width for _ in range(height)]
        self.field[-3] = [1] * width
        self.field[-2] = [2] * width
        self.field[-1] = [3] * width
        self.left = 1
        self.top = 1
        self.cell_size = 32

    def render(self):
        pass


class Block(pygame.sprite.Sprite):

    def __init__(self, group, id, x, y):
        super().__init__(group)
        self.image = load_image(BLOCKS[id]['sprite'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = y


class Person(pygame.sprite.Sprite):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(all_sprites)
        self.image = load_image(sprite_name)
        self.x = x
        self.y = y
        self.frames = []
        self.cur_frame = 0
        self.rect = pygame.Rect(x, y, size[0], size[1])
        self.mask = pygame.mask.from_surface(self.image)

    def edit(self, sheet, columns, rows):
        self.frames = []
        self.image = sheet
        self.cut_sheet(self.image, columns, rows)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(self.x, self.y, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def move(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class MainHero(Person):

    def warmup(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Skeleton(Person):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.attack_range = 20


def start_game():
    clock = pygame.time.Clock()
    field = Map(21, 20)
    orc = MainHero("MainHero.png", 600, 468, [64, 47])
    shift = 10  # шаг орка
    running = True
    c = 1
    c1 = 1
    enemies = []
    for x in range(field.width):
        c1 = 1
        for y in range(field.height):
            Block(all_sprites, field.field[y][x], c, c1)
            c1 += 32
        c += 32
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    enemies.append(Skeleton("s_stand.png", 700, 468, [55, 47]))
                    print(enemies)
            key = pygame.key.get_pressed()
            if key[pygame.K_d]:
                orc.rect.left += shift
                orc.x += shift
                orc.edit(load_image('walk1.png'), 7, 1)
                orc.move()
            if key[pygame.K_a]:
                orc.rect.left -= shift
                orc.x -= shift
                orc.edit(load_image('walk2.png'), 7, 1)
                orc.move()
            if key[pygame.K_s]:
                orc.edit(load_image('MainHero.png'), 1, 1)
        for enemy in range(len(enemies)):
            print(enemies[enemy].x, orc.x)
            if abs(enemies[enemy].x - orc.x) > enemies[enemy].attack_range:
                enemies[enemy].edit(load_image('s_move.png'), 9, 1)
                enemies[enemy].move()
                if enemies[enemy].x > orc.x:
                    enemies[enemy].rect.left -= shift - 9
                    enemies[enemy].x -= shift - 9
                else:
                    enemies[enemy].rect.left += shift - 9
                    enemies[enemy].x += shift - 9
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)
