
#dodati oci na glavu lol

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
GEN_FONT = SCORE_FONT




def draw_window(win, population, toShow, num_of_gen, global_best_score):
    win.fill(BLACK)
    population.draw(win, toShow)
    gentext = GEN_FONT.render("Generation: "+str(num_of_gen), 1, WHITE)
    currscoretext = SCORE_FONT.render("Current best score: "+str(population.snakes[population.currentBestSnake].score), 1, WHITE)
    genbestscore = GEN_FONT.render("Best score of this generation: "+str(population.genBestScore), 1, WHITE)
    globalscoretext = SCORE_FONT.render("All time best score: "+str(population.globalBestScore), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 3)
    win.blit(gentext, (1133,5))
    win.blit(currscoretext, (5,820))
    win.blit(globalscoretext, (1133,35))
    win.blit(genbestscore, (5, 850))
    pygame.display.update()

def main():
    population = Population()
    num_of_gen = 1
    global_best_score = 0
    toShow =  [0,1] #show[0] == 0 -> show all snakes, show[0] == 1 ->show only the best snake, show[1] == 0 -> hide brain, show[1] == 1 -> show brain
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('AI learns to play Snake')
    clock = pygame.time.Clock()
    FPS = 40 #frames per second
    run = True
    while run:
        play = True
        #win.fill(BLACK)
        while play:
            draw_window(win, population, toShow, num_of_gen, global_best_score)
            clock.tick(FPS)
            #win.fill(BLACK)
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
                    if event.key == pygame.K_SPACE: #show all snakes/only the best snake
                        toShow[0] = not toShow[0]
                    #if event.key == pygame.K_a:
                     #   toShow[0] = 0
                    #if event.key == pygame.K_KP5:
                     #   toShow[0] = 5
                    if event.key == pygame.K_h: #show/hide brain of the best snake
                        toShow[1] = not toShow[1]

            population.update()
            if population.globalBestScore > global_best_score:
                global_best_score = population.globalBestScore
            #draw_window(win, population, toShow, num_of_gen, global_best_score)
            
            if population.allDead():
                win.fill(BLACK)
                pygame.display.update()
                population.genetic_algorithm()
                if num_of_gen == SAVE:
                    population.saveBestSnake()
                num_of_gen+=1
                #play = False
                #break;
            #draw_window(win, population, toShow, num_of_gen, global_best_score)
            #else:
              #  draw_window(win, population, toShow, num_of_gen, global_best_score)

        if not run:
            break
        if run == True:
            play = True
    
    pygame.quit()
    quit()




if __name__ == '__main__':
    main()

