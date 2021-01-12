import random
import pygame
import os
import sys  # Импортируются библиотеки
from PROGRAMM import Player, Directions, Ball, Racketka, game_over
global screen


def open_nearest(y, x, board):  # Функция открытия ближайших клеток
    for y2 in range(-1, 2):
        if not (y + y2 >= 10 or y + y2 < 0):
            for x2 in range(-1, 2):
                if not (x + x2 >= 10 or x + x2 < 0):
                    if board[y + y2][x + x2] == - 1:
                        if not x2 == y2 == 0:
                            s = 0
                            for dy in range(-1, 2):
                                if not (y + y2 + dy >= 10 or y + y2 + dy < 0):
                                    for dx in range(-1, 2):
                                        if not (x + x2 + dx >= 10 or x + x2 + dx < 0):
                                            if board[y + y2 + dy][x + x2 + dx] == 10:
                                                s += 1
                                board[y + y2][x + x2] = s
                            if s == 0 and not (y2 == 0 and x2 == 0):
                                board = open_nearest(y + y2, x + x2, board)
    return board


def load_image(name, color_key=None):  # Функия для загрузки изображения
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не могу загрузить изображение:', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Board:
    def __init__(self, width_of_board, height_of_board):  # Функция создания игры
        self.width = width_of_board
        self.height = height_of_board
        self.board = [[0] * width_of_board for _ in range(height_of_board)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):  # Рендеринг поля
        for y in range(self.height):
            for x in range(self.width):
                pygame.draw.rect(screen,
                                 pygame.Color('black'), (
                                     x * self.cell_size + self.left,
                                     y * self.cell_size + self.top,
                                     self.cell_size, self.cell_size), 1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):  # Определение местоположения клетки
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 \
                or cell_x >= self.width \
                or cell_y < 0 \
                or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        pass


