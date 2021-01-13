"""main.py -- отвечает за запуск игры"""

# импорты
import pygame
import os
import sys

# константы
FPS = 15
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
clock = pygame.time.Clock()


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
        self.damage = 5
        self.hp = 100

    def edit(self, sheet, columns, rows):
        self.image = sheet
        self.cut_sheet(self.image, columns, rows)

    def cut_sheet(self, sheet, columns, rows):
        self.frames = []
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

    def attack(self, other):
        other.hp -= self.damage

    def draw_attack(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class MainHero(Person):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.hp = 153
        self.damage = 30
        self.attack_range = 96
        self.speed = 10

    def warmup(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def draw_attack(self):
        super().draw_attack()
        if self.cur_frame == 0:
            self.edit(load_image("MainHero.png"), 1, 1)


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, sprite_name, x, y, size, hp):
        super().__init__(all_sprites)
        self.image = load_image(sprite_name)
        self.rect = pygame.Rect(x, y, size[0], size[1])

    def draw(self, hp):
        pygame.draw.rect(self.image, (97, 0, 0), (18, 4, hp, 13))
        pygame.display.flip()


class Skeleton(Person):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.attack_range = 32
        self.speed = 10


def start_game():
    field = Map(21, 20)
    orc = MainHero("MainHero.png", 600, 468, [64, 47])
    health = HealthBar('health_bar.png', 1, 10, (190, 21), orc.hp)
    health.draw(orc.hp)
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
                if event.key == pygame.K_ESCAPE:
                    request = esc()
                    if not request:
                        running = False
            if event.type == pygame.USEREVENT + 1:
                orc.draw_attack()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for enemy in [e for e in enemies if 0 >= e.x - orc.x >= -orc.attack_range]:
                        orc.attack(enemy)
                        if enemy.hp <= 0:
                            enemy.kill()
                            enemies.remove(enemy)
                    orc.edit(load_image("attack1.png"), 6, 1)
                    orc.draw_attack()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 100)
                if event.button == 3:
                    for enemy in [e for e in enemies if 0 >= orc.x - e.x >= -orc.attack_range]:
                        orc.attack(enemy)
                        enemy.speed -= 9
                        if enemy.hp <= 0:
                            enemy.kill()
                            enemies.remove(enemy)
                    orc.edit(load_image("attack2.png"), 6, 1)
                    orc.draw_attack()
                    pygame.time.set_timer(pygame.USEREVENT + 1, 100)
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
            if abs(enemies[enemy].x - orc.x) > enemies[enemy].attack_range:
                if enemies[enemy].x > orc.x:
                    enemies[enemy].edit(load_image('s_walk1.png'), 9, 1)
                    enemies[enemy].move()
                    enemies[enemy].rect.left -= shift - 5
                    enemies[enemy].x -= shift - 5
                elif enemies[enemy].x < orc.x:
                    enemies[enemy].edit(load_image('s_walk2.png'), 9, 1)
                    enemies[enemy].move()
                    enemies[enemy].rect.left += shift - 5
                    enemies[enemy].x += shift - 5
            else:
                if enemies[enemy].x > orc.x:
                    enemies[enemy].edit(load_image('s_attack1.png'), 6, 1)
                    enemies[enemy].attack(orc)
                    enemies[enemy].draw_attack()
                    health.draw(orc.hp)
                elif enemies[enemy].x < orc.x:
                    enemies[enemy].edit(load_image('s_attack2.png'), 6, 1)
                    enemies[enemy].attack(orc)
                    enemies[enemy].draw_attack()
                    health.draw(orc.hp)
                if orc.hp <= 0:
                    running = False
                    orc.kill()
                    for enemy in enemies:
                        enemy.kill()
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)
