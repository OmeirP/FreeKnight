import pygame
import sys
import os


########## all variables will go here



#display_width = 1600
#display_height = 900


red = (255, 0, 0)
blue = (0, 255, 0)
green = (0, 0, 255)


fps=60

runFrames=10


gaming=True





############ objects

class playerClass(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.xMove = 0
        self.yMove = 0
        self.frame = 0
        
        self.imgsList = []
        for i in range(1, 11):
            
            self.image = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/run", "run" + str(i) + ".png")).convert()
            self.image = pygame.transform.scale(self.image, (18*playerXScale, 27*playerYScale)).convert()  #18 and 27 because original canvas size is 80x120, 18 and 27 scales to screen size and keeps ratio
            self.imgsList.append(self. image)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect = self.firstImg.get_rect()
    
    def move(self, x, y):
        
        self.xMove += x
        self.yMove += y
        
    def posUpdate(self):
        
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
            self.image = pygame.transform.flip((self.imgsList[self.frame//runFrames]), True, False)
            
        





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

gameDisplayRect=gameDisplay.get_rect()


player = playerClass()
player.rect.x = 0
player.rect.y = 0

playerList = pygame.sprite.Group()
playerList.add(player)

runXChange=5





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
    
    player.posUpdate()
    playerList.draw(gameDisplay)
    
    
    pygame.display.update()
    clock.tick(fps)
                



