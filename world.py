#if snake goes up, it can't go down and vice versa
#if snake goes right, it can't go left and vice versa

#dodati oči na glavu lol

import numpy as np
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import time
from population import Population
from snake import Snake
from brain import Brain

BLACK = (0,0,0)
RED = (255, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)


pygame.font.init()
SCORE_FONT = pygame.font.SysFont("monospace", 25)
GEN_FONT = SCORE_FONT


WIN_HEIGHT = 1000
WIN_WIDTH = 1700
GAME_WIDTH = 800
GAME_HEIGHT = 800


RECT_DIM = 20



def draw_window(win, population, toShow, num_of_gen, global_best_score):
    win.fill(BLACK)
    population.draw(win, toShow)
    gentext = GEN_FONT.render("Generation: "+str(num_of_gen), 1, WHITE)
    currscoretext = SCORE_FONT.render("Current best score: "+str(population.snakes[population.currentBestSnake].score), 1, WHITE)
    globalscoretext = SCORE_FONT.render("All time best score: "+str(population.globalBestScore), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 3)
    win.blit(gentext, (820,5))
    win.blit(currscoretext, (820,55))
    win.blit(globalscoretext, (820,105))
    pygame.display.update()

def main():
    population = Population()
    num_of_gen = 1
    global_best_score = 0
    run = True
    showOnlyBest = False
    showBestFive = False
    pygame.init()
    toShow = 0
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('AI learns to play Snake')
    clock = pygame.time.Clock()
    FPS = 40
    i = 0
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
                    if event.key == pygame.K_UP:
                        FPS+=5
                    if event.key == pygame.K_DOWN and FPS>=10:
                        FPS-=5
                    if event.key == pygame.K_SPACE:
                        showOnlyBest = True
                        toShow = 1
                    if event.key == pygame.K_a:
                        showOnlyBest = False
                        toShow = 0
                    if event.key == pygame.K_KP5:
                        showBestFive = True
                        toShow = 5
            population.update()
            if population.globalBestScore > global_best_score:
                global_best_score = population.globalBestScore
            #draw_window(win, population, toShow, num_of_gen, global_best_score)
            
            if population.allDead():
                win.fill(BLACK)
                pygame.display.update()
                population.genetic_algorithm()
                num_of_gen+=1
                #play = False
                #break;
            #draw_window(win, population, toShow, num_of_gen, global_best_score)
            else:
                draw_window(win, population, toShow, num_of_gen, global_best_score)

        if not run:
            break
        if run == True:
            play = True
    
    pygame.quit()
    quit()




if __name__ == '__main__':
    main()

