import numpy as np
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
from brain import Brain
from matrix import Matrix

GAME_WIDTH = 800
GAME_HEIGHT = 800

RECT_DIM = 20

VELOCITY = 20

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

INPUT = 24
HIDDEN = 16
OUTPUT = 4


class Snake():
    def __init__(self):
        self.x = GAME_WIDTH/2
        self.y = GAME_HEIGHT/2
        self.tail = [[self.x, self.y+RECT_DIM], [self.x, self.y+2*RECT_DIM],[self.x, self.y+3*RECT_DIM]]
        self.len = 4 #length of snake = 1+ len(self.tail)
        self.vel = [0, -VELOCITY] #direction of movement
        self.food = self.set_food()
        self.brain = Brain() #Brain()#neural network
        self.fitness = 0
        self.lifetime = 0
        self.leftToLive = 200 #to prevent infinite loops
        self.allowToLive = 200
        self.score = 0
        self.dead = False
        self.vision = np.zeros((24,1)) #input of network
        self.decision = np.zeros((4,1)) #output of network

    
    def think(self,win):
        self.decision = self.brain.procces(self.vision)
       
    
    def move(self, win):
        self.lifetime+=1
        self.leftToLive-=1
        if self.leftToLive < 0:
            self.dead = True
            return

        direction = np.argmax(self.decision)

        if direction == 0: #left
            if not self.vel == [VELOCITY, 0]:
                self.vel = [-VELOCITY, 0]
                #self.vel = [0,0]
                #self.dead = True
            #else:
                
        
        if direction == 1: #up
            if not self.vel == [0, VELOCITY]:
                self.vel = [0, -VELOCITY]
                #self.vel = [0,0]
                #self.dead = True
            #else:
                
        
        if direction == 2: #right
            if not self.vel == [-VELOCITY, 0]:
                self.vel = [VELOCITY, 0]
               # self.vel = [0,0]
               # self.dead = True
            #else:
                

        if direction == 3: #down
            if not self.vel == [0, -VELOCITY]:
                self.vel = [0, VELOCITY]
                #self.vel = [0,0]
                #self.dead = True
            #else:
                
       # if self.vel == [0,0]:
        #    return
        #else:
        self.moveTail()
        self.x += self.vel[0]
        self.y += self.vel[1]
        

        #if self.collide([self.food.x, self.food.y]):
        self.eat(win) #check if ir found food

        self.crash(win) #check if it crashed
            
    def moveTail(self):
        #pos = [self.x-self.vel[0], self.y-self.vel[1]]
        i = self.len -2
        while i > 0:
            self.tail[i] = self.tail[i-1]
            i-=1
        self.tail[0] = [self.x, self.y]
        #self.tail[0] = pos


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
        self.len+=1


    def eat(self,win):
        if self.x == self.food.x and self.y == self.food.y:
            self.leftToLive +=100
            self.allowToLive+=100
            self.score+=1
            self.food = self.set_food()
            self.grow()

    
    def crashIntoSelf(self, x = "", y = ""):
        if not x and not y:
            x = self.x
            y = self.y
        for part in self.tail:
            if x == part[0] and y == part[1]:
                return True
        return False

    
    def crash(self, win):
        if self.crashIntoSelf():
            self.dead = True
        if self.x > GAME_WIDTH-RECT_DIM or self.x <0 or self.y < 0 or self.y > GAME_HEIGHT-RECT_DIM:
            self.dead = True


    def look(self, win): #vision of snake (input of neural net)

        new_vision = self.whatISee((VELOCITY, 0), win) #right
        self.vision[0] = new_vision[0]
        self.vision[1] = new_vision[1]
        self.vision[2] = new_vision[2]
        
        new_vision = self.whatISee((VELOCITY, VELOCITY), win) #right-down
        self.vision[3] = new_vision[0]
        self.vision[4] = new_vision[1]
        self.vision[5] = new_vision[2]
       
        new_vision = self.whatISee((0, VELOCITY), win) #down
        self.vision[6] = new_vision[0]
        self.vision[7] = new_vision[1]
        self.vision[8] = new_vision[2]
        
        new_vision = self.whatISee((-VELOCITY, 0), win) #left
        self.vision[9] = new_vision[0]
        self.vision[10] = new_vision[1]
        self.vision[11] = new_vision[2]
        
        new_vision = self.whatISee((-VELOCITY, -VELOCITY), win) #left-up
        self.vision[12] = new_vision[0]
        self.vision[13] = new_vision[1]
        self.vision[14] = new_vision[2]
       
        new_vision = self.whatISee((0, -VELOCITY), win) #up
        self.vision[15] = new_vision[0]
        self.vision[16] = new_vision[1]
        self.vision[17] = new_vision[2]
        
        new_vision = self.whatISee((VELOCITY, -VELOCITY), win) #right-up
        self.vision[18] = new_vision[0]
        self.vision[19] = new_vision[1]
        self.vision[20] = new_vision[2]
       
        new_vision = self.whatISee((-VELOCITY, VELOCITY), win) #left-down
        self.vision[21] = new_vision[0]
        self.vision[22] = new_vision[1]
        self.vision[23] = new_vision[2]       

    def whatISee(self, dir, win):
        vision = [0,0,0] # (food, tail, wall)
        dist = 1
        pos = [self.x, self.y]
        food_pos = [self.food.x, self.food.y]
        foodSeen = False
        tailSeen = False

        while pos[0] < GAME_WIDTH and pos[0] > 0 and pos[1] > 0 and pos[1] < GAME_HEIGHT:
            pos[0] = pos[0] + dir[0]
            pos[1] = pos[1] + dir[1]
            if not foodSeen and food_pos == pos:
                foodSeen = True
                vision[0] = 1
            if not tailSeen and self.crashIntoSelf(pos[0], pos[1]):
                tailSeen = True
                vision[1] = 1/dist
            dist+=1
        vision[2] = 1/dist
        return vision


    def crossover(self, partner): 
        child = Snake()
        child.brain = self.brain.crossover(partner.brain)
        return child

    
    def mutate(self):
        self.brain.mutate()

    def calcFitness(self):
        #self.fitness = self.score
        #self.fitness = self.lifetime**2 + math.floor(pow(2, self.score))
        self.fitness = self.lifetime*self.lifetime * math.floor(pow(2, self.score+1))
        #if self.score == 0:
          #  self.fitness = self.lifetime*self.lifetime * math.floor(pow(2, self.score))
       # if self.leftToLive == 0: #probably started going in loop
        #    self.fitness -=self.allowedToLive
        #else:
           # self.fitness = self.lifetime*self.lifetime * math.floor(pow(2, self.score+1))
        #self.fitness = self.li


    def clone(self):
        new_snake = Snake()
        new_snake.brain = self.brain
        return new_snake


    def draw(self,win):
        self.food.draw(win)
        pygame.draw.rect(win, BLACK, (self.x, self.y, RECT_DIM, RECT_DIM), 5)
        pygame.draw.rect(win, WHITE, (self.x, self.y, RECT_DIM, RECT_DIM))
        for part in self.tail:
            pygame.draw.rect(win, BLACK, (part[0], part[1], RECT_DIM, RECT_DIM), 5)
            pygame.draw.rect(win, GREEN, (part[0], part[1], RECT_DIM, RECT_DIM))
        
    def set_food(self):
        food = Food()
        while(self.x == food.x and self.y == food.y):
            food = Food()
        return food

class Food:

    def __init__(self):
        random.seed(time.time())
        self.x = random.randint(0, 39)*20
        self.y = random.randint(0, 39)*20
    
    def draw(self,win):
        pygame.draw.rect(win, BLACK, (self.x, self.y, RECT_DIM, RECT_DIM),5)
        pygame.draw.rect(win, RED, (self.x, self.y, RECT_DIM, RECT_DIM))