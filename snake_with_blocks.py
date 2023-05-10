import pygame
from pygame.math import Vector2
from random import randint


def check_fruit_position(fruit, blocks, snake):
    if fruit.pos in snake.body:
        return True

    for block in blocks:
        if block.pos == fruit.pos:
            return True

    return False


def check_block_position(new_block, block_list, fruit, snake):
    if new_block.pos in snake.body:
        return True

    if new_block.pos == fruit.pos:
        return True

    if new_block.pos in block_list:
        return True

    return False


class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            # create a rect
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            # draw the rect
            pygame.draw.rect(screen, '#006B6D', block_rect)

    def move_snake(self):
        if self.direction.x != 0 or self.direction.y != 0:
            if self.new_block:
                body_copy = self.body
                body_copy.insert(0, body_copy[0] + self.direction)
                self.body = body_copy[:]
                self.new_block = False
            else:
                body_copy = self.body[:-1]
                body_copy.insert(0, self.body[0] + self.direction)
                self.body = body_copy[:]

    def add_block(self):
        self.new_block = True


class Fruit:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        x_pos = int(self.x * cell_size)
        y_pos = int(self.y * cell_size)
        fruit_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, '#00CCE8', fruit_rect)

    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Block:
    def __init__(self):
        self.randomize()

    def draw_block(self):
        x_pos = int(self.x * cell_size)
        y_pos = int(self.y * cell_size)
        block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
        pygame.draw.rect(screen, '#454839', block_rect)

    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.blocks = []
        self.determine_block = 0
        self.running = True

    def draw_elements(self):
        for block in self.blocks:
            block.draw_block()

        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:

            # add another block to the snake
            self.snake.add_block()

            # add block to map
            self.determine_block += 1
            if self.determine_block == 3:
                temp_block = Block()
                while check_block_position(temp_block, self.blocks, self.fruit, self.snake):
                    temp_block.randomize()

                self.blocks.append(temp_block)
                self.determine_block = 0

            # reposition the fruit
            self.fruit.randomize()
            while check_fruit_position(self.fruit, self.blocks, self.snake):
                self.fruit.randomize()

    def check_fail(self):
        # Ends game if snake hits wall
        if not 0 <= self.snake.body[0].x < cell_number \
                or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        # Ends game if snake hits itself
        for block in self.snake.body[1:]:
            if self.snake.body[0].x == block.x and \
                    self.snake.body[0].y == block.y:
                self.game_over()

        # Ends game if snake hits block
        for block in self.blocks:
            if self.snake.body[0].x == block.x and \
                    self.snake.body[0].y == block.y:
                self.game_over()

    def game_over(self):
        self.running = False

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = font.render(score_text, True, (56, 74, 12))

        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 60
        score_rect = score_surf.get_rect(center=(score_x, score_y))
        screen.blit(score_surf, score_rect)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


pygame.init()
cell_size = 30
cell_number = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)
score = 0

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()

while main_game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_game.game_over()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_game.game_over()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction != Vector2(0, 1):
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN and main_game.snake.direction != Vector2(0, -1):
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction != Vector2(1, 0):
                main_game.snake.direction = Vector2(-1, 0)
            if event.key == pygame.K_RIGHT and main_game.snake.direction != Vector2(-1, 0):
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_SPACE:
                main_game.snake.direction = Vector2(0, 0)

    screen.fill((175, 215, 70))
    main_game.draw_elements()

    pygame.display.update()
    clock.tick(60)
