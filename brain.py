import numpy as np
import tenserflow as tf
from tf import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random

WIN_WIDTH = 600
WIN_HEIGHT = 600

RECT_DIM = 20

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

INPUT = 24
HIDDEN = 18
OUTPUT = 4

LEFT = 'l'
RIGHT = 'r'
UP = 'u'
DOWN = 'd'

class Brain():
    def __init__(self, weights=''):
        self.brain = Sequential()
        self.brain.add(Dense(INPUT, input_dim = INPUT))
        self.brain.add(Activation('relu'))
        self.brain.add(Dense(HIDDEN, input_dim = INPUT))
        self.brain.add(Activation('relu'))
        self.brain.add(Dense(OUTPUT))
        self.brain.add(Activation('sigmoid'))

        if weights:
            self.brain.load_wights(weights)
        self.brain.compile(loss='mse', optimizer='adam')

    def mutate(self, weigths):


    def crossoverInputToHidden(self, partner):
        my_weights = self.brain.get_weights()[1]
        partner_weights = partner.brain.get_weights()[1]
        randC = random.randint(0, INPUT)
        randR = random.randint(0, HIDDEN)
        child_weights = [][]
        for i in range(0, HIDDEN-1):
            for j in range(0, INPUT-1):
                if i < randR or (i == randR and j<randC):
                    child_weights[i][j] = my_weights[i][j]
                else:
                    child_weights[i][j] = partner_weights[i][j]
        return child_weights

      
    
    def crossoverHiddenToInput(self, partner):
        my_weights = self.brain.get_weights()[2]
        partner_weights = partner.brain.get_weights()[2]
        randC = random.randint(0, OUTPUT)
        randR = random.randint(0, HIDDEN)
        child_weights = [][]
        for i in range(0, OUTPUT-1):
            for j in range(0, HIDDEN-1):
                if i < randR or (i == randR and j<randC):
                    child_weights[i][j] = my_weights[i][j]
                else:
                    child_weights[i][j] = partner_weights[i][j]
        return child_weights
                
    