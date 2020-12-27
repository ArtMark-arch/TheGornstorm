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
SCREEN = pygame.display.set_mode((1366, 768))


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
        self.field[len(self.field) // 2] = [1] * width
        self.field[len(self.field) // 2 + 1] = [2] * width
        self.field[len(self.field) // 2 + 2] = [3] * width
        self.left = 1
        self.top = 1
        self.cell_size = 64

    def render(self):
        pass


class Block(pygame.sprite.Sprite):

    def __init__(self, group, id, x, y):
        super().__init__(group)
        self.image = load_image(BLOCKS[id]['sprite'])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pass


if __name__ == '__main__':
    map = Map(21, 12)
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
        SCREEN.fill((0, 0, 0))
        all_sprites.draw(SCREEN)
        pygame.display.flip()
