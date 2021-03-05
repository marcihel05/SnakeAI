NUMBER_OF_SNAKES = 2000 #number of snakes in population

MUTATION_RATE = 0.1

SAVE_GEN1 = 150
SAVE_GEN2 = 250
SAVE_GEN3 = 500
SAVE_GEN4 = 650 #save brain of best snake after SAVE_GEN generations

INPUT = 25
HIDDEN1 = 16
HIDDEN2 = 16
OUTPUT = 4

#dimensions of screen and game
WIN_HEIGHT = 950
WIN_WIDTH = 1700
GAME_WIDTH = 800
GAME_HEIGHT = 800


RECT_DIM = 20 #dimension of snake's part and food
VELOCITY = 20 #velocity of snake
LEFT_TO_LIVE = 200

LEFT = [-VELOCITY, 0]
UP = [0, -VELOCITY]
RIGHT = [VELOCITY, 0]
DOWN = [0, VELOCITY]

#used colors
BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0,0,255)
ORANGE = (255,128,0)

BRAIN_FILE = 'brain_z10_650'