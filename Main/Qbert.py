import pygame
import sys
import random
import time
pygame.init()

# Screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Qbrt")

#spritesheet
sprite1 = pygame.image.load("C:/Users/ABKrep8015/Downloads/qber-multiprocess-main/Main/Art/BaseBlock1.png")
sprite1.set_colorkey((255, 255, 255))

# Define the size and position of a single sprite
sprite_width = 32
sprite_height = 32
sprite_x = 0
sprite_y = 0

screen.blit(sprite1, (330, 40)) #top block
screen.blit(sprite1, (330, 199))
screen.blit(sprite1, (235, 200)) #3rd row left block
screen.blit(sprite1, (428, 200)) #3rd row right block
screen.blit(sprite1, (284, 120)) #2nd section
screen.blit(sprite1, (380, 120)) #2nd section right block
#4th row start
screen.blit(sprite1, (186, 281)) #4th row left block
screen.blit(sprite1, (280, 279)) #4th row 2nd left block
screen.blit(sprite1, (378, 279)) #4th row 2nd right block
screen.blit(sprite1, (475, 279)) #4th row  right block
screen.blit(sprite1, (136, 360)) #5th row left block
screen.blit(sprite1, (232, 358)) #5th row 2nd left block
screen.blit(sprite1, (328, 358)) #5th row middleblock
screen.blit(sprite1, (423, 358)) #5th row 2nd rightblock
screen.blit(sprite1, (520, 358)) #5th row rightblock
screen.blit(sprite1, (87, 439)) #6th row left block
screen.blit(sprite1, (186, 439)) #6th row 2nd left block
screen.blit(sprite1, (280, 439)) #6th row left middle block
screen.blit(sprite1, (375, 439)) #6th row 2nd right middleblock block
screen.blit(sprite1, (470, 439)) #6th row 2nd right block
screen.blit(sprite1, (565, 439)) #6th row right block
pygame.display.flip()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    # Update display lmfao
    pygame.display.flip()

pygame.quit()
sys.exit()
