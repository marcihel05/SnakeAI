import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
from snake import Snake


NUM_OF_SNAKES = 2000
MUTATION_RATE = 0.05

class Population:
    def __init__(self, num = NUM_OF_SNAKES):
        self.num_of_snakes = num
        self.snakes = []
        self.currentBestSnake = "" #index of current beast snake (highest score)
        self.globalBestSnake = "" #index of best snake in this generation (fitness score)
        self.globalBestScore = 0 #best score of this generation
        self.globalFitness = 0 #fitness score of current generation
        self.bestGlobalFitness = 0 #fitness of best snake
        self.genBestScore = 0

        for i in range(0, self.num_of_snakes):
            self.snakes.append(Snake())
        
        self.currentBestSnake = 0
        self.globalBestSnake = 0

    def findCurrentBestSnake(self):
        if not self.snakes[self.currentBestSnake].dead:
            maxScore = self.snakes[self.currentBestSnake].score
            maxSnake = self.currentBestSnake
        else:
            maxScore = 0
            maxSnake = 0
        i = 0 #index of snake in self.snakes
        for snake in self.snakes:
            if snake.score > maxScore and not snake.dead:
                maxScore = snake.score
                maxSnake = i
            i+=1
        self.currentBestSnake = maxSnake
        if maxScore > self.globalBestScore:
            self.globalBestScore = maxScore
        if maxScore > self.genBestScore:
            self.genBestScore = maxScore
    
    
    def findCurrentFiveBestSnakes(self):
        fiveBestSnakes = [self.snakes[0], self.snakes[1], self.snakes[2], self.snakes[3], self.snakes[4]]
        maxIndex = [0,1,2,3,4]

        for i in range(5, len(self.snakes)):
            for j in range(0,5):
                if self.snakes[i].score > fiveBestSnakes[j].score:
                    fiveBestSnakes[j] = self.snakes[i]
                    break
        
        return fiveBestSnakes


    def findGlobalBestSnake(self): #fitness
        maxFitness = 0
        maxIndex = 0
        i = 0
        for snake in self.snakes:
            if snake.fitness > maxFitness:
                maxFitness = snake.fitness
                maxIndex = i
            i+=1
        if maxFitness > self.bestGlobalFitness:
            self.bestGlobalFitness = maxFitness
            self.globalBestSnake = maxIndex


    def calcFitness(self):
        for snake in self.snakes:
            snake.calcFitness()


    def genetic_algorithm(self): ##modify this
        self.calcFitness() #calculate fitness of each snake
        self.findGlobalBestSnake() #find best snake of this generation
        self.calcGlobalFitness() #calc sum of fitness scores of all snakes in this generation
        new_snakes = [self.snakes[self.globalBestSnake].clone()]
        for i in range(1, len(self.snakes)): #find new snakes
            parent1 = self.selectParent() #find parents
            parent2 = self.selectParent()
            child = parent1.crossover(parent2) #make new child
            child.mutate() #mutate child
            new_snakes.append(child)
        self.snakes = new_snakes
        self.currentBestSnake = 0
        self.globalBestSnake = 0
        self.genBestScore = 0
    
    def calcGlobalFitness(self):
        fitness = 0
        for snake in self.snakes:
            fitness+=snake.fitness
        self.globalFitness = fitness


    def selectParent(self):
        #random.seed(time.time())
        rand = random.randrange(0, self.globalFitness)
        sum = 0
        for snake in self.snakes:
            sum+=snake.fitness
            if sum > rand:
                return snake
        return self.snakes[0]



    def update(self):
        for snake in self.snakes:
            if not snake.dead:
                snake.look()
                snake.think()
                snake.move()
        self.findCurrentBestSnake()
        
        

    def allDead(self):
        for snake in self.snakes:
            if not snake.dead:
                return False
        return True
    
    def draw(self, win, toShow):
        if toShow[0] == 1:
            self.findCurrentBestSnake()
            self.snakes[self.currentBestSnake].draw(win)
        if toShow[0] == 5:
            bestSnakes = self.findCurrentFiveBestSnakes()
            for snake in bestSnakes:
                snake.draw(win)
        if toShow[0] == 0:
            for snake in self.snakes:
                if not snake.dead:
                    snake.draw(win)
        if toShow[1] == 1:
            index = np.argmax(self.snakes[self.currentBestSnake].decision)
            self.snakes[self.currentBestSnake].brain.draw(win,index)

        

    

       
