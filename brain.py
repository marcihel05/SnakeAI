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

WIN_HEIGHT = 1000
WIN_WIDTH = 1700
GAME_WIDTH = 800
GAME_HEIGHT = 800

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
ORANGE = (255,128,0)

MUTATION_RATE = 0.05

class Brain():
    def __init__(self):
        self.wih = Matrix(HIDDEN, INPUT+1) #weights beetwen input and hidden, bias included
        self.whh = Matrix(HIDDEN, HIDDEN +1) 
        self.who = Matrix(OUTPUT, HIDDEN+1) #weights beetwen hidden and output, bias included
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
        input_vision.matrix = vision #input
        inputBias = input_vision.addBias() #add bias to input vector
        middle = self.wih.multiplyWithVector(inputBias.matrix) #multiply weights and input
        middle.relu() #activation function

        middleBias = middle.addBias()
        middle_second = self.whh.multiplyWithVector(middleBias.matrix) #multiply weights and first hidden neurons
        middle_second.relu() #activation function

        middle_second_Bias = middle_second.addBias()
        decision = self.who.multiplyWithVector(middle_second_Bias.matrix) #multiply weights and second hidden neurons
        decision.sigmoid() #activation function

        return decision.matrix #output


    
    def draw(self,win, index):
        c = 35
        for i in range(0, INPUT):
            d = 187
            for j in range(0, HIDDEN):
                if self.wih.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (900, c),(1133, d) ) #weights between input and first hidden layer
                else:
                    pygame.draw.line(win, ORANGE, (900, c),(1133, d) )
                d+=38
            pygame.draw.circle(win, WHITE, (900, c), 13) #input nodes
            c+=38
        
        c = 187
        for i in range(0, HIDDEN):
            d = 187
            for j in range(0,HIDDEN):
                if self.whh.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (1133, c), (1366, d)) #weights between first and second hidden layer
                else:
                    pygame.draw.line(win, ORANGE, (1133, c), (1366, d))
                d+=38
            pygame.draw.circle(win, WHITE, (1133, c), 13) #first hidden layer nodes
            c+=38
        
        c = 187
        for i in range(0,HIDDEN):
            d = 415
            for j in range(0, OUTPUT):
                if self.who.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (1366, c), (1599, d)) #weights between second hidden layer and output
                else:
                    pygame.draw.line(win, ORANGE, (1366, c), (1599, d))
                d+=38
            pygame.draw.circle(win, WHITE, (1366, c), 13) #second hidden layer nodes
            c+=38

        c = 415
        for i in range(0, OUTPUT):
            if i == index:
                pygame.draw.circle(win, YELLOW, (1599, c), 13) #output nodes
            else:
                pygame.draw.circle(win, WHITE, (1599, c), 13)
            c+=38

