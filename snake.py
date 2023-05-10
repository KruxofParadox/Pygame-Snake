import pygame
from pygame.math import Vector2 as Vec
from constants import *


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.body = [
            Vec(CELL_SIZE//2, CELL_SIZE//2),
            Vec(CELL_SIZE//2-1, CELL_SIZE//2),
            Vec(CELL_SIZE//2-1, CELL_SIZE//2)
        ]
        self.direction = Vec(0, 0)
        self.new_block = False

    def draw_snake(self):
        for segment in self.body:
            x_pos = segment.x * CELL_SIZE + W_OFFSET
            y_pos = segment.y * CELL_SIZE + H_OFFSET
            segment_rect = pygame.Rect((x_pos, y_pos), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, WHITE, segment_rect)

    def move_snake(self):
        if self.direction.x != 0 or self.direction.y != 0:
            if self.new_block: body_copy = self.body
            else: body_copy = self.body[:-1]

            body_copy.insert(0, self.body[0] + self.direction)
            self.body = body_copy
            self.new_block = False

    def add_block(self):
        self.new_block = True

    def update(self, event):
        if event.key == pygame.K_UP and \
                self.direction != Vec(0, 1):
            self.direction = Vec(0, -1)
        elif event.key == pygame.K_DOWN and \
                self.direction != Vec(0, -1):
            self.direction = Vec(0, 1)
        elif event.key == pygame.K_LEFT and \
                self.direction != Vec(1, 0):
            self.direction = Vec(-1, 0)
        elif event.key == pygame.K_RIGHT and \
                self.direction != Vec(-1, 0):
            self.direction = Vec(1, 0)
