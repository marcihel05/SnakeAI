import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
from population import Population
from snake import Snake
from brain import Brain
from settings import *

pygame.font.init()
SCORE_FONT = pygame.font.SysFont("monospace", 25)
GAME_OVER_FONT = pygame.font.SysFont("monospace", 50)
OVERTEXT = GAME_OVER_FONT.render("Game Over", 1, WHITE)
CONTINUETEXT1 = GAME_OVER_FONT.render("Press Enter", 1, WHITE)
CONTINUETEXT2 = GAME_OVER_FONT.render("to start again", 1, WHITE)


def draw_window(win, snake, toShow, global_best_score):
    win.fill(BLACK)
    snake.draw(win, toShow)
    currscoretext = SCORE_FONT.render("Current best score: "+str(snake.score), 1, WHITE)
    globalscoretext = SCORE_FONT.render("All time best score: "+str(global_best_score), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 3)
    win.blit(currscoretext, (1133,5))
    win.blit(globalscoretext, (1133,35))
    pygame.display.update()


def game_over(win, snake):
	while 1:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					return True
		win.fill(BLACK)
		scoretext = GAME_OVER_FONT.render("Score = "+str(snake.score), 1, WHITE)
		win.blit(scoretext, (WIN_WIDTH/2-WIN_WIDTH/4,WIN_HEIGHT/3))
		win.blit(OVERTEXT, (WIN_WIDTH/2-WIN_WIDTH/4,WIN_HEIGHT/6))
		win.blit(CONTINUETEXT1, (WIN_WIDTH/2-WIN_WIDTH/4,WIN_HEIGHT/2))
		win.blit(CONTINUETEXT2, (WIN_WIDTH/2-WIN_WIDTH/4-50,WIN_HEIGHT/2+75))
		pygame.display.update()



def main():
 	snake = Snake(rand = False, load = True)
 	global_best_score = 0
 	toShow = True
 	pygame.init()
 	win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
 	pygame.display.set_caption('AI learned to play Snake')
 	clock = pygame.time.Clock()
 	FPS = 10 #frames per second
 	run = True
 	while run:
 		play = True
 		while play:
 			draw_window(win, snake, toShow, global_best_score)
 			clock.tick(FPS)
 			for event in pygame.event.get():
 				if event.type == pygame.QUIT:
 					play = False
 					run = False
 					break
 				if event.type == pygame.KEYDOWN:
 					if event.key == pygame.K_UP: #speed up the game
 						FPS+=5
 					if event.key == pygame.K_DOWN and FPS>=10: #slow down the game
 						FPS-=5
 					if event.key == pygame.K_SPACE: #show/hide brain
 						toShow = not toShow
 			snake.look()
 			snake.think()
 			snake.move()
 			if snake.dead:
 				cont = game_over(win, snake)
 				if cont:
 					snake = snake.clone()
 				else:
 					play = False
 					run = False
 		if not run:
 			break
 		if run == True:
 			play = True
 	pygame.quit()
 	quit()


if __name__ == '__main__':
    main()