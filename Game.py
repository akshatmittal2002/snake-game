import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()

class Directions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    LIGHTBLUE = (0, 150, 255)

Point = namedtuple('Point', 'x, y')
font = pygame.font.Font('NotoSans-Regular.ttf', 20)


BLOCK_SIZE = 20
SPEED = 8

class SnakeGame:

    def __init__(self, width= 640, height= 480):
        self.width = width
        self.height = height

        #initialise game display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()

        #initialise game state
        self.direction = Directions.RIGHT
        
        self.head = Point(self.width // 2, self.height // 2)

        self.snake = [self.head, 
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2 * BLOCK_SIZE, self.head.y)]

        self.score = 0

        self.increments = 0
        self.speed = SPEED

        self.food = None

        self._generate_food()

    def _generate_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)

        if self.food in self.snake:
            self._generate_food()
        
    def play(self):
        # Collecting user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.direction = Directions.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Directions.DOWN
                elif event.key == pygame.K_LEFT:
                    self.direction = Directions.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Directions.RIGHT

        # Moving ahead 
        self._step(self.direction) 
        self.snake.insert(0, self.head)

        # Checking if game is over
        game_over = False
        if self._is_game_over():
            game_over = True
            return game_over, self.score

        # Checking if snake ate food
        if self.head == self.food:
            self.score += 1
            self._generate_food()
        else:
            self.snake.pop()

        new_increment = self.score // 10

        if new_increment > self.increments:
            self.increments = new_increment
            self.speed += 1

        self._update_ui()
        self.clock.tick(self.speed)

        return game_over, self.score
        

    def _update_ui(self):
        self.display.fill(Colors.BLACK)

        # Drawing snake
        for pt in self.snake:
            pygame.draw.rect(self.display, Colors.BLUE, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            small_block = int(BLOCK_SIZE * 0.8)
            border = BLOCK_SIZE - small_block
            pygame.draw.rect(self.display, Colors.LIGHTBLUE, pygame.Rect(pt.x + border, pt.y + border, small_block, small_block))
        
        # Drawing food
        pygame.draw.rect(self.display, Colors.RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Printing score
        text = font.render(f'Score: {self.score}', True, Colors.WHITE)
        self.display.blit(text, [0, 0])

        pygame.display.flip()

    def _step(self,direction):
        x = self.head.x
        y = self.head.y

        if (direction == Directions.UP):
            y -= BLOCK_SIZE
        elif (direction == Directions.DOWN):
            y += BLOCK_SIZE
        elif (direction == Directions.LEFT):
            x -= BLOCK_SIZE
        elif (direction == Directions.RIGHT):
            x += BLOCK_SIZE

        self.head = Point(x, y)

    def _is_game_over(self):
        return (self.head.x > self.width - BLOCK_SIZE 
                or self.head.x < 0 
                or self.head.y > self.height - BLOCK_SIZE
                or self.head.y < 0) or (self.head in self.snake[1:])

                

if __name__ == "__main__":
    Game = SnakeGame()
    
    while True:
        game_over, score = Game.play()

        if (game_over):
            break

    print(f'Game over! Your score is {score}')

    pygame.quit()