class XO(Board):
    def __init__(self, width_of_xo, height_of_xo):  # Функция создания поля дла крестиков-ноликов
        super().__init__(width_of_xo, height_of_xo)
        self.timer = - 1
        self.win = False
        self.country = False
        self.width = width_of_xo
        self.height = height_of_xo
        self.board = [[1] * width_of_xo for _ in range(height_of_xo)]
        self.left = 10
        self.top = 10
        self.cell_size = 30
        self.x = ['x', 'y']
        self.k = 0
        self.start = False

    def draw_x(self, x, y):  # Заполнение списка после нажатия на клетку
        self.board[x][y] = 'x'
        self.k += 1
        if self.k > 4:
            self.result()

    def draw_0(self, x, y):  # Заполнение списка после нажатия на клетку
        self.board[x][y] = '0'
        self.k += 1
        if self.k > 4:
            self.result()

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):  # Рендеринг поля
        if not self.start:  # Рендеринг правил
            screen.fill((107, 142, 35))
            all_sprites_of_xo = pygame.sprite.Group()
            camouflage = pygame.sprite.Sprite(all_sprites_of_xo)
            camouflage.image = load_image('camouflage.png')
            camouflage.rect = camouflage.image.get_rect()
            camouflage.rect.topleft = [0, 0]
            all_sprites_of_xo.draw(screen)
            font = pygame.font.Font('data/Arial.ttf', 25)
            text = font.render('Стандартная игра в крестики-нолики(изменены иконки).',
                               True, (255, 193, 37))
            text_x = 20
            text_y = 40
            screen.blit(text, (text_x, text_y))
            text_x2 = 30
            text_y2 = 80
            font = pygame.font.Font('data/Arial.ttf', 20)
            text2 = font.render('Нажмите любую кнопку, чтобы продолжить',
                                True, (255, 193, 37))
            screen.blit(text2, (text_x2, text_y2))
            font = pygame.font.Font('data/Arial.ttf', 20)
            text21 = font.render('или возобновить игру после ее окончания.',
                                 True, (255, 193, 37))
            text_x21 = 30
            text_y21 = 120
            screen.blit(text21, (text_x21, text_y21))
            text_x3 = 30
            text_y3 = 160
            font = pygame.font.Font('data/Arial.ttf', 20)
            text3 = font.render('Игроки по очереди ставят на свободные клетки поля 3х3 знаки.',
                                True, (255, 193, 37))
            screen.blit(text3, (text_x3, text_y3))
            text_x4 = 30
            text_y4 = 200
            font = pygame.font.Font('data/Arial.ttf', 20)
            text4 = font.render('Первый, выстроивший в ряд 3 своих фигуры по вертикали,',
                                True, (255, 193, 37))
            screen.blit(text4, (text_x4, text_y4))
            text_x5 = 30
            text_y5 = 240
            font = pygame.font.Font('data/Arial.ttf', 20)
            text5 = font.render('горизонтали или диагонали, выигрывает.',
                                True, (255, 193, 37))
            screen.blit(text5, (text_x5, text_y5))

        elif self.start:  # Рендеринг игры
            if self.win is False or -1 < self.timer <= 12:  # Рендеринг игры, где пока нет победителя
                if not self.timer == - 1:
                    self.timer += 1
                self.timer += 1
                screen.fill((208, 227, 247))
                all_sprites_of_xo = pygame.sprite.Group()
                camouflage = pygame.sprite.Sprite(all_sprites_of_xo)
                camouflage.image = load_image('camouflage.png')
                camouflage.rect = camouflage.image.get_rect()
                camouflage.rect.topleft = [0, 0]
                all_sprites_of_xo.draw(screen)
                for y in range(self.height):
                    for x in range(self.width):
                        if self.board[x][y] == 'x':
                            hero = pygame.sprite.Sprite(all_sprites_of_xo)
                            hero.image = load_image('soviet.png')
                            hero.image.set_colorkey((255, 255, 255))
                            hero.rect = hero.image.get_rect()
                            hero.rect.topleft = [x * self.cell_size + 10, y * self.cell_size + 11]
                            all_sprites_of_xo.draw(screen)
                        elif self.board[x][y] == '0':
                            hero = pygame.sprite.Sprite(all_sprites_of_xo)
                            hero.image = load_image('german.png')
                            hero.image.set_colorkey((255, 255, 255))
                            hero.rect = hero.image.get_rect()
                            hero.rect.topleft = [x * self.cell_size + 10, y * self.cell_size + 41]
                            all_sprites_of_xo.draw(screen)
                        pygame.draw.rect(screen,
                                         pygame.Color((107, 142, 35)), (0, 0,
                                                                        3 * self.cell_size,
                                                                        3 * self.cell_size), 20)
                for y in range(self.height):
                    for x in range(self.width):
                        pygame.draw.rect(screen,
                                         pygame.Color('black'), (
                                            x * self.cell_size + self.left,
                                            y * self.cell_size + self.top,
                                            self.cell_size, self.cell_size), 1)
            else:  # Рендеринг экрана победы
                all_sprites_of_xo = pygame.sprite.Group()
                screen.fill((107, 142, 35))
                camouflage = pygame.sprite.Sprite(all_sprites_of_xo)
                camouflage.image = load_image('camouflage.png')
                camouflage.rect = camouflage.image.get_rect()
                camouflage.rect.topleft = [0, 0]
                all_sprites_of_xo.draw(screen)
                font = pygame.font.Font('data/Arial.ttf', 50)
                if self.country == 'x':
                    hero = pygame.sprite.Sprite(all_sprites_of_xo)
                    hero.image = load_image('soviet.png')
                    hero.image.set_colorkey((255, 255, 255))
                    hero.rect = hero.image.get_rect()
                    hero.rect.topleft = [240, 100]
                    all_sprites_of_xo.draw(screen)
                    answer = 'Выиграла Красная Армия!!!'
                elif self.country == '0':
                    hero = pygame.sprite.Sprite(all_sprites_of_xo)
                    hero.image = load_image('german.png')
                    hero.image.set_colorkey((255, 255, 255))
                    hero.rect = hero.image.get_rect()
                    hero.rect.topleft = [240, 130]
                    all_sprites_of_xo.draw(screen)
                    answer = 'Выиграл Вермахт. Гады!!!'
                else:
                    answer = 'Ничья'
                text = font.render(answer, True, (255, 211, 0))
                text_x = 350 - text.get_width() // 2
                text_y = 350 - text.get_height() // 2 + 30
                text_w = text.get_width()
                text_h = text.get_height()
                pygame.draw.rect(screen, 'black', (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20))
                screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, 'red', (text_x - 5, text_y - 5,
                                                 text_w + 10, text_h + 10), 2)
                font = pygame.font.Font('data/Army.ttf', 20)
                text2 = font.render('Esc-return to menu',
                                    True, (255, 193, 37))
                text_x2 = 450
                text_y2 = 540
                screen.blit(text2, (text_x2, text_y2))
                font = pygame.font.Font('data/Army.ttf', 20)
                text3 = font.render('Enter-continue',
                                    True, (255, 193, 37))
                text_x3 = 450
                text_y3 = 500
                screen.blit(text3, (text_x3, text_y3))

    def on_click(self, cell):  # Обработка нажатия на клетку под определенным номером
        if cell is not None:
            cell_x = cell[0]
            cell_y = cell[1]
            if self.k % 2 == 0 and self.board[cell_x][cell_y] == 1:
                self.draw_x(cell_x, cell_y)
            elif self.k % 2 == 1 and self.board[cell_x][cell_y] == 1:
                self.draw_0(cell_x, cell_y)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):  # Нахождение номера клетки
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 \
                or cell_x >= self.width \
                or cell_y < 0 \
                or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def result(self):  # Проверка на наличие победителя
        if self.board[0][0] == self.board[0][1] == self.board[0][2] and not self.board[0][0] == 1:
            self.win = True
            self.country = self.board[0][0]
            self.timer = 0
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] and not self.board[0][0] == 1:
            self.win = True
            self.country = self.board[0][0]
            self.timer = 0
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] and not self.board[0][0] == 1:
            self.win = True
            self.country = self.board[0][0]
            self.timer = 0
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] and not self.board[1][0] == 1:
            self.win = True
            self.country = self.board[1][0]
            self.timer = 0
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] and not self.board[2][1] == 1:
            self.win = True
            self.country = self.board[2][0]
            self.timer = 0
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] and not self.board[0][1] == 1:
            self.win = True
            self.country = self.board[0][1]
            self.timer = 0
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] and not self.board[0][2] == 1:
            self.win = True
            self.country = self.board[0][2]
            self.timer = 0
        elif self.board[0][2] == self.board[1][1] == self.board[2][0] and not self.board[0][2] == 1:
            self.win = True
            self.country = self.board[0][2]
            self.timer = 0
        elif self.k == 9:
            self.win = True
            self.country = 'Ничья'
            self.timer = 11


