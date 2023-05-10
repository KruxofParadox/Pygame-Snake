import pygame
from pygame.math import Vector2 as Vec
from random import randint
from constants import *


class Fruit:
    def __init__(self, screen):
        self.randomize()
        self.screen = screen

    def draw_fruit(self):
        x_pos = self.pos.x * CELL_SIZE + W_OFFSET
        y_pos = self.pos.y * CELL_SIZE + H_OFFSET
        fruit_rect = pygame.Rect((x_pos, y_pos), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(self.screen, RED, fruit_rect)

    def randomize(self):
        self.x = randint(0, CELL_NUMBER-1)
        self.y = randint(0, CELL_NUMBER-1)
        self.pos = Vec(self.x, self.y)
