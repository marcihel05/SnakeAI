
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
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
    globalscoretext = SCORE_FONT.render("All time best score: "+str(global_best_score), 1, WHITE)
    pygame.draw.rect(win, WHITE, (0,0, GAME_WIDTH, GAME_HEIGHT), 2)
    win.blit(gentext, (1133,5))
    win.blit(currscoretext, (5,GAME_WIDTH+20))
    win.blit(globalscoretext, (1133,35))
    win.blit(genbestscore, (5, GAME_WIDTH+50))
    pygame.display.update()

def main():
    population = Population()
    num_of_gen = 1
    global_best_score = 0 #all time best score
    toShow =  0 #show == 0 -> show all snakes, show == 1 ->show only the best snake
    pygame.init()
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption('AI learns to play Snake')
    clock = pygame.time.Clock()
    FPS = 40 #frames per second
    run = True
    while run:
        draw_window(win, population, toShow, num_of_gen, global_best_score)
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: #speed up the game
                    FPS+=5
                if event.key == pygame.K_DOWN and FPS>=10: #slow down the game
                    FPS-=5
                if event.key == pygame.K_SPACE: #show all snakes/only the best snake
                    toShow = not toShow

        population.update()
        if population.genBestScore > global_best_score:
            global_best_score = population.genBestScore
            
        if population.allDead():
            win.fill(BLACK)
            pygame.display.update()
            population.genetic_algorithm()
            if num_of_gen == SAVE_GEN:
                population.saveBestSnake()
            num_of_gen+=1

        if not run:
            break
    
    pygame.quit()
    quit()




if __name__ == '__main__':
    main()