class Minesweeper(Board):
    def __init__(self, width_of_m, height_of_m, n):  # Создание игры
        super().__init__(width_of_m, height_of_m)
        self.board = [[-1] * 10 for _ in range(10)]
        i = 0
        while i < n:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] == -1:
                self.board[y][x] = 10
                i += 1
        self.lost = False
        self.start = False
        self.win = False
        self.flags = []
        self.timer = 0

    def get_click_flag(self, mouse_pos):  # Создание флага
        flag_x, flag_y = self.get_cell(mouse_pos)
        if not 10 > self.board[flag_y][flag_x] >= 0:
            if (flag_x, flag_y) in self.flags:
                self.flags.remove((flag_x, flag_y))
            else:
                self.flags.append((flag_x, flag_y))

    def open_cell(self, cell):  # Открытие клетки
        if cell not in self.flags or self.lost is True:
            x, y = cell
            if self.board[y][x] == 10:
                self.lost = True
                self.timer = 0
            else:
                s = 0
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if x + dx < 0 \
                                or x + dx >= self.width \
                                or y + dy < 0 \
                                or y + dy >= self.height:
                            continue
                        if self.board[y + dy][x + dx] == 10:
                            s += 1
                self.board[y][x] = s
                if s == 0:
                    self.board = open_nearest(y, x, self.board)  # Открытие ближайших

    def open_rect(self, mouse_pos):  # Открытие квадрата вокруг клетки
        x, y = self.get_cell(mouse_pos)
        if 10 > self.board[y][x] >= 0:
            number = self.board[y][x]
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if (x + dx, y + dy) in self.flags:
                        count += 1
            if number == count:
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if 0 <= x + dx < 10 and 0 <= y + dy < 10:
                            if self.board[y + dy][x + dx] == 10 and (x + dx, y + dy) in self.flags:
                                pass
                            elif self.board[y + dy][x + dx] == 10 and (x + dx, y + dy) not in self.flags:
                                self.lost = True
                                self.timer = 0
                            else:
                                self.open_cell([x + dx, y + dy])

    def on_click(self, cell):
        self.open_cell(cell)

    def render(self):  # Рендеринг игры
        if self.start:  # Рендеринг игры после ее начала
            all_sprites_of_m = pygame.sprite.Group()
            if not (self.lost or self.win):
                screen.fill((170, 170, 170))
                for y in range(self.height):
                    for x in range(self.width):
                        if self.board[y][x] >= 0 and self.board[y][x] != 10:
                            font = pygame.font.Font(None, self.cell_size - 6)
                            if self.board[y][x] == 0:
                                color = 'white'
                            elif self.board[y][x] == 1:
                                color = 'black'
                            elif self.board[y][x] == 2:
                                color = 'grey'
                            elif self.board[y][x] == 3:
                                color = 'yellow'
                            else:
                                color = 'red'
                            pygame.draw.rect(screen, pygame.Color(112, 130, 56),
                                             (x * self.cell_size + self.left,
                                              y * self.cell_size + self.top,
                                              self.cell_size,
                                              self.cell_size))
                            if not self.board[y][x] == 0:
                                text = font.render(str(self.board[y][x]),
                                                   True, pygame.Color(color))
                                screen.blit(text, (x * self.cell_size + self.left + 20,
                                                   y * self.cell_size + self.top + 11))
                        else:
                            pygame.draw.rect(screen, (75, 83, 32),
                                             (x * self.cell_size + self.left,
                                              y * self.cell_size + self.top,
                                              self.cell_size,
                                              self.cell_size))
                            pygame.draw.rect(screen, pygame.Color(55, 63, 12),
                                             (x * self.cell_size + self.left,
                                              y * self.cell_size + self.top,
                                              self.cell_size,
                                              self.cell_size), 8)
                        if (x, y) in self.flags:
                            hero = pygame.sprite.Sprite(all_sprites_of_m)
                            hero.image = load_image('flag.png')
                            hero.image.set_colorkey((255, 255, 255))
                            hero.rect = hero.image.get_rect()
                            hero.rect.topleft = [x * self.cell_size + self.left,
                                                 y * self.cell_size + self.top]
                            all_sprites_of_m.draw(screen)
                        pygame.draw.rect(screen, pygame.Color('black'),
                                         (x * self.cell_size + self.left,
                                          y * self.cell_size + self.top,
                                          self.cell_size,
                                          self.cell_size), 1)
            elif self.win:  # Рендеринг игры, в случае победы
                screen.fill((107, 142, 35))
                camouflage = pygame.sprite.Sprite(all_sprites_of_m)
                camouflage.image = load_image('camouflage.png')
                camouflage.rect = camouflage.image.get_rect()
                camouflage.rect.topleft = [0, 0]
                all_sprites_of_m.draw(screen)
                font = pygame.font.Font('data/Arial.ttf', 50)
                text = font.render('Вы победили!!!', True, (255, 211, 0))
                text_x = 350 - text.get_width() // 2
                text_y = 350 - text.get_height() // 2
                text_w = text.get_width()
                text_h = text.get_height()
                screen.blit(text, (text_x, text_y))
                screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, 'black', (text_x - 10, text_y - 10,
                                                   text_w + 20, text_h + 20))
                screen.blit(text, (text_x, text_y))
                pygame.draw.rect(screen, 'red', (text_x - 5, text_y - 5,
                                                 text_w + 10, text_h + 10), 2)
                font = pygame.font.Font('data/Army.ttf', 20)
                text2 = font.render('Esc-return to menu',
                                    True, (255, 193, 37))
                text_x2 = 450
                text_y2 = 540
                screen.blit(text2, (text_x2, text_y2))
                font = pygame.font.Font('data/Army.ttf', 20)
                text3 = font.render('Enter-continue',
                                    True, (255, 193, 37))
                text_x3 = 450
                text_y3 = 500
                screen.blit(text3, (text_x3, text_y3))
            else:  # Рендеринг игры, в случае поражения
                if self.timer <= 100:
                    self.timer += 1
                    screen.fill((112, 130, 56))
                    for y in range(self.height):
                        for x in range(self.width):
                            if self.board[y][x] == 10:
                                if self.timer <= 10:  # Рисование бомбы
                                    hero = pygame.sprite.Sprite(all_sprites_of_m)
                                    hero.image = load_image('bomb.png')
                                    hero.image.set_colorkey((255, 255, 255))
                                    hero.rect = hero.image.get_rect()
                                    hero.rect.topleft = [x * self.cell_size + self.left,
                                                         y * self.cell_size + self.top]
                                    all_sprites_of_m.draw(screen)
                                else:  # Рисование взрыва после истечения таймера
                                    hero = pygame.sprite.Sprite(all_sprites_of_m)
                                    hero.image = load_image('boom.png')
                                    hero.image.set_colorkey((255, 255, 255))
                                    hero.rect = hero.image.get_rect()
                                    hero.rect.topleft = [x * self.cell_size + self.left,
                                                         y * self.cell_size + self.top]
                                    all_sprites_of_m.draw(screen)
                            if self.board[y][x] >= 0 and self.board[y][x] != 10:
                                font = pygame.font.Font(None, self.cell_size - 6)
                                if self.board[y][x] == 0:
                                    color = 'white'
                                elif self.board[y][x] == 1:
                                    color = 'black'
                                elif self.board[y][x] == 2:
                                    color = 'grey'
                                elif self.board[y][x] == 3:
                                    color = 'yellow'
                                else:
                                    color = 'red'
                                pygame.draw.rect(screen, pygame.Color((112, 130, 56)),
                                                 (x * self.cell_size + self.left,
                                                  y * self.cell_size + self.top,
                                                  self.cell_size,
                                                  self.cell_size))
                                if not self.board[y][x] == 0:
                                    text = font.render(str(self.board[y][x]),
                                                       True, pygame.Color(color))
                                    screen.blit(text, (x * self.cell_size + self.left + 20,
                                                       y * self.cell_size + self.top + 11))
                            if self.board[y][x] < 0:
                                font = pygame.font.Font(None, self.cell_size - 6)
                                self.open_cell((x, y))
                                if self.board[y][x] == 0:
                                    color = 'white'
                                elif self.board[y][x] == 1:
                                    color = 'black'
                                elif self.board[y][x] == 2:
                                    color = 'grey'
                                elif self.board[y][x] == 3:
                                    color = 'yellow'
                                else:
                                    color = 'red'
                                pygame.draw.rect(screen, pygame.Color((112, 130, 56)),
                                                 (x * self.cell_size + self.left,
                                                  y * self.cell_size + self.top,
                                                  self.cell_size,
                                                  self.cell_size))
                                if not self.board[y][x] == 0:
                                    text = font.render(str(self.board[y][x]),
                                                       True, pygame.Color(color))
                                    screen.blit(text, (x * self.cell_size + self.left + 20,
                                                       y * self.cell_size + self.top + 11))
                            pygame.draw.rect(screen, pygame.Color('black'),
                                             (x * self.cell_size + self.left,
                                              y * self.cell_size + self.top,
                                              self.cell_size,
                                              self.cell_size), 1)
                else:  # Рендеринг игры, в случае поражения
                    screen.fill((107, 142, 35))
                    camouflage = pygame.sprite.Sprite(all_sprites_of_m)
                    camouflage.image = load_image('camouflage.png')
                    camouflage.rect = camouflage.image.get_rect()
                    camouflage.rect.topleft = [0, 0]
                    all_sprites_of_m.draw(screen)
                    font = pygame.font.Font('data/Arial.ttf', 50)
                    text = font.render('Вы проиграли.', True, (255, 211, 0))
                    text_x = 350 - text.get_width() // 2
                    text_y = 350 // 2 - text.get_height() // 2
                    text_w = text.get_width()
                    text_h = text.get_height()
                    pygame.draw.rect(screen, 'black', (text_x - 10, text_y - 10,
                                                       text_w + 20, text_h + 20))
                    screen.blit(text, (text_x, text_y))
                    pygame.draw.rect(screen, 'red', (text_x - 5, text_y - 5,
                                                     text_w + 10, text_h + 10), 2)
                    screen.blit(text, (text_x, text_y))
                    screen.blit(text, (text_x, text_y))
                    font = pygame.font.Font('data/Army.ttf', 20)
                    text2 = font.render('Esc-return to menu',
                                        True, (255, 193, 37))
                    text_x2 = 450
                    text_y2 = 540
                    screen.blit(text2, (text_x2, text_y2))
                    font = pygame.font.Font('data/Army.ttf', 20)
                    text3 = font.render('Enter-continue',
                                        True, (255, 193, 37))
                    text_x3 = 450
                    text_y3 = 500
                    screen.blit(text3, (text_x3, text_y3))
        else:  # Рендеринг правил игры
            all_sprites_of_m = pygame.sprite.Group()
            screen.fill((107, 142, 35))
            camouflage = pygame.sprite.Sprite(all_sprites_of_m)
            camouflage.image = load_image('camouflage.png')
            camouflage.rect = camouflage.image.get_rect()
            camouflage.rect.topleft = [0, 0]
            all_sprites_of_m .draw(screen)
            font = pygame.font.Font('data/Arial.ttf', 25)
            text = font.render('Стандартная игра в сапер.',
                               True, (255, 193, 37))
            text_x = 120
            text_y = 40
            screen.blit(text, (text_x, text_y))
            text_x2 = 40
            text_y2 = 80
            font = pygame.font.Font('data/Arial.ttf', 20)
            text2 = font.render('Нажмите любую кнопку, чтобы продолжить',
                                True, (255, 193, 37))
            screen.blit(text2, (text_x2, text_y2))
            font = pygame.font.Font('data/Arial.ttf', 20)
            text21 = font.render('или возобновить игру после ее окончания.',
                                 True, (255, 193, 37))
            text_x21 = 40
            text_y21 = 120
            screen.blit(text21, (text_x21, text_y21))
            text_x3 = 40
            text_y3 = 160
            font = pygame.font.Font('data/Arial.ttf', 20)
            text3 = font.render('«Сапер» – это несложная игра, развивающая внимание,',
                                True, (255, 193, 37))
            screen.blit(text3, (text_x3, text_y3))
            text_x4 = 40
            text_y4 = 200
            font = pygame.font.Font('data/Arial.ttf', 20)
            text4 = font.render('память и логику. Цель – открыть все ячейки на поле так,',
                                True, (255, 193, 37))
            screen.blit(text4, (text_x4, text_y4))
            text_x5 = 40
            text_y5 = 240
            font = pygame.font.Font('data/Arial.ttf', 20)
            text5 = font.render('чтобы не “взорвать” ни одну мину. Для поиска',
                                True, (255, 193, 37))
            screen.blit(text5, (text_x5, text_y5))
            text_x6 = 40
            text_y6 = 280
            font = pygame.font.Font('data/Arial.ttf', 20)
            text6 = font.render('взрывоопасных квадратиков можно использовать подсказки.',
                                True, (255, 193, 37))
            screen.blit(text6, (text_x6, text_y6))
        if self.start:
            self.win = self.result()

    def result(self):
        for i in self.board:
            if -1 in i or self.lost is True:
                return False
        return True


