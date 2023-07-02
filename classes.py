from constants import blockHeight
import pygame
from math import sin, cos
from functions import *
class mirror:
    mirrorObjects = []
    def __init__(self, length, posX, posY):
        self.image = pygame.image.load("mirror.png").convert_alpha()
        self.rotatorImage = pygame.image.load("rotator.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (length, blockHeight) )
        self.posX = posX
        self.posY = posY
        self.rect = self.image.get_rect(center = (posX, posY))
        self.rotatorImage = pygame.transform.scale(self.rotatorImage, (20, 20))
        self.rotatorRect = self.rotatorImage.get_rect(center = (posX, posY))
        self.length = length
        self.orientation = -90
        mirror.mirrorObjects.append(self)
    def update(self, newPosX, newPosY):
        self.posX, self.posY = newPosX, newPosY
        self.rect = self.image.get_rect(center = (newPosX, newPosY))
        self.rotatorRect = self.rotatorImage.get_rect(center = (newPosX, newPosY))
    def circCollide(self, coordinates):
        if (coordinates[0] - self.posX)**2 + (coordinates[1] - self.posY)**2 >= 25 and (coordinates[0] - self.posX)**2 + (coordinates[1] - self.posY)**2 <= 64:
            return 1
    def orient(self, angle):
        self.orient_center(angle)
        self.orientation = angle
    def orient_center(self, angle):
        self.image = pygame.transform.scale(pygame.image.load("mirror.png"), (100, blockHeight))
        self.image = pygame.transform.rotate(self.image, - angle - 90)
        self.rect = self.image.get_rect(center = (self.posX, self.posY))
    def collide(self, pointPosX, pointPosY):
        distance = ((pointPosX - self.posX)**2 + (pointPosY - self.posY)**2)**(0.5)
        if pointPosX != self.posX:
            angle = 180/pi*arctan(pointPosY - self.posY, pointPosX - self.posX)
        else:
            if sin(pi/180*self.orientation) != 0:
                if abs(pointPosY - self.posY) <= blockHeight/2/sin(pi/180*self.orientation):
                    return 1
                else:
                    return 0
            else:
                if abs(pointPosY - self.posY) <= self.length/2:
                    return 1
                else:
                    return 0
        perpendicularComp = distance*cos(pi/180*(angle - self.orientation))
        parallelComp = distance*sin(pi/180*(angle - self.orientation))
        if abs(perpendicularComp) <= blockHeight/2 and abs(parallelComp) <= self.length/2:
            return 1

class obstacle(mirror):
    obstacleObjects = []
    def __init__(self, length, posX, posY):
        super().__init__(length, posX, posY)
        mirror.mirrorObjects.remove(self) # Could replace with pop to optimise.
        self.image = pygame.image.load("obstacle.png")
        self.image = pygame.transform.scale(self.image, (length, blockHeight) )
        obstacle.obstacleObjects.append(self)
    def __del__(self):
        obstacle.obstacleObjects.remove(self)

class ray:
    def __init__(self, goalX, goalY, goalR, posX, posY, direction, color):
        self.goalX = goalX
        self.goalY = goalY
        self.goalR = goalR
        self.direction = direction
        self.posX = posX
        self.posY = posY
        self.color = color
        self.mirrColliding = 0
    def reached(self):
        if ((self.posX - self.goalX)**2 + (self.posY - self.goalY)**2)**(0.5) <= self.goalR:
            return 1
    def propogate(self, drawSur):
        self.posX += int(5*cos(pi/180*self.direction))
        self.posY += int(5*sin(pi/180*self.direction))
        if self.posX > 1500 or self.posY > 800 or self.posX < 0 or self.posY < 0:
            self.mirrColliding = 0
            return -1
        for obstacleOb in obstacle.obstacleObjects:
            if obstacleOb.collide(self.posX, self.posY):
                self.mirrColliding = 0
                return -1
                # self.__del__() can't delete after returning
        for mirrorOb in mirror.mirrorObjects:
            if mirrorOb.collide(self.posX, self.posY) and self.mirrColliding != mirrorOb:
                self.mirrColliding = mirrorOb
                incidentAngle = (mirrorOb.orientation - self.direction)%360
                print(incidentAngle)
                if incidentAngle > 180:
                    incidentAngle -= 360
                if incidentAngle >= - 90 and incidentAngle <= 90:
                    self.direction = (self.direction + 2*incidentAngle+180)%360
                else:
                    print("Ray being deleted")
                    self.mirrColliding = 0
                    return -1
                break
        for x in range(self.posX-5, self.posX+5):
            for y in range(int(self.posY - (25 - (x-self.posX)**2)**(0.5)), int(self.posY + (25 - (x-self.posX)**2)**(0.5)) ):
                if (x - self.posX)**2 + (y - self.posY)**2 <=25:
                    drawSur.set_at((x, y), (self.color[0], self.color[1], self.color[2], 255 - int(((x-self.posX)**2 + (y-self.posY)**2)/25*255)) )
        if self.reached():
            self.mirrColliding = 0
            return 1
        
class fireButtonCl:
    def __init__(self):
        self.image = pygame.image.load("fireButton.png").convert_alpha()
        self.rect = self.image.get_rect(center = (750, 750))

fireButton = fireButtonCl()
        
class clicker:
    drag = False
    posX = 0
    posY = 0
    activeObject = None
    @classmethod
    def reset(cls):
        drag = False
        posX = 0
        posY = 0
        activeObject = None
        
class roundClicker:
    drag = False
    activeObject = None
    origOrientation = None
    @classmethod
    def reset(cls):
        drag = False
        activeObject = None
        origOrientation = None

class mirrorMakerCl:
    def __init__(self):
        self.image = pygame.image.load("mirror.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, blockHeight))
        self.rect = self.image.get_rect(center = (400, 20))

mirrorMaker = mirrorMakerCl() 