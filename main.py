
# import constants
import pygame

pygame.init()


screen = pygame.display.set_mode((1500, 800))
backSur = pygame.Surface((1500, 800)).convert_alpha()
backSur.fill((220,220,220,255))
drawSur = pygame.Surface((1500, 800)).convert_alpha()
drawSur.fill((220,220,220,0))

from functions import *

from classes import *
from level import *



                
levelRay = ray(1300, 600, 10, 80, 200, -60, (240, 180, 60, 255))

import victory
            
for x in range(200, 1300, 200):
    obstacle(150, x, 500)

if level(levelRay, backSur, drawSur, screen) == 1:
    if fire(levelRay, backSur, drawSur, screen) == 1:
        x = 0
        for i in range(1000000):
            x += 1
        victory.youWon(screen)

    else:
        print(0)
        run = 1
        # gameOver()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    exit()
                    run = 0