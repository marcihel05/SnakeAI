import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time

MUTATION_RATE = 0.05

def sigmoid_function(x):
    return 1/(1+exp(-x))

class Matrix():
    def __init__(self, r = 0, c = 0):
        self.row = r
        self.col = c
        self.matrix = np.random.uniform(-1, 1, (self.row, self.col))
    
    def crossover(self, partner):
        child = Matrix(self.row, self.col)
        randR = random.randint(0, self.row-1)
        randC = random.randint(0, self.col-1)

        for i in range(0, self.row-1):
            for j in range(0, self.col-1):
                if i < randR or (i== randR and j < randC):
                    child.matrix[i][j] == self.matrix[i][j]
                else:
                    child.matrix[i][j] == partner.matrix[i][j]
        return child

    
    
    def mutate(self):
        for i in range(0, self.row-1):
            for j in range(0, self.col-1):
                rand = random.uniform(0,1)
                if rand < MUTATION_RATE:
                   self.matrix[i][j] +=random.gauss(0,1)*5


    
    def addBias(self):
        """
        for i in range(0, self.row-1):
            for j in range(0, self.col-1):
                self.matrix[i][j] += random.gauss(0, 1)
        """
        return



    def multiply(self, other): #return Matrix
        res = Matrix(self.row, other.col)
        res.matrix = self.matrix.dot(other)
        return res
    
    def multiplyWithVector(self, other):
        res = Matrix(self.row, 1)
        res.matrix = self.matrix.dot(other)
        return res
    
    def relu(self):
        for i in range(0, self.row-1):
            for j in range(0, self.col-1):
                if self.matrix[i][j] < 0:
                    self.matrix[i][j] = 0

                
    def sigmoid(self):
        for i in range(0, self.row-1):
            for j in range(0, self.col-1):
                self.matrix[i][j] = sigmoid_function(self.matrix[i][j])

    






