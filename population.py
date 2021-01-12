import numpy as np
import tenserflow as tf
from tf import keras
from keras import Sequential
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time


NUM_OF_SNAKES = 1000

class Population:
   def __init__(self):
       self.snakes =[Snake()]*NUM_OF_SNAKES
       self.currentBest = 0
       self.globalBest = 0
       
