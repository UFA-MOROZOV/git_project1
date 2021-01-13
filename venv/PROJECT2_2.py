import pygame
import os
from enum import Enum
import random


black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (64, 64, 64)
clock = pygame.time.Clock()


class Ball(pygame.sprite.Sprite):
    def __init__(self, screen_b, width, height):
        super().__init__()
        granata_img = load_image('granata_p_50.png')
        self.width, self.height = width, height
        self.direction = random.choice([Directions.DOWN_LEFT, Directions.DOWN_RIGHT, Directions.UP_LEFT,
                                        Directions.UP_RIGHT])
        self.screen = screen_b
        self.image = granata_img
        self.rect = self.image.get_rect()
        self.position = (width / 2 + 2, height / + 2)
        self.hits = 0
        self.speed_up = 1.0

    def draw(self, screen_d):
        screen_d.blit(self.image, self.rect)

    def hit(self):
        self.hits += 1
        self.speed_up = 1.0+self.hits/10

    @property
    def position(self):
        return self.rect.x, self.rect.y

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def up_left(self):
        self.position = (self.position[0] - 10*self.speed_up, self.position[1] - 10*self.speed_up)

    def up_right(self):

        self.position = (self.position[0] + 10*self.speed_up, self.position[1] - 10*self.speed_up)

    def down_left(self):

        self.position = (self.position[0] - 10*self.speed_up, self.position[1] + 10*self.speed_up)

    def down_right(self):

        self.position = (self.position[0] + 10*self.speed_up, self.position[1] + 10*self.speed_up)

    def update(self):
        if self.position[1] <= 10:  # upper border
            self.direction = random.choice(
                [Directions.DOWN_LEFT, Directions.DOWN_RIGHT])
        if self.position[1] >= self.height - 10:  # bottom border
            self.direction = random.choice(
                [Directions.UP_LEFT, Directions.UP_RIGHT])

        options = {Directions.UP_LEFT: self.up_left,
                   Directions.UP_RIGHT: self.up_right,
                   Directions.DOWN_LEFT: self.down_left,
                   Directions.DOWN_RIGHT: self.down_right,
                   }
        options[self.direction]()

    def toggle_direction(self):
        if self.direction == Directions.DOWN_LEFT:
            new_direction = Directions.DOWN_RIGHT

        elif self.direction == Directions.DOWN_RIGHT:
            new_direction = Directions.DOWN_LEFT

        elif self.direction == Directions.UP_RIGHT:
            new_direction = Directions.UP_LEFT

        elif self.direction == Directions.UP_LEFT:
            new_direction = Directions.UP_RIGHT
        else:
            new_direction = None
        try:
            self.direction = new_direction
        except NameError:
            pass

    def get_x_val(self):
        return self.rect.x


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


class Directions(Enum):
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = 1
    DOWN_RIGHT = 3
    LEFT = 3
    RIGHT = 6


class Racketka(pygame.sprite.Sprite):

    def __init__(self, screen_r, width, height, side):
        super().__init__()
        if side == Directions.DOWN_RIGHT:
            racketka_img = load_image('soldat_p_68_100.png')
        else:
            racketka_img = load_image('nazi_soldat.png')
        self.width, self.height = width, height
        self.racket_height = 100
        self.movement_speed = 20
        offset = 5
        self.screen = screen_r
        self.image = racketka_img
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        if side is Directions.LEFT:
            self.position = (offset, self.height / 2)
        else:
            self.position = (self.width - offset - 68, self.height / 2)

    @property
    def position(self):
        return self.rect.x, self.rect.y

    @position.setter
    def position(self, pos):
        try:
            pos_x, pos_y = pos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            self.rect.x, self.rect.y = pos_x, pos_y

    def move_up(self):
        if self.position[1] > 0:
            self.position = (self.position[0], self.position[1] - self.movement_speed)

    def move_down(self):
        if self.position[1] + self.racket_height < self.height:
            self.position = (self.position[0], self.position[1] + self.movement_speed)


class Player:

    def __init__(self, side, name):
        self.side = side
        self.points = 0
        self.name = name

    @property
    def score(self):
        return self.points

    @score.setter
    def score(self, val):
        self.points += val


win_width = 800
win_height = 640
display = (win_width, win_height)
left_player = Player(Directions.LEFT, 'Left')
right_player = Player(Directions.RIGHT, 'Right')


def game_over(screen_go, winner, left_paper, right_player_go):
    grey_overlay = pygame.Surface((win_width, win_height))
    grey_overlay.fill(grey)
    grey_overlay.set_colorkey(grey)
    pygame.draw.rect(grey_overlay, black, [0, 0, win_width, win_height])
    grey_overlay.set_alpha(99)
    screen_go.blit(grey_overlay, (0, 0))
    font_go = pygame.font.SysFont('data/Arial.ttf', 100)
    text = ''
    if winner.name.upper() == 'LEFT':
        text = 'Игрок 1 победил!'
    elif winner.name.upper() == 'RIGHT':
        text = 'Игрок 2 победил!'
    game_over1 = font_go.render(text, True, white)
    screen_go.blit(game_over1, (win_width / 2 - 300, win_height / 2 - 100))
    scoreline = font_go.render(
        '{} - {}'.format(left_paper.score, right_player_go.score), True, white)
    screen_go.blit(scoreline, (win_width / 2 - 50, win_height / 2 + 100))
    pygame.display.update()
    pygame.time.delay(2000)
