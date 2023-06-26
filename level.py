import gc
import pygame
from classes import *

def makeHypothRay(drawSur, levelRay):
    origPosX, origPosY = levelRay.posX, levelRay.posY
    origDir = levelRay.direction
    drawSur.fill((0,0,0,0))
    val = 0
    while val not in [-1, 1]:
        val = levelRay.propogate(drawSur)
    if levelRay.direction == origDir:
        print("SAME")
    levelRay.direction = origDir
    levelRay.posX, levelRay.posY = origPosX, origPosY
    print(levelRay.mirrColliding)

def level(levelRay, backSur, drawSur, screen):
    for x in range(levelRay.goalX - levelRay.goalR, levelRay.goalX + levelRay.goalR):
        for y in range(levelRay.goalY - levelRay.goalR, levelRay.goalY + levelRay.goalR):
            backSur.set_at((x, y), (0, 0, 0, 255))
    makerClickerDrag = False
    run = 1
    while run:
        if pygame.mouse.get_pressed()[0]:
            makeHypothRay(drawSur, levelRay)
        gc.collect()
        screen.blit(backSur, (0,0))
        screen.blit(drawSur, (0,0))
        screen.blit(fireButton.image, fireButton.rect)
        for mirrorOb in mirror.mirrorObjects:
            screen.blit(mirrorOb.image, mirrorOb.rect)
            screen.blit(mirrorOb.rotatorImage, mirrorOb.rotatorRect)
        for obstacleOb in obstacle.obstacleObjects:
            screen.blit(obstacleOb.image, obstacleOb.rect)
        screen.blit(mirrorMaker.image, mirrorMaker.rect)
        pygame.display.update()
        if clicker.drag == True:
            clicker.activeObject.update(pygame.mouse.get_pos()[0] - clicker.posX, pygame.mouse.get_pos()[1] - clicker.posY)
            clicker.activeObject.rect = clicker.activeObject.image.get_rect(center = (clicker.activeObject.posX, clicker.activeObject.posY))
        if roundClicker.drag == True:
            roundClicker.activeObject.orient((roundClicker.origOrientation + 180/pi*arctan(pygame.mouse.get_pos()[1]-roundClicker.activeObject.posY, pygame.mouse.get_pos()[0]-roundClicker.activeObject.posX) - roundClicker.startAngle)%360)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mirrorMaker.rect.collidepoint(pygame.mouse.get_pos()):
                    clicker.activeObject = mirror(100, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                    clicker.drag = True
                    clicker.posX, clicker.posY = 0, 0
                for mirrorOb in mirror.mirrorObjects:
                    if mirrorOb.circCollide(pygame.mouse.get_pos()):
                        roundClicker.drag = True
                        roundClicker.startAngle = 180/pi*arctan(pygame.mouse.get_pos()[1]-mirrorOb.posY, pygame.mouse.get_pos()[0]-mirrorOb.posX)
                        roundClicker.activeObject = mirrorOb
                        roundClicker.origOrientation = mirrorOb.orientation
                    elif mirrorOb.collide(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        clicker.drag = True
                        clicker.posX = pygame.mouse.get_pos()[0] - mirrorOb.posX
                        clicker.posY = pygame.mouse.get_pos()[1] - mirrorOb.posY
                        clicker.activeObject = mirrorOb
                        
                if fireButton.rect.collidepoint(pygame.mouse.get_pos()):
                    return 1
            if event.type == pygame.MOUSEBUTTONUP:
                clicker.drag = False
                roundClicker.drag = False
                makerClickerDrag = False
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
                        
        
def fire(levelRay, backSur, drawSur, screen):
    drawSur.fill((0,0,0,0))
    count = 1
    while count:
        screen.blit(backSur, (0,0))
        screen.blit(drawSur, (0,0))
        count += 1
        for mirrorOb in mirror.mirrorObjects:
            screen.blit(mirrorOb.image, mirrorOb.rect)
        for obstacleOb in obstacle.obstacleObjects:
            screen.blit(obstacleOb.image, obstacleOb.rect)
        pygame.display.update()
        propReturn = levelRay.propogate(drawSur)
        if propReturn == 1:
            return 1
        elif propReturn == -1:
            return -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
                count = 0