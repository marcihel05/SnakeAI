import numpy as np
import tenserflow as tf
from tf import keras
from keras import Sequential
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
from snake import Snake


NUM_OF_SNAKES = 1000

class Population:
    def __init__(self):
        self.snakes =[Snake()]*NUM_OF_SNAKES
        self.currentBestSnake = "" #current beast snake
        self.globalBestSnake = "" #index of best snake in this population
        self.globalBestScore = 0

    def findCurrentBestSnake(self):
        max = 0
        maxSnake = self.snakes[0]
        for snake in self.snakes:
            if snake.score > max:
                max = snake.score
                maxSnake = snake
        return maxSnake


    def findGlobalBestSnake(self):

    def genetic_algorithm(self):
        new_population = [Snake()]*NUM_OF_SNAKES
        for i in range(0, len(self.snakes)-1):
            parent1 = self.selectParent()
            parent2 = self.selectParent()
            child_weights = parent1.crossover_and_mutate(parent2)
            new_population[i].brain.set_weights(child_weights)
        return new_population

    def selectParent(self):

    

       
