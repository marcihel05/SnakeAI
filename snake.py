import numpy as np
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
from brain import Brain
from matrix import Matrix
from settings import *



class Snake():
    def __init__(self, rand = True, load = False):
        self.x = GAME_WIDTH/2
        self.y = GAME_HEIGHT/2
        self.tail = [[self.x, self.y+RECT_DIM], [self.x, self.y+2*RECT_DIM],[self.x, self.y+3*RECT_DIM]]
        self.last_pos = ""
        self.len = 4 #length of snake = 1+ len(self.tail)
        self.vel = [0, 0] #direction of movement
        self.food = self.set_food()
        self.brain = Brain(rand) #neural network
        self.fitness = 0
        self.lifetime = 0 #how many steps it made
        self.leftToLive = LEFT_TO_LIVE #to prevent infinite loops
        self.score = 0
        self.had_eaten = False
        self.dead = False
        self.vision = np.zeros((INPUT,1)) #input of network
        self.decision = np.zeros((OUTPUT,1)) #output of network
        self.load = load
        if self.load: #if testing trained snake
            self.loadBrain()

    
    def think(self):
        self.decision = self.brain.decide(self.vision)
       
    
    def move(self):
        if not self.load:
            self.lifetime+=1
            self.leftToLive-=1
            if self.leftToLive < 0:
                self.dead = True
                return

        direction = np.argmax(self.decision)

        if direction == 0: #left
            if self.vel == UP or self.vel == DOWN:
                self.leftToLive-=1
            if not self.vel == RIGHT:
                self.vel = LEFT
        
        if direction == 1: #up
            if self.vel == RIGHT or self.vel == LEFT:
                self.leftToLive-=1
            if not self.vel == DOWN:
                self.vel = UP
                
        
        if direction == 2: #right
            if self.vel == UP or self.vel == DOWN:
                self.leftToLive-=1
            if not self.vel == LEFT:
                self.vel = RIGHT
                

        if direction == 3: #down
            if self.vel == RIGHT or self.vel == LEFT:
                self.leftToLive-=1
            if not self.vel == UP:
                self.vel = DOWN
  
        self.eat() #check if it found food

        self.moveTail()
        self.x += self.vel[0]
        self.y += self.vel[1]
        


        self.crash() #check if it crashed
            
    def moveTail(self):
        i = self.len -2
        self.last_pos = self.tail[i]
        while i > 0:
            self.tail[i] = self.tail[i-1]
            i-=1
        self.tail[0] = [self.x, self.y]
        if self.had_eaten:
            self.grow();
            self.had_eaten = False


    def grow(self):  #popraviti
        self.tail.append(self.last_pos)
       # last = self.tail[(self.len)-2]
        #if last[0] == self.x:
         #   if last[1] > self.y: #end in below head
          #      pos = (last[0], last[1]+RECT_DIM)
           # else: #end is above head
            #    pos = (last[0], last[1]-RECT_DIM)

        #if last[0] < self.x:
         #   if last[1] == self.y: #moving to right
          #      pos = (last[0]-RECT_DIM, last[1])
           # if last[1] > self.y: #
            #    pos = (last[0]-RECT_DIM, last[1])
            #if last[1] < self.y:
             #   pos = (last[0], last[1]- RECT_DIM)
        
        #if last[0] > self.x:
         #   if last[1] == self.y:# moving to left
          #      pos = (last[0] + RECT_DIM, last[1])
           # if last[1] > self.y:
            #    pos = (last[0] + RECT_DIM, last[1])
            #if last[1] < self.y:
             #   pos = (last[0], last[1] - RECT_DIM)

        #self.tail.append(pos)
        self.len+=1


    def eat(self):
        if self.x+self.vel[0] == self.food.x and self.y + self.vel[1]== self.food.y:
            self.leftToLive = 200
            self.score+=1
            self.food = self.set_food()
            self.had_eaten = True
            self.grow()

    
    def crashIntoSelf(self, x = "", y = ""):
        if not x and not y:
            x = self.x
            y = self.y
        for part in self.tail:
            if x == part[0] and y == part[1]:
                return True
        return False

    
    def crash(self):
        if self.crashIntoSelf():
            self.dead = True
        if self.x > GAME_WIDTH-RECT_DIM or self.x <0 or self.y < 0 or self.y > GAME_HEIGHT-RECT_DIM:
            self.dead = True


    def look(self): #vision of snake (input of neural net)

        new_vision = self.whatISee((VELOCITY, 0)) #right
        self.vision[0] = new_vision[0]
        self.vision[1] = new_vision[1]
        self.vision[2] = new_vision[2]
        
        new_vision = self.whatISee((VELOCITY, VELOCITY)) #right-down
        self.vision[3] = new_vision[0]
        self.vision[4] = new_vision[1]
        self.vision[5] = new_vision[2]
       
        new_vision = self.whatISee((0, VELOCITY)) #down
        self.vision[6] = new_vision[0]
        self.vision[7] = new_vision[1]
        self.vision[8] = new_vision[2]
        
        new_vision = self.whatISee((-VELOCITY, 0)) #left
        self.vision[9] = new_vision[0]
        self.vision[10] = new_vision[1]
        self.vision[11] = new_vision[2]
        
        new_vision = self.whatISee((-VELOCITY, -VELOCITY)) #left-up
        self.vision[12] = new_vision[0]
        self.vision[13] = new_vision[1]
        self.vision[14] = new_vision[2]
       
        new_vision = self.whatISee((0, -VELOCITY)) #up
        self.vision[15] = new_vision[0]
        self.vision[16] = new_vision[1]
        self.vision[17] = new_vision[2]
        
        new_vision = self.whatISee((VELOCITY, -VELOCITY)) #right-up
        self.vision[18] = new_vision[0]
        self.vision[19] = new_vision[1]
        self.vision[20] = new_vision[2]
       
        new_vision = self.whatISee((-VELOCITY, VELOCITY)) #left-down
        self.vision[21] = new_vision[0]
        self.vision[22] = new_vision[1]
        self.vision[23] = new_vision[2]

        num_of_rect = (GAME_HEIGHT*GAME_WIDTH)/(RECT_DIM*RECT_DIM)
        self.vision[24] = self.len/(num_of_rect) 

    def whatISee(self, dir): #search for food, tail, wall in given direction
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
                vision[0] = 1#1/dist #1
            if not tailSeen and self.crashIntoSelf(pos[0], pos[1]):
                tailSeen = True
                vision[1] = 1/dist #1
            dist+=1
        vision[2] = 1/dist
        return vision


    def crossover(self, partner): 
        child = Snake(rand = False)
        child.brain = self.brain.crossover(partner.brain)
        return child

    
    def mutate(self):
        self.brain.mutate()

    def calcFitness(self):
        if self.leftToLive == 0:
            self.lifetime-=50
        if self.score == 0:
            self.fitness = pow(self.lifetime, 1.5)
        if self.score > 0:
            self.fitness = self.lifetime*self.lifetime * math.floor(pow(2, self.score+1))
        if self.fitness < 0:
            self.fitness = 0


    def clone(self):
        new_snake = Snake(rand = False)
        new_snake.brain = self.brain
        return new_snake


    def draw(self,win, toShow = False):
        self.food.draw(win)
        pygame.draw.rect(win, BLACK, (self.x, self.y, RECT_DIM, RECT_DIM), 5)
        pygame.draw.rect(win, GREEN, (self.x, self.y, RECT_DIM, RECT_DIM))
        for part in self.tail:
            pygame.draw.rect(win, BLACK, (part[0], part[1], RECT_DIM, RECT_DIM), 5)
            pygame.draw.rect(win, GREEN, (part[0], part[1], RECT_DIM, RECT_DIM))
        win.fill(BLACK, (self.x+5, self.y+10-1,3,3))
        win.fill(BLACK, (self.x+15-2, self.y+10-1,3, 3))
        if toShow:
            self.brain.draw(win, self.vision, np.argmax(self.decision))

    def set_food(self):
        food = Food()
        while(self.x == food.x and self.y == food.y):
            food = Food()
        return food

    def loadBrain(self):
        f = open(BRAIN_FILE)
        weights_map = map(float, f)
        weights = list(weights_map)
        k = 0
        for i in range(0, HIDDEN1):
            for j in range(0, INPUT+1):
                self.brain.wih.matrix[i][j] = weights[k]
                k+=1

        for i in range(0, HIDDEN2):
            for j in range(0, HIDDEN1+1):
                self.brain.whh.matrix[i][j] = weights[k]
                k+=1

        for i in range(0, OUTPUT):
            for j in range(0, HIDDEN2+1):
                self.brain.who.matrix[i][j] = weights[k]
                k+=1

        f.close()


class Food:

    def __init__(self):
        self.x = random.randrange(1,int(GAME_WIDTH/RECT_DIM)-1)*RECT_DIM
        self.y = random.randrange(1,int(GAME_HEIGHT/RECT_DIM)-1)*RECT_DIM
    
    def draw(self,win):
        pygame.draw.rect(win, BLACK, (self.x, self.y, RECT_DIM, RECT_DIM),5)
        pygame.draw.rect(win, RED, (self.x, self.y, RECT_DIM, RECT_DIM))