def draw(screen_draw):  # Рисование менюшки
    all_sprites1 = pygame.sprite.Group()
    screen_draw.fill((107, 142, 35))
    camouflage = pygame.sprite.Sprite(all_sprites1)
    camouflage.image = load_image('camouflage.png')
    camouflage.rect = camouflage.image.get_rect()
    camouflage.rect.topleft = [0, 0]
    all_sprites1.draw(screen_draw)
    hero1 = pygame.sprite.Sprite(all_sprites1)
    hero1.image = load_image('soviet-menu.png')
    hero1.image.set_colorkey((255, 255, 255))
    hero1.rect = hero1.image.get_rect()
    hero1.rect.topleft = [91, 232]
    hero2 = pygame.sprite.Sprite(all_sprites1)
    hero2.image = load_image('german-menu.png')
    hero2.image.set_colorkey((255, 255, 255))
    hero2.rect = hero2.image.get_rect()
    hero2.rect.topleft = [648, 244]
    hero3 = pygame.sprite.Sprite(all_sprites1)
    hero3.image = load_image('bomb-menu.png')
    hero3.image.set_colorkey((255, 255, 255))
    hero3.rect = hero1.image.get_rect()
    hero3.rect.topleft = [256, 140]
    hero4 = pygame.sprite.Sprite(all_sprites1)
    hero4.image = load_image('flag-menu.png')
    hero4.image.set_colorkey((255, 255, 255))
    hero4.rect = hero4.image.get_rect()
    hero4.rect.topleft = [490, 140]
    all_sprites1.draw(screen_draw)
    font = pygame.font.Font('data/army.ttf', 50)
    text = font.render('Army games',
                       True, (0, 0, 0))
    text_x = 230
    text_y = 20
    screen_draw.blit(text, (text_x, text_y))
    font = pygame.font.Font('data/Arial.ttf', 40)
    text2 = font.render(' САПЕР ',
                        True, (255, 211, 0))
    text_w2 = text2.get_width()
    text_h2 = text2.get_height()
    text_x2 = 320
    text_y2 = 150
    pygame.draw.rect(screen_draw, 'black', (text_x2 - 10, text_y2 - 10,
                                            text_w2 + 20, text_h2 + 20))
    pygame.draw.rect(screen_draw, 'red', (text_x2 - 5, text_y2 - 5,
                                          text_w2 + 10, text_h2 + 10), 5)
    screen_draw.blit(text2, (text_x2, text_y2))
    text_x3 = 180
    text_y3 = 250
    font = pygame.font.Font('data/Arial.ttf', 40)
    text3 = font.render('  КРЕСТИКИ-НОЛИКИ  ',
                        True, (255, 211, 0))
    text_w3 = text3.get_width()
    text_h3 = text3.get_height()
    pygame.draw.rect(screen_draw, 'black', (text_x3 - 10, text_y3 - 10,
                                            text_w3 + 20, text_h3 + 20))
    pygame.draw.rect(screen_draw, 'red', (text_x3 - 5, text_y3 - 5,
                                          text_w3 + 10, text_h3 + 10), 3)
    screen_draw.blit(text3, (text_x3, text_y3))
    font = pygame.font.Font('data/Arial.ttf', 40)
    text_x4 = 275
    text_y4 = 350
    text4 = font.render(' ПИНГ-ПОНГ ',
                        True, (255, 211, 0))
    text_w4 = text4.get_width()
    text_h4 = text4.get_height()
    pygame.draw.rect(screen_draw, 'black', (text_x4 - 10, text_y4 - 10,
                                            text_w4 + 20, text_h4 + 20))
    pygame.draw.rect(screen_draw, 'red', (text_x4 - 5, text_y4 - 5,
                                          text_w4 + 10, text_h4 + 10), 3)
    screen_draw.blit(text4, (text_x4, text_y4))


