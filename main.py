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
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.mask = pygame.mask.from_surface(self.image)


    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


if __name__ == '__main__':
    clock = pygame.time.Clock()
    map = Map(21, 20)
    orc = MainHero(load_image("animation.png"), 7, 1, 600, 468)
    running = True
    c = 1
    c1 = 1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        for x in range(map.width):
            c1 = 1
            for y in range(map.height):
                Block(all_sprites, map.field[y][x], c, c1)
                c1 += 32
            c += 32
        clock.tick(100)
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        orc.update()
        pygame.display.flip()
