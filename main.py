import pygame
import sys
import os


########## all variables will go here



#display_width = 1600
#display_height = 900


red = (255,0,0)
blue = (0,255,0)
green = (0,0,255)


fps=60


gaming=True


############## pygame setup things


clock=pygame.time.Clock()

pygame.init()


gameDisplay=pygame.display.set_mode((0,0),pygame.FULLSCREEN)

background = pygame.image.load(os.path.join("Legacy-Fantasy-VL.1 - High Forest - Update 1.5","background.png"))

gameDisplayRect=gameDisplay.get_rect()

print(gameDisplayRect)



############ classes, funcs



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
                



