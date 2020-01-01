import pygame
import sys
import random

FPS = 10
clock = pygame.time.Clock()
running = True
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init()


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


class AnimatedFon:
    def __init__(self):
        self.fon_images = []
        self.order = 0
        for i in range(91):
            self.fon_images.append(
                pygame.transform.scale(load_image(f'fon/{i}.gif'),
                                       (WIDTH, HEIGHT)))  # загружаем все кадры для анимации фона

    def update(self):  # меняем кадры
        fon = self.fon_images[self.order]
        self.order += 1
        if self.order == 91:
            self.order = 0
        screen.blit(fon, (0, 0))


def start_screen():
    fon = AnimatedFon()
    intro_text = []
    font = pygame.font.Font(None, 30)
    text_coord = 0

    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        fon.update()
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def generate_level(level):
    character, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('sand', x, y)
            elif level[y][x] == '+':
                Tile('sand', x, y)
                Tile('sand1', x, y)
            elif level[y][x] == '@':
                Tile('sand', x, y)
                character = Character(x, y)
            elif level[y][x] == '*':
                Tile('sand', x, y)
                Barrier('stone', x, y)
            elif level[y][x] == ',':
                Tile('sand', x, y)
                Item(x, y)
            elif level[y][x] == '%':
                Tile('sand', x, y)
                Exit(x, y)
            elif level[y][x] == '1':
                Barrier('sea1', x, y)
            elif level[y][x] == '0':
                Barrier('sea', x, y)
            elif level[y][x] == '2':
                Barrier('sea2', x, y)
            elif level[y][x] == '3':
                Barrier('sea3', x, y)
            elif level[y][x] == 'g':
                Tile('sand', x, y)
                Barrier('grass', x, y)
            elif level[y][x] == 'p':
                Tile('sand', x, y)
                Barrier('palm', x, y)
    return character, x, y


def clean():
    global exit, all_sprites
    exit = False

    for i in all_sprites:
        i.kill()


def load_level(filename):
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class Exit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(exit_group, all_sprites)
        self.image = tile_images['exit']
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Barrier(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(barriers_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Item(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(item_group, all_sprites)
        tile_type = random.choice(['apple'])
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global exit
        if exit:
            self.kill()


class Character(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(character_group, all_sprites)
        self.image = character_image
        self.start = False
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)

    def update(self):
        global exit
        if self.start:
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                self.rect.x -= 1
            elif pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                self.rect.x += 1
            elif pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                self.rect.y += 1
            elif pygame.key.get_pressed()[pygame.K_UP] == 1:
                self.rect.y -= 1

            if pygame.sprite.spritecollideany(self, item_group):
                exit = True
            if pygame.sprite.spritecollideany(self, exit_group) and exit:
                clean()
                generate_level(load_level('map2.txt'))
        else:
            self.start = True


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


tile_width = tile_height = 70
tile_images = {'apple': load_image('items/Apple.png'), 'sand': load_image('beach_tileset/sand.png'),
               'stone': load_image('beach_tileset/stones.png'), 'exit': load_image('beach_tileset/exit.png'),
               'sea1': load_image('beach_tileset/sea1.png'), 'sea': load_image('beach_tileset/sea.png'),
               'sea2': load_image('beach_tileset/sea2.png'), 'sea3': load_image('beach_tileset/sea3.png'),
               'sand1': load_image('beach_tileset/sand1.png'), 'grass': load_image('beach_tileset/grass.png'),
               'palm': load_image('beach_tileset/palm1.png')}
character_image = load_image('beach_tileset/character.png')

exit = False

exit_group = pygame.sprite.Group()
barriers_group = pygame.sprite.Group()
character_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

generate_level(load_level('map1.txt'))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    item_group.draw(screen)
    barriers_group.draw(screen)
    exit_group.draw(screen)
    character_group.draw(screen)
    character_group.update()
    item_group.update()
    pygame.display.flip()
