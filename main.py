import pygame
import os
import sys

BLOCKS = {
    0: {'name': 'air', 'health': 0, 'sprite': 'air.png'},
    1: {'name': 'grass', 'health': 10, 'sprite': 'grass.png'},
    2: {'name': 'ground', 'health': 10, 'sprite': 'ground.png'},
    3: {'name': 'stone', 'health': 20, 'sprite': 'stone.png'}
}
all_sprites = pygame.sprite.Group()
pygame.init()
SCREEN = pygame.display.set_mode((1200, 600))


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

    def update(self):
        pass


class MainHero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('MainHero.png')
        self.x = x
        self.y = y
        self.frames = []
        self.cur_frame = 0
        self.rect = pygame.Rect(x, y, 64, 47)
        self.mask = pygame.mask.from_surface(self.image)

    def edit(self, sheet, columns, rows):
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

    def warmup(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def move(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def edit(self, sheet, columns, rows):
        self.image = sheet
        self.cut_sheet(self.image, columns, rows)


class Skeleton(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.image = load_image('s_stand.png')
        self.x = x
        self.y = y
        self.frames = []
        self.cur_frame = 0
        self.rect = pygame.Rect(x, y, 55, 47)
        self.mask = pygame.mask.from_surface(self.image)

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

    def edit(self, sheet, columns, rows):
        self.image = sheet
        self.cut_sheet(self.image, columns, rows)


if __name__ == '__main__':
    clock = pygame.time.Clock()
    map = Map(21, 20)
    orc = MainHero(600, 468)
    shift = 10
    running = True
    c = 1
    c1 = 1
    enemy = []
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
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
            if key[pygame.K_w]:
                enemy.append(Skeleton(700, 468))
            for item in enemy:
                if abs(item.x - orc.x) <= 100:
#                    item.edit(load_image('s_move.png'), 9, 1)
#                    item.move()
                    item.rect.left -= 100 * clock.tick() / 1000
                    item.x -= 100 * clock.tick() / 1000
        for x in range(map.width):
            c1 = 1
            for y in range(map.height):
                Block(all_sprites, map.field[y][x], c, c1)
                c1 += 32
            c += 32
        clock.tick(100)
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.display.flip()
