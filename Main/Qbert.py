import pygame
import sys
import time
import random
pygame.init()

# Screen setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Qbrt")

# Load sprites safely
try:
    sprite = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Base Block.png")
    sprite1 = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/BaseBlock1.png")
    unsized = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/pstandingr.png")
except pygame.error as e:
    print(f"Error loading image: {e}")
    pygame.quit()
    sys.exit()

sprite.set_colorkey((255, 255, 255))
sprite1.set_colorkey((255, 255, 255))

# Resize player sprite
PstandingR = pygame.transform.scale(unsized, (48, 48))

# Block positions
block_positions = [
    (330, 40), (330, 199), (235, 200), (428, 200), (284, 120), (380, 120),
    (186, 281), (280, 279), (378, 279), (475, 279), (136, 360), (232, 358),
    (328, 358), (423, 358), (520, 358), (87, 439)   
]

# Player spawn position
player_spawn = (360, 30)  # Only one position, so no need for a list

run = True
while run:
    screen.fill((0, 0, 0))  # Clear screen each frame

    # Draw blocks
    for pos in block_positions:
        screen.blit(sprite1, pos)

    # Draw player sprite
    screen.blit(PstandingR, player_spawn)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

    pygame.display.flip()  # Update display

pygame.quit()
