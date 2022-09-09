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


gaming=True





############ objects

class playerClass:
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.imgsList = []
        for i in range(1,11):
            
            img = pygame.image.load(os.path.join("FreeKnight_v1/Colour1/NoOutline/SeparatePngs/run", "run" + str(i) + ".png")).convert()            
            self.imgsList.append(img)
            
            self.firstImg = self.imgsList[0]  # just to get a picture from the cycle with the same dimensions as the rest to use to get rect
            
            self.rect = self.firstImg.get_rect()





############## pygame setup things


clock=pygame.time.Clock()

pygame.init()

infoObject = pygame.display.Info()

gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

background = pygame.image.load(os.path.join("Legacy-Fantasy-VL.1 - High Forest - Update 1.5/background","background.png")).convert()

background = pygame.transform.scale(background, (infoObject.current_w, infoObject.current_h))

gameDisplayRect=gameDisplay.get_rect()


player = playerClass()
player.rect.x = 0
player.rect.y = 0

playerList = pygame.sprite.Group()
playerList.add(player)






############ first run things here






###########game loop

while gaming:
    
    
    for event in pygame.event.get():
        
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
    
    
    
    gameDisplay.blit(background, gameDisplayRect)
    
    pygame.display.update()
    clock.tick(fps)
                



