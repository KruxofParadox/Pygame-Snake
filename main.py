import pygame
from fruit import Fruit
from snake import Snake
from constants import *


class Main:
    def __init__(self):
        self.running = True
        self.fruit = Fruit(screen)
        self.snake = Snake(screen)
        self.frame_iteration = 0

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

        for segment in self.snake.body[1:]:
            if segment == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 < self.snake.body[0].x < CELL_NUMBER \
                or not 0 <= self.snake.body[0].y < CELL_NUMBER:
            self.game_over()

        for segment in self.snake.body[1:]:
            if self.snake.body[0] == segment:
                self.game_over()

    def game_over(self):
        self.running = False

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surf = font.render('{}{}'.format('Score: ', score_text), True, WHITE)

        score_x = 0
        score_y = 0

        score_rect = score_surf.get_rect(topleft=(score_x, score_y))
        screen.blit(score_surf, score_rect)

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()


if __name__ == "__main__":
    # << BASIC INITIALIZATION >>
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')

    # << GAME VARIABLES >>
    clock = pygame.time.Clock()
    font = pygame.font.SysFont('monospace', 14)
    main_game = Main()

    # << TIMERS >>
    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    # << GAME LOOP >>
    while main_game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_game.game_over()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                main_game.game_over()

            if event.type == SCREEN_UPDATE:
                main_game.update()

            if event.type == pygame.KEYDOWN:
                main_game.snake.update(event)

        screen.fill(BLACK)
        rect_size = (W_OFFSET, H_OFFSET, GAME_SIZE, GAME_SIZE)
        pygame.draw.rect(screen, WHITE, rect_size, 1)
        main_game.draw_elements()

        pygame.display.update()
        clock.tick(60)

