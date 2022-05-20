from collections import namedtuple
from tarfile import DIRTYPE
from matplotlib.pyplot import draw
import pygame
from enum import Enum
import random 
from collections import namedtuple

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple("Point",'x,y')
BLOCK_SIZE = 20
SPEED = 2

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (200,0,0)
BLUE1 = (0,0,255)
BLUE2 = (0,100,255)

#initialize all the modules
pygame.init()
font = pygame.font.SysFont('Arial',25)

class SnakeGame():
    def __init__(self, w= 640, h=480):
        self.w = w
        self.h = h
        self.speed = SPEED

        #init display
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("Snake Game")

        #Control the speed of the game
        self.clock = pygame.time.Clock()

        #init game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w/2,self.h/2)
        self.snake = [self.head,
                    Point(self.head.x-BLOCK_SIZE,self.head.y),
                    Point(self.head.x - (2*BLOCK_SIZE),self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()


    def _place_food(self):
        x = random.randint(0,(self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0,(self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # Collect User input and 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # move Snake
        self._move(self.direction)
        self.snake.insert(0,self.head)

        # Check if game over
        game_over = False
        if self._iscollision():
            game_over = True
            return game_over, self.score

        # Place new food or just move
        if self.head == self.food:
            self.score += 1
            self.speed += 0.5
            self._place_food()
        else:
            self.snake.pop()

        # Update UI and Clock
        self._update_ui()
        self.clock.tick(self.speed)
        # Return game over and score
        return game_over,self.score
    
    def _iscollision(self):
        #if self.head.x > self.w- BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h-BLOCK_SIZE or self.head.y < 0 :
            #return True
        if self.head in self.snake[1:]:
            return True 
        elif self.head.x > self.w-BLOCK_SIZE:
            self.head = Point(0,self.head.y)
        elif self.head.x < 0:
            self.head = Point(self.w - BLOCK_SIZE,self.head.y)
        elif self.head.y > self.h - BLOCK_SIZE:
            self.head = Point(self.head.x, 0)
        elif self.head.y < 0:
            self.head = Point(self.head.x,self.h - BLOCK_SIZE)            


    def _move(self, direction):
        # Snake Head is updated
        x = self.head.x
        y = self.head.y
        #print(direction)
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x,y)

    
    def _update_ui(self):
        self.display.fill(BLACK)
        for pt in self.snake:
            pygame.draw.rect(self.display,BLUE1, pygame.Rect(pt.x,pt.y,BLOCK_SIZE,BLOCK_SIZE))
            pygame.draw.rect(self.display,BLUE2,pygame.Rect(pt.x+4,pt.y+4,12,12))
        #print(str(self.food))
        pygame.draw.rect(self.display,RED,pygame.Rect(self.food.x,self.food.y,BLOCK_SIZE,BLOCK_SIZE))
        text = font.render("Score: "+ str(self.score),True,WHITE)
        self.display.blit(text,[0,0])
        pygame.display.flip()

if __name__ =="__main__":
    snakegame = SnakeGame()
    #print(snakegame.score)
    #print(str(snakegame.food))
    while True:
        game_over, score = snakegame.play_step()
        if game_over == True:
            break
    print("Final Score is :",score)

    pygame.quit()