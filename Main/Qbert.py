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
sprite_sheet_image = pygame.image.load(Base Block.png).convert_alpha()

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
