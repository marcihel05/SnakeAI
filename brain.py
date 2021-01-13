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
        self.wih = Matrix(HIDDEN, INPUT) #weights beetwen input and hidden
        self.woh = Matrix(OUTPUT, HIDDEN) #weights beetwen hidden and input
        self.x = 650 # coord for drawing
        self.y = 100
    

    def mutate(self): #change some chromosomes
        self.wih.mutate()
        self.woh.mutate()
        


    def crossover(self, partner): #find weights for child
        child_wih = self.wih.crossover(partner.wih)
        child_woh = self.woh.crossover(partner.woh)
        return [child_wih, child_woh]

    def procces(self, vision): #decide direction of movement
        
        middle = self.wih.multiplyWithVector(vision)
        middle.addBias()
        middle.relu()

        decision = self.woh.multiplyWithVector(middle.matrix)
        decision.addBias()
        decision.sigmoid()

        return  decision


    
    #def draw(self,win):