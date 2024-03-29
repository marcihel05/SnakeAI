import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random
from matrix import Matrix
from settings import *


class Brain():
    def __init__(self, rand = True):
        self.wih = Matrix(HIDDEN1, INPUT+1, rand) #weights beetwen input and hidden, bias included
        self.whh = Matrix(HIDDEN2, HIDDEN1 +1, rand) 
        self.who = Matrix(OUTPUT, HIDDEN2+1,rand) #weights beetwen hidden and output, bias included
        


    def crossover(self, partner): #find weights for child #!!!modify so it returns brain!!!
        child_brain = Brain(rand = False)
        child_brain.wih = self.wih.crossover(partner.wih)
        child_brain.whh = self.whh.crossover(partner.whh)
        child_brain.who = self.who.crossover(partner.who)
        return child_brain


    def mutate(self): #change some chromosomes
        self.wih.mutate()
        self.whh.mutate()
        self.who.mutate()

    def decide(self, vision): #decide direction of movement

        input_vision = Matrix(INPUT, 1, False);
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


    
    def draw(self,win, vision, index):
        #c = 19
        r = 13#radius
        c = r + (WIN_HEIGHT/INPUT-2*r)/2
        for i in range(0, INPUT):
            d = WIN_HEIGHT/2 - HIDDEN1/2*WIN_HEIGHT/INPUT
            #d = 187
            for j in range(0, HIDDEN1):
                if self.wih.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (900, c),(1133, d) ) #weights between input and first hidden layer
                else:
                    pygame.draw.line(win, ORANGE, (900, c),(1133, d) )
                d+=WIN_HEIGHT/INPUT
            if vision[i] > 0:
                pygame.draw.circle(win, YELLOW, (900, c), r) #input nodes
            else:
                pygame.draw.circle(win, WHITE, (900, c), r)
            c+=WIN_HEIGHT/INPUT
        
        c = WIN_HEIGHT/2 - HIDDEN1/2*WIN_HEIGHT/INPUT
        #c = 187
        for i in range(0, HIDDEN1):
            d = WIN_HEIGHT/2 - HIDDEN2/2*WIN_HEIGHT/INPUT
            #d = 187
            for j in range(0,HIDDEN2):
                if self.whh.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (1133, c), (1366, d)) #weights between first and second hidden layer
                else:
                    pygame.draw.line(win, ORANGE, (1133, c), (1366, d))
                d+=WIN_HEIGHT/INPUT
            pygame.draw.circle(win, WHITE, (1133, c), r) #first hidden layer nodes
            c+=WIN_HEIGHT/INPUT
        
        c = WIN_HEIGHT/2 - HIDDEN2/2*WIN_HEIGHT/INPUT
        #c = 187
        for i in range(0,HIDDEN2):
            d = WIN_HEIGHT/2 -2*WIN_HEIGHT/INPUT
            #d = 415
            for j in range(0, OUTPUT):
                if self.who.matrix[j][i] < 0:
                    pygame.draw.line(win, BLUE, (1366, c), (1599, d)) #weights between second hidden layer and output
                else:
                    pygame.draw.line(win, ORANGE, (1366, c), (1599, d))
                d+=WIN_HEIGHT/INPUT
            pygame.draw.circle(win, WHITE, (1366, c), r) #second hidden layer nodes
            c+=WIN_HEIGHT/INPUT

        c = WIN_HEIGHT/2 -OUTPUT/2*WIN_HEIGHT/INPUT
        #c = 415
        for i in range(0, OUTPUT):
            if i == index:
                pygame.draw.circle(win, YELLOW, (1599, c), r) #output nodes
            else:
                pygame.draw.circle(win, WHITE, (1599, c), 13)
            c+=WIN_HEIGHT/INPUT