def game_on(position):  # Создание цикла игры в случае нажатия на кнопку
    global screen
    if position is not None:
        x = position[0]
        y = position[1]
        if 320 < x < 475 and 150 < y < 185:
            pygame.init()
            pygame.display.set_caption('Сапер')
            size = [700, 700]
            screen = pygame.display.set_mode(size)
            clock = pygame.time.Clock()
            dim = 10
            mines = 10
            board = Minesweeper(dim, dim, mines)
            board.set_view(0, 0, min(size) // dim)
            ticks = 0
            running = True
            all_sprites = pygame.sprite.Group()
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Выключение программы
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Выход в меню
                        running = False
                        pygame.quit()
                        start()
                    if event.type == pygame.MOUSEBUTTONDOWN and board.lost is False and board.win is False\
                            and board.start is True and event.button == 1:  # Обработка нажатия ЛКВ
                        board.get_click(event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and board.lost is False and board.win is False\
                            and board.start is True and event.button == 3:  # Обработка нажатия ПКВ
                        board.get_click_flag(event.pos)
                    if event.type == pygame.MOUSEBUTTONDOWN and board.lost is False and board.win is False\
                            and board.start is True and pygame.mouse.get_pressed(num_buttons=3)[0]\
                            and pygame.mouse.get_pressed(num_buttons=3)[2]:  # Обработка нажатия ЛКВ + ПКВ
                        board.open_rect(event.pos)
                    if board.start is False and event.type == pygame.KEYDOWN:  # Начало игры
                        if event.key == pygame.K_RETURN:
                            board.start = True
                    if board.start is False and event.type == pygame.MOUSEBUTTONDOWN:  # Начало игры
                        board.start = True
                    if ((board.lost and board.timer > 100) or board.win) and\
                            event.type == pygame.MOUSEBUTTONDOWN:  # Обновление игры
                        board.timer = 0
                        all_sprites = pygame.sprite.Group()
                        board.flags = []
                        board.board = [[-1] * 10 for _ in range(10)]
                        i = 0
                        while i < 10:
                            x = random.randint(0, board.width - 1)
                            y = random.randint(0, board.height - 1)
                            if board.board[y][x] == -1:
                                board.board[y][x] = 10
                                i += 1
                        board.win = False
                        board.lost = False
                    if ((board.lost and board.timer > 100) or board.win) and\
                            event.type == pygame.KEYDOWN:  # Обновление игры
                        board.timer = 0
                        if not event.key == pygame.K_ESCAPE:
                            all_sprites = pygame.sprite.Group()
                            board.flags = []
                            board.board = [[-1] * 10 for _ in range(10)]
                            i = 0
                            while i < 10:
                                x = random.randint(0, board.width - 1)
                                y = random.randint(0, board.height - 1)
                                if board.board[y][x] == -1:
                                    board.board[y][x] = 10
                                    i += 1
                            board.win = False
                            board.lost = False
                if running is True:
                    screen.fill(pygame.Color('black'))
                    board.render()
                    pygame.display.flip()
                    all_sprites.draw(screen)
                    clock.tick(50)
                    ticks += 1
            pygame.quit()
        elif 200 < x < 655 and 250 < y < 285:
            pygame.init()
            pygame.display.set_caption('Крестики-нолики')
            size = [700, 700]
            screen = pygame.display.set_mode(size)
            running = True
            board = XO(3, 3)
            board.set_view(0, 0, min(size) // 3)
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # Выключение программы
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN and board.win is False and board.start is True:
                        board.get_click(event.pos)
                    if board.start is False and event.type == pygame.MOUSEBUTTONDOWN:  # Начало игры
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            board.start = True
                    if board.start is False and event.type == pygame.KEYDOWN:  # Начало игры
                        if not event.key == pygame.K_ESCAPE:
                            board.start = True
                    if board.win and board.timer > 12 and event.type == pygame.KEYDOWN:  # Обновление игры
                        if not event.key == pygame.K_ESCAPE:
                            board.win = False
                            board.timer = - 1
                            board.board = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
                            board.k = 0
                    if board.win and board.timer > 12 and event.type == pygame.MOUSEBUTTONDOWN:  # Обновление игры
                        board.win = False
                        board.timer = - 1
                        board.board = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
                        board.k = 0
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Выход в меню
                        running = False
                        pygame.quit()
                        start()
                if running:
                    screen.fill(pygame.Color((255, 255, 255)))
                    board.render()
                    pygame.display.flip()
            pygame.quit()
        elif 275 < x < 530 and 350 < y < 385:
            black = (0, 0, 0)
            clock = pygame.time.Clock()
            win_width = 800
            win_height = 640
            max_score = 10
            display = (win_width, win_height)
            pygame.init()
            screen = pygame.display.set_mode(display, 0, 32)
            done = False
            fps = 30
            all_sprites_pp = pygame.sprite.Group()
            camouflage = pygame.sprite.Sprite(all_sprites_pp)
            camouflage.image = load_image('field.png')
            camouflage.rect = camouflage.image.get_rect()
            camouflage.rect.topleft = [0, 0]
            left_player = Player(Directions.LEFT, 'Left')
            right_player = Player(Directions.RIGHT, 'Right')
            curr_ball = Ball(screen, win_width, win_height)
            left_racket = Racketka(screen, win_width, win_height, Directions.LEFT)
            right_racket = Racketka(screen, win_width, win_height, Directions.RIGHT)
            rackets = pygame.sprite.Group()
            rackets.add(left_racket)
            rackets.add(right_racket)
            stuff_to_draw = pygame.sprite.Group()
            stuff_to_draw.add(left_racket)
            stuff_to_draw.add(right_racket)
            while not done:
                screen.fill(black)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:  # Выход в меню
                        done = True
                        pygame.quit()
                        start()
                all_sprites_pp.draw(screen)
                pygame.event.pump()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_q]:
                    done = True
                if keys[pygame.K_UP]:
                    right_racket.move_up()
                if keys[pygame.K_DOWN]:
                    right_racket.move_down()
                if keys[pygame.K_w]:
                    left_racket.move_up()
                if keys[pygame.K_s]:
                    left_racket.move_down()

                stuff_to_draw.update()
                curr_ball.update()

                col_left, col_right = curr_ball.rect.colliderect(left_racket.rect), curr_ball.rect.colliderect(
                    right_racket.rect)
                if col_right == 1 or col_left == 1:
                    curr_ball.toggle_direction()
                    curr_ball.hit()

                if curr_ball.get_x_val() <= 0:  # left border
                    right_player.score = 1
                    curr_ball = Ball(screen, win_width, win_height)
                elif curr_ball.get_x_val() >= win_width:  # right border
                    left_player.score = 1
                    curr_ball = Ball(screen, win_width, win_height)

                # Print scores
                font = pygame.font.SysFont('Helvetica', 25)

                left_player_score = font.render(
                    '{}'.format(left_player.score), True, (255, 255, 255))
                right_player_score = font.render(
                    '{}'.format(right_player.score), True, (255, 255, 255))
                goal_text = font.render(
                    '{}'.format(max_score), True, (255, 255, 0))

                screen.blit(left_player_score, (win_width / 2 - 100, 10))
                screen.blit(right_player_score, (win_width / 2 + 100, 10))
                screen.blit(goal_text, (win_width / 2, 0))

                stuff_to_draw.draw(screen)
                curr_ball.draw(screen)

                if left_player.score >= max_score:
                    game_over(screen, left_player, left_player, right_player)
                elif right_player.score >= max_score:
                    game_over(screen, right_player, left_player, right_player)
                if left_player.score >= max_score or right_player.score >= max_score:
                    done = True

                pygame.display.set_caption('ПИНГ-ПОНГ ' + str(clock.get_fps()))

                pygame.display.flip()
                clock.tick(fps)


def start():  # Функция вызова менюшки
    pygame.init()
    pygame.display.set_caption('Меню')
    size = 800, 600
    screen_menu = pygame.display.set_mode(size)
    running1_m = True
    while running1_m:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_on(event.pos)
            if event.type == pygame.QUIT:
                sys.exit()
            if running1_m is True:
                draw(screen_menu)
            pygame.display.flip()
    pygame.quit()


start()
