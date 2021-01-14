"""main.py -- отвечает за запуск игры"""

# импорты
import pygame
import os
import sys
from funcs import load_image

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


class Entity(pygame.sprite.Sprite):

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


class MainHero(Entity):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.hp = 153
        self.damage = 30
        self.attack_range = 96
        self.speed = 10
        self.inventory = ['mace', 'bow']
        self.weapon = 'mace'

    def equip(self):
        if self.weapon == 'mace':
            self.weapon = 'bow'
        else:
            self.weapon = 'mace'

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
        self.start_hp = hp

    def draw(self, hp):
        pygame.draw.rect(self.image, (0, 0, 0), (18, 4, self.start_hp, 13))
        pygame.draw.rect(self.image, (97, 0, 0), (18, 4, hp, 13))
        pygame.display.flip()


class WeaponBar(pygame.sprite.Sprite):
    def __init__(self, sprite_name, x, y):
        super().__init__(all_sprites)
        self.image = load_image(sprite_name)
        self.rect = pygame.Rect(x, y, 32, 64)

    def edit(self, sheet):
        self.image = load_image(sheet)


class Skeleton(Entity):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.attack_range = 32
        self.speed = 10
        self.type = 's'


class Bandit(Entity):

    def __init__(self, sprite_name, x, y, size):
        super().__init__(sprite_name, x, y, size)
        self.attack_range = 64
        self.speed = 5
        self.hp = 150
        self.type = 'b'


class Arrow(Entity):
    def __init__(self, sprite_name, x, y, size, direction):
        super().__init__(sprite_name, x, y, size)
        self.damage = 20
        self.hp = 1
        self.arrow_shift = 0
        self.direction = direction


def start_game():
    image = load_image('background.png')
    background = pygame.sprite.Sprite(all_sprites)
    background.image = image
    background.rect = image.get_rect()
    background.rect.topleft = (1, 1)
    clock = pygame.time.Clock()
    field = Map(30, 20)
    orc = MainHero("MainHero.png", 600, 468, [64, 47])
    health = HealthBar('health_bar.png', 1, 10, (190, 21), orc.hp)
    health.draw(orc.hp)
    weapon = WeaponBar('mace_icon.png', 10, 36)
    shift = 10  # шаг орка
    running = True
    c = 1
    c1 = 1
    enemies = []
    arrows = []
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
                if event.key == pygame.K_x:
                    enemies.append(Skeleton("s_stand.png", 700, 468, [55, 47]))
                if event.key == pygame.K_z:
                    enemies.append(Bandit("b_stand1.png", 600, 468, [57, 48]))
            if event.type == pygame.USEREVENT + 1:
                if orc.frames:
                    orc.draw_attack()
                else:
                    pygame.time.set_timer(pygame.USEREVENT + 1, 0)
                    orc.edit(load_image('MainHero.png'), 1, 1)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 2:
                    orc.equip()
                    if orc.weapon == 'mace':
                        weapon.edit('mace_icon.png')
                    else:
                        weapon.edit('bow_icon.png')
                if event.button == 1:
                    if orc.weapon == 'mace':
                        for enemy in [e for e in enemies if 0 >= e.x - orc.x >= -orc.attack_range]:
                            orc.attack(enemy)
                            if enemy.hp <= 0:
                                enemy.kill()
                                enemies.remove(enemy)
                        orc.edit(load_image("attack1.png"), 6, 1)
                        orc.draw_attack()
                    if orc.weapon == 'bow':
                        orc.edit(load_image("shoot1.png"), 10, 1)
                        orc.draw_attack()
                        orc.rect.topleft = (orc.x, orc.y - 13)
                        arrows.append(Arrow('arrow1.png', orc.x, orc.y + 15, (32, 5), 'left'))
                if event.button == 3:
                    if orc.weapon == 'mace':
                        for enemy in [e for e in enemies if 0 >= orc.x - e.x >= -orc.attack_range]:
                            orc.attack(enemy)
                            if enemy.hp <= 0:
                                enemy.kill()
                                enemies.remove(enemy)
                        orc.edit(load_image("attack2.png"), 6, 1)
                        orc.draw_attack()
                    if orc.weapon == 'bow':
                        orc.edit(load_image("shoot2.png"), 10, 1)
                        orc.draw_attack()
                        arrows.append(Arrow('arrow2.png', orc.x, orc.y + 15, (32, 5), 'right'))
                        orc.rect.topleft = (orc.x, orc.y - 13)
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
        for arrow in [a for a in arrows]:
            if arrow.direction == 'right':
                arrow.rect.left += shift
                arrow.x += shift
                arrow.arrow_shift += shift
                for enemy in enemies:
                    if any([pygame.sprite.collide_mask(enemy, item) for item in arrows]):
                        enemy.hp -= arrow.damage
                        if enemy.hp <= 0:
                            enemy.kill()
                            enemies.remove(enemy)
                        if arrow in arrows:
                            arrow.kill()
                            arrows.remove(arrow)
                if arrow.arrow_shift >= 800:
                    if arrow in arrows:
                        arrow.kill()
                        arrows.remove(arrow)
            if arrow.direction == 'left':
                arrow.rect.left -= shift
                arrow.x += shift
                arrow.arrow_shift -= shift
                for enemy in enemies:
                    if any([pygame.sprite.collide_mask(enemy, item) for item in arrows]):
                        enemy.hp -= arrow.damage
                        if enemy.hp <= 0:
                            enemy.kill()
                            enemies.remove(enemy)
                        if arrow in arrows:
                            arrow.kill()
                            arrows.remove(arrow)
                if arrow.arrow_shift <= -800:
                    if arrow in arrows:
                        arrow.kill()
                        arrows.remove(arrow)
        for enemy in range(len(enemies)):
            if abs(enemies[enemy].x - orc.x) > enemies[enemy].attack_range:
                if enemies[enemy].x > orc.x:
                    enemies[enemy].edit(load_image(f'{enemies[enemy].type}_walk1.png'), 9, 1)
                    enemies[enemy].move()
                    enemies[enemy].rect.left -= shift - 5
                    enemies[enemy].x -= shift - 5
                elif enemies[enemy].x < orc.x:
                    enemies[enemy].edit(load_image(f'{enemies[enemy].type}_walk2.png'), 9, 1)
                    enemies[enemy].move()
                    enemies[enemy].rect.left += shift - 5
                    enemies[enemy].x += shift - 5
            else:
                if enemies[enemy].x > orc.x:
                    enemies[enemy].edit(load_image(f'{enemies[enemy].type}_attack1.png'), 6, 1)
                    enemies[enemy].attack(orc)
                    enemies[enemy].draw_attack()
                    health.draw(orc.hp)
                elif enemies[enemy].x < orc.x:
                    enemies[enemy].edit(load_image(f'{enemies[enemy].type}_attack2.png'), 6, 1)
                    enemies[enemy].attack(orc)
                    enemies[enemy].draw_attack()
                    health.draw(orc.hp)
                if orc.hp <= 0:
                    running = False
                    orc.kill()
                    for enemy in enemies:
                        enemy.kill()
                    orc = MainHero("MainHero.png", 600, 468, [64, 47])
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.display.flip()
        clock.tick(FPS)
