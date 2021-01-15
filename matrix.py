import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
import math

MUTATION_RATE = 0.05

def sigmoid_function(x):
    return 1/(1+math.exp(-x))

class Matrix():
    def __init__(self, r = 0, c = 0, rand = True):
        self.row = r
        self.col = c
        random.seed(time.time())
        self.matrix = np.zeros((self.row, self.col))
        if rand == True: #set weights
            for i in range(0, self.row):
                for j in range(0, self.col):
                    random.seed(time.time())
                    self.matrix[i][j] = random.uniform(-1, 1)
    
    def crossover(self, partner):
        child = Matrix(self.row, self.col, False)
        random.seed(time.time())
        randR = random.randint(0, self.row-1)
        randC = random.randint(0, self.col-1)

        for i in range(0, self.row):
            for j in range(0, self.col):
                if (i < randR) or (i== randR and j <= randC):
                    child.matrix[i][j] = self.matrix[i][j]
                else:
                    child.matrix[i][j] = partner.matrix[i][j]
        return child

    
    
    def mutate(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                random.seed(time.time())
                rand = random.uniform(0,1)
                if rand < MUTATION_RATE:
                    r = random.gauss(0,1)/5
                    self.matrix[i][j] +=r
                if self.matrix[i][j] > 1:
                    self.matrix[i][j] = 1
                if self.matrix[i][j] < -1:
                    self.matrix[i][j] = -1


    
    def addBias(self): #add bias to nx1 vector
        new = Matrix(self.row +1, 1, False)
        for i in range(0, self.row):
            new.matrix[i][0] = self.matrix[i][0]
        new.matrix[self.row][0] = 1
        return new



    #def multiply(self, other): #return Matrix
     #   res = Matrix(self.row, other.col, False)
      #  res.matrix = self.matrix.dot(other)
       # return res
    
    def  multiply(self, other):
        res = Matrix(self.row, other.col, False)
        for i in range(0, self.row):
            for j in range(0, other.col):
                sum_ = 0
                for k in range(0, self.col):
                    sum_+= self.matrix[i][k]*other.matrix[k][j]
                res.matrix[i][j] = sum_
        return res
        
    
    def multiplyWithVector(self, other):
        res = Matrix(self.row, 1, False)
        res.matrix = self.matrix.dot(other)
        return res
    
    def relu(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                if self.matrix[i][j] < 0:
                    self.matrix[i][j] = 0

                
    def sigmoid(self):
        for i in range(0, self.row):
            for j in range(0, self.col):
                self.matrix[i][j] = sigmoid_function(self.matrix[i][j])

    






