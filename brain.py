import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
from matrix import Matrix

INPUT = 24
HIDDEN = 16
OUTPUT = 4


MUTATION_RATE = 0.05

class Brain():
    def __init__(self):
        self.wih = Matrix(HIDDEN, INPUT+1) #weights beetwen input and hidden, bias included
        self.whh = Matrix(HIDDEN, HIDDEN +1)
        self.who = Matrix(OUTPUT, HIDDEN+1) #weights beetwen hidden and input, bias included
        self.x = 650 # coord for drawing
        self.y = 100
    

    def mutate(self): #change some chromosomes
        self.wih.mutate()
        self.whh.mutate()
        self.who.mutate()
        


    def crossover(self, partner): #find weights for child #!!!modify so it returns brain!!!
        child_brain = Brain()
        child_brain.wih = self.wih.crossover(partner.wih)
        child_brain.whh = self.whh.crossover(partner.whh)
        child_brain.who = self.who.crossover(partner.who)
        return child_brain

    def procces(self, vision): #decide direction of movement

        input_vision = Matrix(24, 1);
        input_vision.matrix = vision
       # print("vision")
        #print(input_vision.matrix)
        inputBias = input_vision.addBias()
        #print("with bias")
        #print(inputBias.matrix)
        #print("weights")
        #print(self.wih.matrix)
        middle = self.wih.multiplyWithVector(inputBias.matrix) #vector
        #print("middle_first")
        #print(middle.matrix)
        middle.relu()
        #print("middle_first_relu")
        #print(middle.matrix)


        middleBias = middle.addBias()
        middle_second = self.whh.multiplyWithVector(middleBias.matrix)
        middle_second.relu()

        middle_second_Bias = middle_second.addBias()
        decision = self.who.multiplyWithVector(middle_second_Bias.matrix)
        decision.sigmoid()

        return decision.matrix


    
    #def draw(self,win):