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
healthRed = (255, 59, 59)
borderCol = (61, 39, 0)
blackish = (58, 64, 66)
#whitish = (245, 245, 245)
redishWhitish = (252, 199, 199)
#darkerWhitish = (191, 191, 191)
darkerRedishWhitish = (198, 145, 145)
green = (0, 255, 0)
blue = (0, 0, 255)

#alpha = ()


fps = 60

runFrames = 10
playerIdleFrames = 10
playerJumpFrames = 3
playerFallFrames = 3

boarRunFrames = 6




gaming = True
pause = False
totPlayTime = 0





############ objects

class playerClass(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.xMove = 0
        self.yMove = 0
        self.frame = 0
        self.health = 20
        self.lostLife = 0
        self.hitTick = 0
        self.direction = "right"
        self.jumpState = False
        self.fallState = True
        
        self.playerXScale = infoObject.current_w//37
        self.playerYScale = infoObject.current_h//19
        
        self.imgsList = []
        for i in range(1, 11):
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/idle", "idle" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1.357142857*self.playerXScale, 2.035714286*self.playerYScale)).convert_alpha() 
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect = self.firstImg.get_rect()
    
    
    
    def gravity(self):
        self.yMove += 0.00041667*infoObject.current_h   # Player fall speed. Always be falling because gravity always active.
        

                
    
    def move(self, x, y, device):
        
        if device == "KEYBOARD":
            self.xMove += x
        elif device == "CONTROLLER":
            self.xMove = x
        
        self.yMove += y
        
        if self.xMove < 0:
            self.direction = "left"
        elif self.xMove > 0:
            self.direction = "right"
        

    def jump(self):
        if self.jumpState == False: # if not already jumping
            self.fallState = False
            self.jumpState = True
        #else:
        #    print("fail")

    
    def runAnimSwitch(self):
        
        self.playerXScale = infoObject.current_w//42
        self.playerYScale = infoObject.current_h//28
        
        self.imgsList = []
        for i in range(1, 11):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/run", "run" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (2*self.playerXScale, 3*self.playerYScale)).convert_alpha()  #2 and 3 because original canvas size is 120x80, 2 and 3 scales to screen size and keeps ratio
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect.width = self.firstImg.get_width()
            self.rect.height = self.firstImg.get_height()
    
    
    
    def idleAnimSwitch(self):
        
        self.playerXScale = infoObject.current_w//37
        self.playerYScale = infoObject.current_h//19
        
        self.imgsList = []
        for i in range(1, 11):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/idle", "idle" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1.357142857*self.playerXScale, 2.035714286*self.playerYScale)).convert_alpha() # These decimal values are specific because the images have different pixel sizes to the run images and the size of the sprites must be equal. See scaleCalculations.txt for how to work out.
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]
            
            self.rect.width = self.firstImg.get_width()
            self.rect.height = self.firstImg.get_height()
                
    
    
    def jumpAnimSwitch(self):
        
        self.playerXScale = infoObject.current_w//37
        self.playerYScale = infoObject.current_h//23
        self.imgsList = []
        for i in range(1, 4):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/jump", "jump" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1.64285714291*self.playerXScale, 2.46428571436*self.playerYScale)).convert_alpha()
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]
            
            self.rect.width = self.firstImg.get_width()
            self.rect.height = self.firstImg.get_height()
    
    


    def fallAnimSwitch(self):
        
        self.playerXScale = infoObject.current_w//37
        self.playerYScale = infoObject.current_h//27
        self.imgsList = []
        for i in range(1, 4):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/fall", "fall" + str(i) + ".png")).convert_alpha()
            self.image = pygame.transform.scale(self.image, (1.92857142862*self.playerXScale, 2.89285714293*self.playerYScale)).convert_alpha() 
            self.imgsList.append(self.image)
            
            self.firstImg = self.imgsList[0]
            
            self.rect.width = self.firstImg.get_width()
            self.rect.height = self.firstImg.get_height()





    def update(self):
        

        
        if self.xMove > 0 and self.fallState != True:  #more than 0 because future x pos will increase if moving right
            self.runAnimSwitch()
            self.frame += 1
            if self.frame > 8*runFrames:  # 9 because thats how many other frames there are
                self.frame = 0  ## reset animation
            self.image = self.imgsList[self.frame//runFrames]

    
        if self.xMove < 0 and self.fallState != True:  #moving left
            self.runAnimSwitch()
            self.frame += 1
            if self.frame > 8*runFrames:
                self.frame = 0
            self.image = pygame.transform.flip((self.imgsList[self.frame//runFrames]), True, False)  #flipping the item in the list that is going to be updated to
                     
        
        if self.xMove == 0 and self.fallState != True:
            self.idleAnimSwitch()
            self.frame += 1
            if self.frame > 8*playerIdleFrames:
                self.frame = 0
            if self.direction == "right":
                self.image = self.imgsList[self.frame//playerIdleFrames]
            elif self.direction == "left":
                self.image = pygame.transform.flip((self.imgsList[self.frame//playerIdleFrames]), True, False)
        
        
        self.rect.x += self.xMove
        self.rect.y += self.yMove
            
        
            
        dmgList = pygame.sprite.spritecollide(self, enemyList, False, pygame.sprite.collide_rect)  # False is for dokill, go on pygame doc for an explanation
        
        for enemy in dmgList:
            if self.hitTick == 0 and self.health > 0:
                self.health -= 4
                self.hitTick = fps
                #pygame.mixer.Sound.play(hurtSnd)
                hurtSnd.play()
                print("self.health", self.health)
        if self.hitTick > 0:
            self.hitTick -= 1

        self.lostLife = 20 - self.health
        

        
        grndHitList = pygame.sprite.spritecollide(self, grndList, False)    # spritecollide returns a list of sprites in the group that intersect with the player.
        
        for grnd in grndHitList:
            self.yMove = 0
            self.rect.bottom = grnd.rect.top
            self.jumpState = False  # Finish jumping
            self.fallState = False
        
        
        pltHitList = pygame.sprite.spritecollide(self, pltList, False)  # Consider adding mask_collide. Better collision with side but correction uses rect not mask so doesn't look as clean.
        
        
    
        platsNum = len(pltList.sprites())
        
        
        
        
        for plat in pltHitList:

            # This part same as before for ground.
            self.yMove = 0
            #self.jumpState = False
            platformRight = (startPos + tileWidth * platsNum)
            # If player is under platform when colliding.
            if self.rect.bottom <= plat.rect.bottom:    # If the player is higher than the platform when colliding. Make player sprite sit on top of platform sprite.
                self.rect.bottom = plat.rect.top
                self.jumpState = False
                self.fallState = False

            
            elif self.rect.bottom > plat.rect.bottom and (self.rect.left > startPos and self.rect.right < platformRight):     # If player is below platform (when jumping) and not outside of it.
                self.yMove += 0.00041667*infoObject.current_h   # Else normal fall.
        
                
                
            
            else:
                if (self.rect.left < platformRight and abs(platformRight-self.rect.left) < abs(startPos-self.rect.right)) and self.rect.bottom > plat.rect.bottom:  # If player intersects with right side of platform, keep on right side of platform.
                    self.rect.left = platformRight
                    self.yMove += 0.00055556*infoObject.current_h
                    

                elif (self.rect.left < platformRight and abs(platformRight-self.rect.left) > abs(startPos-self.rect.right)) and self.rect.bottom > plat.rect.bottom: # If player intersects with left side of platform, keep on left side of platform.
                    self.rect.right = startPos
                    self.yMove += 0.00055556*infoObject.current_h
                    #print(self.rect.left, plat.rect.right)
                
        
    

        
            
        #   Check if player fell out of bounds
        if self.rect.y > levelHeight and self.yMove > 0:
            self.health -= 5
            self.rect.x = infoObject.current_w*0.38
            self.rect.y = infoObject.current_h-tileWidth*6  # Instead, die and go to place on screen
        
            
        # The jump part, switches to falling at the end.
        if self.jumpState == True and self.fallState == False:
            self.yMove -= 0.0138888888888889*infoObject.current_h    # Change this to be proportional to screen size.
            #play sound here
            #pygame.mixer.Sound.play(jumpSnd)
            jumpSnd.play()
            self.fallState = True
            
            
            
        #print(self.fallState, self.jumpState)
        
        if self.yMove < 0:
            self.jumpAnimSwitch()
            self.frame += 1
            if self.frame > 2*playerJumpFrames:
                self.frame = 0
            if self.direction == "right":
                self.image = self.imgsList[self.frame//playerJumpFrames]
            elif self.direction == "left":
                self.image = pygame.transform.flip((self.imgsList[self.frame//playerJumpFrames]), True, False)
                
        if self.yMove > 1:
            self.fallAnimSwitch()
            self.frame += 1
            if self.frame > 2*playerFallFrames:
                self.frame = 0
            if self.direction == "right":
                self.image = self.imgsList[self.frame//playerFallFrames]
            elif self.direction == "left":
                self.image = pygame.transform.flip((self.imgsList[self.frame//playerFallFrames]), True, False)
    
        
            

        
        
            
            

class EnemyClass(pygame.sprite.Sprite):
    
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
    
        self.frame = 0
        self.xMove = 0.0015625*infoObject.current_w
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
    
    
    
    
    def gravity(self):
        self.yMove += 0.0013888888888889*infoObject.current_h
        
        #   Check if player fell out of bounds
        if self.rect.y > levelHeight and self.yMove > 0:
            self.yMove = 0
            self.rect.y = infoObject.current_h-tileWidth*6  # should reach floor before this. Do something else.
        
        
        
        
    
    def move(self):

        
        distance = 240
        #speed = 2
        

        if self.stepCount >= 0 and self.stepCount <= distance:     #stepCount is basically distance travelled, no direction. half steps taken one way. other half taken other way. step count resets to represent being at starting point. Infinite if-else loop
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
        self.rect.y += self.yMove
        
        
        if self.direction == "right":
            self.frame += 1
            if self.frame > 5*boarRunFrames: 
                self.frame = 0
            self.image = pygame.transform.flip((self.imgsList[self.frame//boarRunFrames]), True, False)
        if self.direction == "left":
            self.frame += 1
            if self.frame > 5*boarRunFrames: 
                self.frame = 0
            self.image = self.imgsList[self.frame//boarRunFrames]


        grndHitList = pygame.sprite.spritecollide(self, grndList, False)    # spritecollide returns a list of sprites in the group that intersect with the player.
        
        for grnd in grndHitList:
            self.yMove = 0
            self.rect.bottom = grnd.rect.top
            #self.jumpState = False  # Finish jumping.





class Platform(pygame.sprite.Sprite):
    def __init__(self, xpos, ypos, imgWidth, imgHeight, imgFile):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('groundpngs', imgFile)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (tileWidth, tileHeight))
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos




        

class Level: 
    def mobSpawn(lvl, spawnPos):
        if lvl == 1:
            boar = EnemyClass(spawnPos[0], spawnPos[1])
            enemyList = pygame.sprite.Group()
            enemyList.add(boar)
        
        return enemyList
    
    
    

    def ground(lvl, gPos, tileWidth, tileHeight): # Attributes of where to put ground.
        grndList = pygame.sprite.Group()
        placed = 0
        if lvl == 1:
            leftGrnd = Platform(tileWidth + gPos[placed], infoObject.current_h-tileHeight*3, tileWidth, tileHeight, "ground000.png")
            leftSub1Grnd = Platform(tileWidth + gPos[placed], infoObject.current_h-tileHeight*2, tileWidth, tileHeight, "ground008.png")
            leftSub2Grnd = Platform(tileWidth + gPos[placed], infoObject.current_h-tileHeight, tileWidth, tileHeight, "ground008.png")
            platsToAdd = [leftGrnd, leftSub1Grnd, leftSub2Grnd]
            
            for plat in platsToAdd:
                grndList.add(plat)
                
            while placed < len(gPos):    # Checks against how many ground tiles will be.
                topGrnd = Platform(tileWidth*2 + gPos[placed], infoObject.current_h-tileHeight*3, tileWidth, tileHeight, "ground001.png")
                sub1Grnd = Platform(tileWidth*2 + gPos[placed], infoObject.current_h-tileHeight*2, tileWidth, tileHeight, "ground009.png")
                sub2Grnd = Platform(tileWidth*2 + gPos[placed], infoObject.current_h-tileHeight, tileWidth, tileHeight, "ground009.png")
                platsToAdd = [topGrnd, sub1Grnd, sub2Grnd]
                for plat in platsToAdd:
                    grndList.add(plat)
    
                placed+=1            
        return grndList
    
    
    
    
    def platform(lvl, tileWidth, tileHeight):
        pltList = pygame.sprite.Group()
        screenHeight = infoObject.current_h
        pPos = []
        platsPlaced = 0
        if lvl == 1:
            allStartPos = [levelWidth*0.05] # This list should contain start positions for all platforms. (May need to use enumerate for multiple platforms.)
            
            for startPos in allStartPos:
                pPos.append((startPos, screenHeight - (tileWidth*7.5), 8))  # tuple for individual positions.  Format: (x, y, length). Length is number of tiles for platform to consist of.   Have multiple of these lines for how many platforms wanted.
            while platsPlaced < len(pPos):    # number of elements in pPos means that platforms in level
                tilesPlaced = 0
                while tilesPlaced <= pPos[platsPlaced][2]:
                    plat = Platform((pPos[platsPlaced][0] + (tilesPlaced*tileWidth)), pPos[platsPlaced][1], tileWidth, tileHeight, "ground001.png")
                    pltList.add(plat)
                    tilesPlaced += 1
                platsPlaced += 1
                
            platsNum = len(pltList.sprites())
            platformRight = (startPos + tileWidth * platsNum)
                
        return pltList, startPos, platformRight
        

class Healthbar():
    
    def __init__(self):
        self.backRect = pygame.Rect((100, 100), (400, 50))
        self.redRect = pygame.Rect((100, 100), (400, 50))
        self.borderRect = pygame.Rect((97, 97), (404, 55))
        self.noHealth = False
        
    def drawBar(self):
        pygame.draw.rect(gameDisplay, blackish, self.backRect)
        pygame.draw.rect(gameDisplay, healthRed, self.redRect)
        if not self.noHealth:
            pygame.draw.polygon(gameDisplay, redishWhitish, [(100, 100), (499 - (player.lostLife*20), 100), (499 - (player.lostLife*20), 104), (103, 103)])
            pygame.draw.polygon(gameDisplay, darkerRedishWhitish, [(100, 100), (100, 150), (103, 150), (103, 103)])
        pygame.draw.rect(gameDisplay, borderCol, self.borderRect, 3)

    def update(self):
        if player.health <= 0:
            self.noHealth = True
            
        self.redRect = pygame.Rect((100, 100), (400 - (player.lostLife*20), 50))
        
        
        
        
class PauseMenu(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("pauseAssets", "pauseScreen1.png")).convert()
        self.image = pygame.transform.scale(self.image, (infoObject.current_w, infoObject.current_h))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = infoObject.current_h  # Do everything relative screen as pause screen is relative to screen.
        
        
    def ascend(self):
        
        while self.rect.y > 0:
            self.rect.y -= 120
            drawAll()
        else:
            self.rect.y = 0
            drawAll()
    
    
    def descend(self):
        
        while self.rect.y < infoObject.current_h:
            self.rect.y += 120
            drawAll()
        else:
            self.rect.y = infoObject.current_h
            drawAll()
    

class SettingsMenu(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("settingsAssets", "settingsScreen.png")).convert()
        self.image = pygame.transform.scale(self.image, (infoObject.current_w, infoObject.current_h))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = infoObject.current_h  # Do everything relative screen as pause screen is relative to screen.
    
    
    def ascend(self):
            
        while self.rect.y > 0:
            self.rect.y -= 120
            drawAll()
        else:
            self.rect.y = 0
            drawAll()
    
    
    def descend(self):
        
        while self.rect.y < infoObject.current_h:
            self.rect.y += 120
            drawAll()
        else:
            self.rect.y = infoObject.current_h
            drawAll()


def alphaBlit(gameDisplay, image, position, opacity):
        x = position[0]
        y = position[1]
        temp = pygame.Surface((image.get_width(), image.get_height())).convert()
        temp.blit(gameDisplay, (-x, -y))
        temp.blit(image, (0, 0))
        temp.set_alpha(opacity)        
        gameDisplay.blit(temp, position)
        

def death():
    
    deathSnd.play()
    
    opacity = 0
    opacityChng = 4
    alphaImage = deathScrn.copy()
    #alphaImage.set_alpha(alpha)
    #alphaImage.set_colorkey((255,0,255)) 
    startPlay = False
    bin = True
    while bin:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if pygame.K_j:
                    pygame.quit()
                    sys.exit()
                    
                
        alphaBlit(gameDisplay, alphaImage, (0,0), opacity)
        opacity += opacityChng
        pygame.display.update()
        clock.tick(fps)
        if not startPlay:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join("sounds/themes", "dead.wav"))
            pygame.mixer.music.play(-1)
            startPlay = True
        



def menu():
    pass




def button(actvImg, inactvImg, xPos, yPos, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    imgRect = actvImg.get_rect()
    width = imgRect.width
    height = infoObject.current_h*0.1
    height = imgRect.height
    
    
    # scale image to screen size. 
    
    if xPos + width > mouse[0] > xPos and yPos + height > mouse[1] > yPos:
        image = actvImg
        if click[0] == 1 and action != None:
            pygame.mixer.Sound.play(slctSnd)
            
            match action:
                case "exit":
                    pygame.quit()
                    sys.exit()
                case "settings":
                    settingsScreen.ascend()
                    while True:
                        pygame.display.update()
                        button(quitBtnRoll, quitBtnNorm, infoObject.current_w*0.6, infoObject.current_h*0.4, "settingsByeBye")
                case "settingsByeBye":
                    pass
                    settingsScreen.descend()
                        
                        
                    
    else:
        image = inactvImg
        #image = pygame.transform.scale(image, (width, height)).convert_alpha()
        

    gameDisplay.blit(image, [xPos, yPos])



def drawAll():
    for i in background:
        gameDisplay.blits([(i, (decorFocusPoint*0.1, 0)), (i, (decorFocusPoint*0.1+infoObject.current_w, 0)), (i, (decorFocusPoint*0.1-infoObject.current_w, 0))])
    gameDisplay.blit(redTree, [decorFocusPoint + (500)/(2560/infoObject.current_w)*1.5, (infoObject.current_h-tileHeight*3)-(360)/(1440/infoObject.current_h)*1.5])
    enemyList.draw(gameDisplay)
    grndList.draw(gameDisplay)
    pltList.draw(gameDisplay)
    playerList.draw(gameDisplay)
    for i in ui:
        i.drawBar()
    screens.draw(gameDisplay)
    pygame.display.update()



##############  setup things


clock=pygame.time.Clock()



pygame.init()   # Also calls pygame.joystick.init()



# Joystick code.

print("Joystick module initialised?", pygame.joystick.get_init())


if not (pygame.joystick.get_count() >= 1):
    print("No controller connected.")
else:
    print("Controller found.")
    xController = pygame.joystick.Joystick(0)
    xController.init()



infoObject = pygame.display.Info()

gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
#gameDisplay=pygame.display.set_mode((256, 144))


jumpSnd = pygame.mixer.Sound(os.path.join("sounds\sfx","jump1.wav"))
jumpSnd.set_volume(0.5)

hurtSnd = pygame.mixer.Sound(os.path.join("sounds\sfx", "hurt1.wav"))

slctSnd = pygame.mixer.Sound(os.path.join("sounds\sfx", "select1.wav"))

deathSnd = pygame.mixer.Sound(os.path.join("sounds\sfx", "isThisDeath1.wav"))

deathScrn = pygame.image.load(os.path.join("deathscreen", "youdied.png")).convert_alpha()
deathScrn = pygame.transform.scale(deathScrn, (infoObject.current_w, infoObject.current_h))



#background = pygame.image.load(os.path.join("Legacy-Fantasy-VL.1 - High Forest - Update 1.5/background","background.png")).convert()
bgl1 = pygame.image.load(os.path.join("skybgs\Clouds\Clouds 1","1.png")).convert_alpha()
bgl1 = pygame.transform.scale(bgl1, (infoObject.current_w, infoObject.current_h))
bgl2 = pygame.image.load(os.path.join("skybgs\Clouds\Clouds 1","2.png")).convert_alpha()
bgl2 = pygame.transform.scale(bgl2, (infoObject.current_w, infoObject.current_h))
bgl3 = pygame.image.load(os.path.join("skybgs\Clouds\Clouds 1","3.png")).convert_alpha() 
bgl3 = pygame.transform.scale(bgl3, (infoObject.current_w, infoObject.current_h))
bgl4 = pygame.image.load(os.path.join("skybgs\Clouds\Clouds 1","4.png")).convert_alpha()
bgl4 = pygame.transform.scale(bgl4, (infoObject.current_w, infoObject.current_h))

background = [bgl1, bgl2, bgl3, bgl4]



decorFocusPoint = 0

redTree = pygame.image.load(os.path.join("Legacy-Fantasy - High Forest 2.3\Trees\RedTreeLarge","redTree1.png")).convert_alpha()
treeRect = redTree.get_rect()
redTree = pygame.transform.scale(redTree, ((treeRect.width/(2560/infoObject.current_w))*1.5, (treeRect.height/(1440/infoObject.current_h))*1.5))



quitBtnNorm = pygame.image.load(os.path.join("pauseAssets", "buttonRev4_normal.png")).convert_alpha()
quitBtnRoll = pygame.image.load(os.path.join("pauseAssets", "buttonRev5_rollover.png")).convert_alpha()


#playerXScale = infoObject.current_w//42
#playerYScale = infoObject.current_h//28

#playerXScale = infoObject.current_w//80
#playerYScale = infoObject.current_h//120


boarXScale = infoObject.current_w//48
boarYScale = infoObject.current_h//32

gameDisplayRect=gameDisplay.get_rect()


fwdCamDed = infoObject.current_w * 0.6      # Forward camera deadzone
bkwdCamDed = infoObject.current_w * 0.1




player = playerClass()



player.rect.x = infoObject.current_w*0.2
player.rect.y = infoObject.current_h*0.7

playerList = pygame.sprite.Group()
playerList.add(player)

#runXChange = 10
runXChange = infoObject.current_w*0.00390625


spawnPos = [1200, 1100]

#spawnPos = [infoObject.current_w*0.08, infoObject.current_h*0.6]

enemyList = Level.mobSpawn(1, spawnPos)


grndTilPos = []


tileWidth = 0.025*infoObject.current_w
tileHeight = 0.025*infoObject.current_w
#tileWidth = 64
#tileHeight = 64


levelWidth = infoObject.current_w*10   #   Change this depending on level.
levelHeight = infoObject.current_h+infoObject.current_h*0.1     # Screen Height + 10% of screen height so can fall a bit out and not die.


i = 0
while i < ((levelWidth/tileWidth) + tileWidth):   # Adds how many ground tiles to do for ground based on level width.
    grndTilPos.append(tileWidth*i)
    i+=1

grndList = Level.ground(1, grndTilPos, tileWidth, tileHeight)

pltList, startPos, platformRight = Level.platform(1, tileWidth, tileHeight)


hlthbar = Healthbar()
ui = [hlthbar]


pauseScreen = PauseMenu()
settingsScreen = SettingsMenu()

screens = pygame.sprite.Group()
screens.add(pauseScreen)
screens.add(settingsScreen)

theme1 = pygame.mixer.music.load(os.path.join("sounds/themes", "level1.ogg"))

pygame.mixer.music.play(-1)


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
            if event.key == pygame.K_p:
                totPlayTime += pygame.mixer.music.get_pos()
                pygame.mixer.music.stop()
                pause = True
            #if event.key == pygame.K_j:
            #    death()
    
    
    # movement code
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move(runXChange, 0, "KEYBOARD")
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move(-runXChange, 0, "KEYBOARD")
            if event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jump()
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.move(-runXChange, 0, "KEYBOARD")
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.move(runXChange, 0, "KEYBOARD")
                


        
        if event.type == pygame.JOYBUTTONDOWN:
            if event.button == 0:
                player.jump()
        
        
        if event.type == pygame.JOYAXISMOTION:
            xAxisPos = xController.get_axis(0)
            if xAxisPos < -0.3:
                player.move(-runXChange, 0, "CONTROLLER")
            elif xAxisPos > 0.3:
                player.move(runXChange, 0, "CONTROLLER")
            else:
                player.move(0, 0, "CONTROLLER")
    
    
            
    if pause:
        pygame.mixer.music.load(os.path.join("sounds/themes", "level1Pause.ogg"))
        pygame.mixer.music.play(-1, (totPlayTime/1000)%17.5)  # Divide by 1000 as get_pos returns millisecond time. Play takes seconds.
        
        pauseScreen.ascend()

    
                
    while pause:

        #gameDisplay.blit(playBtnNorm, [400, 800])
        button(quitBtnRoll, quitBtnNorm, infoObject.current_w*0.6, infoObject.current_h*0.7, "exit")
        #button(quitBtnRoll, quitBtnNorm, infoObject.current_w*0.4, infoObject.current_h*0.7, "settings")
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()


                if event.key == pygame.K_p:
                    pause = False
                    totPlayTime += pygame.mixer.music.get_pos() # Get_pos doesn't take timestamp of file played, just how long the sound has been playing for. Keeps track of how long all themes have been playing.
                    pauseScreen.descend()
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join("sounds/themes", "level1.ogg"))  
                    pygame.mixer.music.play(-1, (totPlayTime/1000)%17.5)    # Divide by 1000 as get_pos returns millisecond time. Play takes seconds. Remainder for dividing by song length so time isn't invalid after song ends and has to repeat.

        
    
        
    
    
    
    
    
    #   Scroll player and platform tiles when going foward.
    if player.rect.x >= fwdCamDed:
        scrollChange = player.rect.x - fwdCamDed    # Get change to move platforms.
        player.rect.x = fwdCamDed   # Keep player at deadzone spot.
        for plat in pltList:
            plat.rect.x -= scrollChange
        startPos -= scrollChange
        for grnd in grndList:
            grnd.rect.x -= scrollChange
        for enemy in enemyList:
            enemy.rect.x -= scrollChange
        decorFocusPoint -= scrollChange
    
    
    #   Scroll player and platform tiles when going foward.
    if player.rect.x <= bkwdCamDed:
        scrollChange = bkwdCamDed - player.rect.x
        player.rect.x = bkwdCamDed
        for plat in pltList:
            plat.rect.x += scrollChange 
        startPos += scrollChange # Need to do for all startPos in allStartPos?
        for grnd in grndList:
            grnd.rect.x += scrollChange
        for enemy in enemyList:
            enemy.rect.x += scrollChange
        decorFocusPoint += scrollChange
    


    
    for i in background:
        gameDisplay.blits([(i, (decorFocusPoint*0.1, 0)), (i, (decorFocusPoint*0.1+infoObject.current_w, 0)), (i, (decorFocusPoint*0.1+infoObject.current_w*2, 0)), (i, (decorFocusPoint*0.1+infoObject.current_w, 0)), (i, (decorFocusPoint*0.1-infoObject.current_w, 0))])
        """gameDisplay.blit(i, (decorFocusPoint*0.1+infoObject.current_w, 0))
        gameDisplay.blit(i, (decorFocusPoint*0.1-infoObject.current_w, 0))"""
    
    gameDisplay.blit(redTree, [decorFocusPoint + (500)/(2560/infoObject.current_w)*1.5, (infoObject.current_h-tileHeight*3)-(360)/(1440/infoObject.current_h)*1.5])
    
    
    player.gravity()
    
    player.update()
    playerList.draw(gameDisplay)
    
    if player.health <= 0:
        death()
    #boar.update()
    
    
    for i in enemyList:

        i.move()
        i.gravity()
        i.update()
        
        
    enemyList.draw(gameDisplay)
    grndList.draw(gameDisplay)
    pltList.draw(gameDisplay)
    for i in ui:
        i.drawBar()
        i.update()
    
    pygame.display.update()
    clock.tick(fps)
                


