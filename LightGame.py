from math import pi, atan, cos, sin
from copy import deepcopy
# import constants
import pygame
import gc

pygame.init()

blockHeight = 20

screen = pygame.display.set_mode((1500, 800))
backSur = pygame.Surface((1500, 800)).convert_alpha()
backSur.fill((220,220,220,255))
drawSur = pygame.Surface((1500, 800)).convert_alpha()
drawSur.fill((220,220,220,0))

def dist(x, y, a, b):
    return ((x - a)**2 + (y - b)**2)**(0.5)

def arctan(a, b):
    if b == 0:
        if a > 0:
            return pi/2
        elif a < 0:
            return -pi/2
        else:
            return -pi/2
    elif b > 0:
        return atan(a/b)
    elif b < 0:
        return pi + atan(a/b)
    else:
        if b > 0:
            return pi
        else:
            return -pi

class mirror:
    mirrorObjects = []
    def __init__(self, length, posX, posY):
        self.image = pygame.image.load("E:/NitAgartala/mirror.png").convert_alpha()
        self.rotatorImage = pygame.image.load("E:/NitAgartala/rotator.png").convert_alpha()
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
    # def __del__(self):
    #     mirror.mirrorObjects.remove(self)
    # def rotateAct(self, coordX, coordY):
    #     mouseX = pygame.pygame.mouse.get_pos()[0]
    #     mouseY = pygame.pygame.mouse.get_pos()[1]
    #     if mouseX < 0:
    #         angleNew = 180 + 180/pi*math.atan(mouseY/mouseX)
    #     elif mouseX > 0:
    #         angleNew = 180/pi*math.atan(mouseY/mouseX)
    #     else:
    #         if mouseY > 0:
    #             angleNew = 90
    #         elif mouseY < 0:
    #             angleNew = -90
    #         else:
    #             return
    #     if coordX < 0
    #         angleOld = 180 + 180/pi*math.atan(coordY/coordX)
    #     elif coordX > 0:
    #         angleOld = 180/pi*math.atan(coordY/coordX)
    #     else:
    #         if coordY > 0:
    #             angleOld = 90
    #         elif coordY < 0:
    #             angleOld = -90
    #         else:
    #             return
    #     angleDiff = angleNew - angleOld
    #     self.rotate(angleDiff)
    def orient(self, angle):
        self.orient_center(angle)
        self.orientation = angle
    def orient_center(self, angle):
        self.image = pygame.transform.scale(pygame.image.load("E:/NitAgartala/mirror.png"), (100, blockHeight))
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
        # for x in range(pointPosX - self.length//2, pointPosX + self.length//2):
        #     for y in range(pointPosX - self.length//2, pointPosX + self.length//2):
        #         if distance*cos(pi/180*(arctan( - self.orientation))
        if abs(perpendicularComp) <= blockHeight/2 and abs(parallelComp) <= self.length/2:
            return 1

class obstacle(mirror):
    obstacleObjects = []
    def __init__(self, length, posX, posY):
        super().__init__(length, posX, posY)
        mirror.mirrorObjects.remove(self) # Could replace with pop to optimise.
        self.image = pygame.image.load("E:/NitAgartala/obstacle.png")
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
        screen.set_at((self.posX, self.posY), color)
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
                    # print(incidentAngle)
                    print("Ray being deleted")
                    self.mirrColliding = 0
                    return -1
                    # self.__del__()=
                break
        # drawSur.set_at((self.posX, self.posY), self.color) #Need to reduce opacity of surrounding pixels to make it less pixely
        # print(drawSur.get_at((self.posX, self.posY)))
        for x in range(self.posX-5, self.posX+5):
            for y in range(int(self.posY - (25 - (x-self.posX)**2)**(0.5)), int(self.posY + (25 - (x-self.posX)**2)**(0.5)) ):
                # print(255 - int(((x-self.posX)**2 + (y-self.posY)**2)/25*255))
                # drawSur.set_at((x,y), (self.color[0], self.color[1], self.color[2], 255))
                if (x - self.posX)**2 + (y - self.posY)**2 <=25:
                    drawSur.set_at((x, y), (self.color[0], self.color[1], self.color[2], 255 - int(((x-self.posX)**2 + (y-self.posY)**2)/25*255)) )
                    # drawSur.set_at((x, y), (self.color[0], self.color[1], self.color[2], 255 - int(dist(x, y, self.posX, self.posY)/5*255)) )
                # print(drawSur.get_at((x, y) ))
        if self.reached():
            self.mirrColliding = 0
            return 1
        
class fireButtonCl:
    def __init__(self):
        self.image = pygame.image.load("E:/NitAgartala/fireButton.png").convert_alpha()
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
        self.image = pygame.image.load("E:/NitAgartala/mirror.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, blockHeight))
        self.rect = self.image.get_rect(center = (400, 20))

mirrorMaker = mirrorMakerCl() 

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

def level(levelRay):
    for x in range(levelRay.goalX - levelRay.goalR, levelRay.goalX + levelRay.goalR):
        for y in range(levelRay.goalY - levelRay.goalR, levelRay.goalY + levelRay.goalR):
            backSur.set_at((x, y), (0, 0, 0, 255))
    makerClickerDrag = False
    run = 1
    while run:
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
                makeHypothRay(drawSur, levelRay)
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                exit()
                        
        
def fire(levelRay, backSur):
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
        # print(mirror.mirrorObjects)
        # print(levelRay.posX, levelRay.posY)
                
levelRay = ray(1300, 600, 10, 80, 200, -60, (240, 180, 60, 255))

class victory:
    def __init__(self):
        self.image = pygame.image.load("E:/NitAgartala/winScreen.png")
    def youWon(self):
        print('inside')
        run = 1
        while (run):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    run = 0
            screen.blit(self.image, (0,0))
            pygame.display.update()
            
for x in range(200, 1300, 200):
    obstacle(150, x, 500)

if level(levelRay) == 1:
    if fire(levelRay, backSur) == 1:
        x = 0
        for i in range(1000000):
            x += 1
        victOb = victory()
        victOb.youWon()
        # print(levelRay.posX, levelRay.posY, levelRay.goalX, levelRay.goalY)
        # run = 1
        # while(run):
        #     for event in pygame.event.get():
        #         if event.type == pygame.QUIT:
        #             pygame.display.quit()
        #             pygame.quit()
        #             exit()
        #             run = 0

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