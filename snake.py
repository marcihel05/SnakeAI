import numpy as np
import tenserflow as tf
from tf import keras
from keras import Sequential
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import timeimport random

WIN_WIDTH = 600
WIN_HEIGHT = 600

RECT_DIM = 20

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

INPUT = 24
HIDDEN = 18
OUTPUT = 4

LEFT = 'l'
RIGHT = 'r'
UP = 'u'
DOWN = 'd'


class Snake():
    def __init__(self):
        self.x = WIN_WIDTH-100
        self.y = 300
        self.tail = [(self.x+RECT_DIM, self.y), (self.x+2*RECT_DIM, self.y)]
        self.len = 3 #length of snake = 1+ len(self.tail)
        self.dir = (0,0) #direction of movement
        self.food = Food()
        self.brain = Brain(INPUT, HIDDEN, OUTPUT) #neural network
        self.fitness = 0
        self.lifetime = 0
        self.leftToLive = 200 #to prevent infinite loops
        self.score = 0
        self.dead = False
        self.vision = [] #input of network
        self.decision = [] #output of network

    
    def move(win, self):
        self.lifetime+=1
        self.leftToLive-=1
        if self.leftToLive < 0:
            self.dead = True
            return
        
        self.x += self.dir[0]
        self.y += self.dir[1]

        if self.collide(win, (self.food.x, self.food.y))
            self.eat()

        if not self.crash(win):
            self.moveTail()


    
    def moveTail(self):
        pos = (self.x, self.y)-self.dir
        for i in reversed(range(1, self.len-1)):
            self.tail[i] = self.tail[i-1]
        self.tail[0] = pos



    def grow(self):
        last = self.tail[(self.len)-2]
        if last[0] == self.x:
            if last[1] > self.y: #end in below head
                pos = (last[0], last[1]+RECT_DIM)
            else: #end is above head
                pos = (last[0], last[1]-RECT_DIM)

        if last[0] < self.x:
            if last[1] == self.y: #moving to right
                pos = (last[0]-RECT_DIM, last[1])
            if last[1] > self.y: #
                pos = (last[0]-RECT_DIM, last[1])
            if last[1] < self.y:
                pos = (last[0], last[1]- RECT_DIM)
        
        if last[0] > self.x:
            if last[1] == self.y:# moving to left
                pos = (last[0] + RECT_DIM, last[1])
            if last[1] > self.y:
                pos = (last[0] + RECT_DIM, last[1])
            if last[1] < self.y:
                pos = (last[0], last[1] - RECT_DIM)

        self.tail.append(pos)


    def eat(self):
        self.score+=1
        self.food = Food()
        self.grow()

    def collide(self, win, pos):
        snake_rect = pygame.draw.rect(win, GREEN, (self.x, self.y, RECT_DIM, RECT_DIM))
        obj_rect = pygame.draw.rect(win, BLACK, (pos[0], pos[1], RECT_DIM, RECT_DIM))
        if snake_rect.colliderect(obj_rect):
            return True
    
    def crashIntoSelf(self, win):
        for i in range (1, self.len-2):
            if self.collide(win, (self.tail[i][0], self.tail[i][1]):
                return True
        return False

    
    def crash(self, win):
        if self.crashIntoSelf(win):
            return True
        if self.x > WIN_WIDTH or self.x <0 or self.y < 0 or self.y > WIN_HEIGHT:
            self.dead = True


    def whatISee(self, win): #vision of snake
        new_vision = self.look((RECT_DIM, 0), win) #right
        self.vision[0] = new_vision[0]
        self.vision[1] = new_vision[1]
        self.vision[2] = new_vision[2]
        
        new_vision = self.look((RECT_DIM, RECT_DIM), win) #right-down
        self.vision[3] = new_vision[0]
        self.vision[4] = new_vision[1]
        self.vision[5] = new_vision[2]
       
        new_vision = self.look((0, RECT_DIM), win) #down
        self.vision[6] = new_vision[0]
        self.vision[7] = new_vision[1]
        self.vision[8] = new_vision[2]
        
        new_vision = self.look((-RECT_DIM, 0), win) #left
        self.vision[9] = new_vision[0]
        self.vision[10] = new_vision[1]
        self.vision[11] = new_vision[2]
        
        new_vision = self.look((-RECT_DIM, -RECT_DIM), win) #left-up
        self.vision[12] = new_vision[0]
        self.vision[13] = new_vision[1]
        self.vision[14] = new_vision[2]
       
        new_vision = self.look((0, -RECT_DIM), win) #up
        self.vision[15] = new_vision[0]
        self.vision[16] = new_vision[1]
        self.vision[17] = new_vision[2]
        
        new_vision = self.look((RECT_DIM, -RECT_DIM), win) #right-up
        self.vision[18] = new_vision[0]
        self.vision[19] = new_vision[1]
        self.vision[20] = new_vision[2]
       
        new_vision = self.look((-RECT_DIM, RECT_DIM), win) #left-down
         elf.vision[21] = new_vision[0]
        self.vision[22] = new_vision[1]
        self.vision[23] = new_vision[2]       


    def look(self, dir, win):
        vision = [] # (food, tail, wall)
        dist = 0
        pos = (self.x, self.y)
        food_pos = (self.food.x, self.food.y)
        foodSeen = False
        tailSeen = False

        while pos[0] < WIN_WIDTH and pos[0] > 0 and pos[1] >0 and pos[1] < WIN_HEIGHT:
            ++dist
            pos +=dir
            if not foodSeen and self.collide(win, food_pos):
                foodSeen = True
                vision[0] = 1
            if not tailSeen and self.crashIntoSelf(win):
                tailSeen = True
                vision[1] = 1/dist
        vision[2] = 1/dist
        return vision


    def crossover(self, partner):
        new_wights_1 = self.brain.crossoverInputToHidden(partner.brain)
        new_wights_2 = self.brain.crossoverHiddenToInput(partner.brain)
        child_weights = [new_wights_1, new_wights_2]

    def draw(self,win):
        pygame.draw.rect(win, GREEN, (self.x, self.y, RECT_DIM, RECT_DIM))
        for part in self.tail:
          pygame.draw.rect(win, GREEN, (part[0], part[1], RECT_DIM, RECT_DIM))
        self.food.draw(win)

class Food:

    def __init__(self):
        random.seed(time.time())
        self.x = random.randrange(40, WIN_WIDTH-50)
        self.y = random.randrange(40, WIN_WIDTH-50)
    
    def draw(self,win):
        pygame.draw.rect(win, RED, (self.x, self.y, RECT_DIM, RECT_DIM))