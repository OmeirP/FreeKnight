from distutils.spawn import spawn
from re import X
from turtle import right
import pygame
import sys
import os


########## all variables will go here



#display_width = 1600
#display_height = 900


red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)

alpha = ()


fps = 60

runFrames = 10
playerIdleFrames = 10

boarRunFrames = 6


gaming = True





############ objects

class playerClass(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.xMove = 0
        self.yMove = 0
        self.frame = 0
        self.health = 20
        
        self.imgsList = []
        for i in range(1, 11):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/run", "run" + str(i) + ".png")).convert()
            self.image = pygame.transform.scale(self.image, (18*playerXScale, 27*playerYScale)).convert()  #18 and 27 because original canvas size is 80x120, 18 and 27 scales to screen size and keeps ratio
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect = self.firstImg.get_rect()
    
    def move(self, x, y):
        
        self.xMove += x
        self.yMove += y
        
    def update(self):
        
        self.rect.x += self.xMove
        self.rect.y += self.yMove
        
        
        if self.xMove > 0:  #more than 0 because future x pos will increase if moving right
            self.frame += 1
            if self.frame > 9*runFrames:  # 9 because thats how many other frames there are
                self.frame = 0
            self.image = self.imgsList[self.frame//runFrames]


        if self.xMove < 0:  #moving left
            self.frame += 1
            if self.frame > 9*runFrames:
                self.frame = 0
            self.image = pygame.transform.flip((self.imgsList[self.frame//runFrames]), True, False)  #flipping the item in the list that is going to be updated to
            
        dmgList = pygame.sprite.spritecollide(self, enemyList, False)  # False is for dokill, go on pygame doc for an explanation
        
        for enemy in dmgList:
            self.health -= 1
            print("self.health", self.health)
            
        
            
            

class boarClass(pygame.sprite.Sprite):
    
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
    
        self.frame = 0
        self.xMove = 2
        self.yMove = 0
        self.wait = 5000
        self.direction = "right"
        
        
        self.imgsList = []
        for i in range(1, 7):
            
            self.image = pygame.image.load(os.path.join("Legacy-Fantasy-VL.1 - High Forest - Update 1.5/Mob/Boar/Run/SeparatePngs/boarRun", "boarRun" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (3*boarXScale, 2*boarYScale)).convert_alpha()
            self.imgsList.append(self. image)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect = self.firstImg.get_rect()
            
        self.rect.x = x
        self.rect.y = y
        
        self.stepCount = 0
    
    
    def move(self):

        
        distance = 240
        #speed = 2
        

        if self.stepCount >= 0 and self.stepCount <= distance:
            self.direction = "right"
            self.rect.x += self.xMove
        elif self.stepCount >= distance and self.stepCount <= distance*2:
            self.direction = "left"
            self.rect.x -= self.xMove
        else:
            self.stepCount = 0
        
        self.stepCount += 1
        
        
    def update(self):
        
        #self.rect.x += self.xMove
        #self.rect.y += self.yMove
        
        
        if self.direction == "right":  # standing still
            self.frame += 1
            if self.frame > 5*boarRunFrames: 
                self.frame = 0
            self.image = pygame.transform.flip((self.imgsList[self.frame//boarRunFrames]), True, False)
        
        if self.direction == "left":  # standing still
            self.frame += 1
            if self.frame > 5*boarRunFrames: 
                self.frame = 0
            self.image = self.imgsList[self.frame//boarRunFrames]




class level:
    def mobSpawn(lvl, spawnPos):
        if lvl == 1:
            boar = boarClass(spawnPos[0], spawnPos[1])
            enemyList = pygame.sprite.Group()
            enemyList.add(boar)
        
        return enemyList
            
        





##############  setup things


clock=pygame.time.Clock()

pygame.init()

infoObject = pygame.display.Info()

gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#gameDisplay=pygame.display.set_mode((256, 144))

background = pygame.image.load(os.path.join("Legacy-Fantasy-VL.1 - High Forest - Update 1.5/background","background.png")).convert()

background = pygame.transform.scale(background, (infoObject.current_w, infoObject.current_h))

playerXScale = infoObject.current_w//80
playerYScale = infoObject.current_h//120

boarXScale = infoObject.current_w//48
boarYScale = infoObject.current_h//32

gameDisplayRect=gameDisplay.get_rect()


player = playerClass()

#player.rect.x = 200
#player.rect.y = 1000

player.rect.x = infoObject.current_w*0.08
player.rect.y = infoObject.current_h*0.6


playerList = pygame.sprite.Group()
playerList.add(player)

runXChange = 5


spawnPos = [1200, 1100]

enemyList = level.mobSpawn(1, spawnPos)




###########game loop

while gaming:
    
    
    
    
    for event in pygame.event.get():
    
    
    # exit code
    
        if event.type == pygame.QUIT:
            pygame.quit()
            try:
                sys.exit()
            finally:
                gaming=False
                
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                try:
                    sys.exit()
                finally:
                    gaming=False
    
    
    # movement code
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move(runXChange, 0)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move(-runXChange, 0)
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                print("jump key down")
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move(-runXChange, 0)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move(runXChange, 0)
                

    
    
    
    gameDisplay.blit(background, gameDisplayRect)
    
    player.update()
    playerList.draw(gameDisplay)
    
    #boar.update()
    
    
    for i in enemyList:

        i.move()
        i.update()    
        
        
    enemyList.draw(gameDisplay)
    
    
    pygame.display.update()
    clock.tick(fps)
                



