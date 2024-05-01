import pygame
import time
import random
from enum import Enum


class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4


class GameOverException(Exception):
    pass


bg_color = "black"


class Game:

    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((750, 750))
        self.snake = Snake(self.win, 1)
        self.snake.draw()
        self.food = Food(self.win)
        self.border_color = "white"
        self.running = True
        self.pause = False
        self.pause_snake = True
        self.font = pygame.font.SysFont('impact', 28)

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + self.snake.size:
            if y2 <= y1 < y2 + self.snake.size:
                return True
        return False

    def draw_border(self):
        pygame.draw.rect(self.win, self.border_color, (0, 0, self.win.get_width(), 60))
        pygame.draw.rect(self.win, self.border_color, (0, self.win.get_height() - 60, self.win.get_width(), 60))
        pygame.draw.rect(self.win, self.border_color, (0, 0, 60, self.win.get_height()))
        pygame.draw.rect(self.win, self.border_color, (self.win.get_width() - 60, 0, 60, self.win.get_height()))

    def play(self):
        if not self.pause_snake:
            self.snake.walk()
        self.food.draw()
        self.draw_border()
        self.display_score()

        # checks if snake collides with food, then moves the food and increases the snake's length
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.food.move()
            self.snake.increase_length()

        # checks if snake collides with itself, then ends game
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise GameOverException

        # checks if snake collides with the border, then ends game
        if self.is_border_collision(self.snake.x[0], self.snake.y[0]):
            raise GameOverException

        pygame.display.flip()

    def display_score(self):
        score = self.font.render(f"Score: {self.snake.length}", True, "black")
        self.win.blit(score, (600, 10))

    def run(self):
        # Loop that runs the game until user closes window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if self.snake.direction != Direction.DOWN:
                            self.snake.direction = Direction.UP
                        self.pause_snake = False
                    if event.key == pygame.K_DOWN:
                        if self.snake.direction != Direction.UP:
                            self.snake.direction = Direction.DOWN
                        self.pause_snake = False
                    if event.key == pygame.K_LEFT:
                        if self.pause_snake or self.snake.direction != Direction.RIGHT:
                            self.snake.direction = Direction.LEFT
                        self.pause_snake = False
                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction != Direction.LEFT:
                            self.snake.direction = Direction.RIGHT
                        self.pause_snake = False
            try:
                if not self.pause:
                    self.play()
            except GameOverException:
                self.end_game()
                self.pause = True

            time.sleep(0.2)

    def is_border_collision(self, snake_x, snake_y):
        if snake_x < 60 or snake_x > self.win.get_width() - 90:
            return True
        if snake_y < 60 or snake_y > self.win.get_height() - 90:
            return True
        return False

    def end_game(self):
        self.win.fill(bg_color)
        font = pygame.font.SysFont('impact', 90)
        line1 = font.render("Game Over!", True, "white")
        line2 = font.render(f"Your score is {self.snake.length}", True, "white")
        font = pygame.font.SysFont('impact', 60)
        restart_text = font.render("Restart", True, "white")
        quit_text = font.render("Quit", True, "white")
        restart_text_hover = font.render("Restart", True, "lime")
        quit_text_hover = font.render("Quit", True, "lime")
        self.win.blit(line1, ((self.win.get_width() - line1.get_width()) / 2, 150))
        self.win.blit(line2, ((self.win.get_width() - line2.get_width()) / 2, 250))
        restart_button = self.win.blit(restart_text, (self.win.get_width() * 0.2, 450))
        quit_button = self.win.blit(quit_text, (self.win.get_width() * 0.65, 450))
        pygame.display.flip()

        end_game = True
        while end_game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                mouse_pos = pygame.mouse.get_pos()
                if quit_button.collidepoint(mouse_pos):
                    quit_button = self.win.blit(quit_text_hover, (self.win.get_width() * 0.65, 450))
                elif restart_button.collidepoint(mouse_pos):
                    restart_button = self.win.blit(restart_text_hover, (self.win.get_width() * 0.2, 450))
                else:
                    restart_button = self.win.blit(restart_text, (self.win.get_width() * 0.2, 450))
                    quit_button = self.win.blit(quit_text, (self.win.get_width() * 0.65, 450))
                pygame.display.flip()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.collidepoint(mouse_pos):
                        exit()
                    if restart_button.collidepoint(mouse_pos):
                        self.pause = False
                        end_game = False
        game.__init__()
        game.run()


class Snake:
    def __init__(self, window, length):
        self.length = length
        self.color = "lime"
        self.size = 30
        self.start_x = 300
        self.start_y = 300
        self.x = [self.start_x] * self.length
        self.y = [self.start_y] * self.length
        self.window = window
        self.direction = Direction.RIGHT

    def draw(self):
        self.window.fill(bg_color)
        for i in range(self.length):
            pygame.draw.rect(self.window, self.color, (self.x[i], self.y[i], self.size, self.size))

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == Direction.RIGHT:
            self.x[0] += 30
        elif self.direction == Direction.LEFT:
            self.x[0] -= 30
        elif self.direction == Direction.UP:
            self.y[0] -= 30
        else:
            self.y[0] += 30
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Food:
    def __init__(self, window):
        self.size = 30
        self.color = "red"
        self.x = 90
        self.y = 90
        self.window = window

    def draw(self):
        pygame.draw.rect(self.window, self.color, (self.x, self.y, self.size, self.size))

    def move(self):
        self.x = random.randint(2, self.window.get_width() / 30 - 3) * 30
        self.y = random.randint(2, self.window.get_height() / 30 - 3) * 30


class Button:
    def __init__(self, window, text):
        self.size = (60, 30)
        self.window = window
        self.text = text


game = Game()
game.run()

pygame.quit()
