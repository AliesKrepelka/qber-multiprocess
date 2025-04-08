import pygame
import sys
import random
import time
import multiprocessing

def spawn_enemy(queue):
    time.sleep(4)
    queue.put((565, 439))  # Spawn enemy at the bottom-right block

def center_on_block(block_x, block_y, sprite_width, sprite_height):
    # Calculate the center position of Q*Bert based on the block's position
    block_center_x = block_x + sprite_width // 1.93  # Block center X
    block_center_y = block_y + sprite_height // 2  # Block center Y
    # Adjusting by a slight offset to ensure it's positioned correctly in relation to the block
    offset_x = 5  # Shift slightly to the right
    return [block_center_x - sprite_width // 2 + offset_x, block_center_y - sprite_height // 2]

def get_neighbors(blocks, current_index):
    # Given the index of the current block, get neighboring blocks (up, down, left, right)
    neighbors = []
    if current_index > 0:  # There's a block to the left
        neighbors.append(current_index - 1)
    if current_index + 1 < len(blocks):  # There's a block to the right
        neighbors.append(current_index + 1)
    return neighbors

if __name__ == "__main__":
    # Initialize Pygame and setup window only inside __main__ to avoid double windows.
    pygame.init()

    # Screen setup
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Qbrt")

    # Load sprites
    sprite1 = pygame.image.load(r"C:\Users\giann\Downloads\qbrt\Art\BaseBlock1.png")
    sprite2 = pygame.image.load(r"C:\Users\giann\Downloads\qbrt\Art\blueball.png")
    unsized = pygame.image.load(r"C:\Users\giann\Downloads\qbrt\Art\pstandingr.png")
    PstandingR = pygame.transform.scale(unsized, (48, 48))  # Scale Q*Bert sprite
    sprite1.set_colorkey((255, 255, 255))  # Transparent background for base blocks

    # Block positions (pyramid layout)
    block_positions = [
          (330, 40),   # Top
        (284, 120), (380, 120),
        (235, 200), (330, 199), (428, 200),
        (186, 281), (280, 279), (378, 279), (475, 279),
        (136, 360), (232, 358), (328, 358), (423, 358), (520, 358),
        (87, 439),  (186, 439), (280, 439), (375, 439), (470, 439), (565, 439),
        (38, 519) , (135, 519), (230, 519), (325, 519), (420, 519), (515, 519), (610, 519)
    ]

    # Set player position based on the first block
    current_block_index = 0
    player_pos = center_on_block(*block_positions[current_block_index], sprite1.get_width(), sprite1.get_height())

    # Enemy process setup
    enemy_queue = multiprocessing.Queue()
    enemy_process = multiprocessing.Process(target=spawn_enemy, args=(enemy_queue,))
    enemy_process.start()

    enemy_spawned = False
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:  # Move up-left
                    if current_block_index - 1 >= 0:
                        current_block_index -= 1
                elif event.key == pygame.K_e:  # Move up-right
                    if current_block_index + 1 < len(block_positions):
                        current_block_index += 1
                elif event.key == pygame.K_a:  # Move down-left
                    # Add logic to handle moving down-left, for now just moving left
                    if current_block_index - 1 >= 0:
                        current_block_index -= 1
                elif event.key == pygame.K_d:  # Move down-right
                    # Add logic to handle moving down-right, for now just moving right
                    if current_block_index + 1 < len(block_positions):
                        current_block_index += 1

                # Update player position based on the new block
                player_pos = center_on_block(*block_positions[current_block_index], sprite1.get_width(), sprite1.get_height())

        # Clear screen and redraw
        screen.fill((0, 0, 0))

        # Draw pyramid blocks
        for pos in block_positions:
            screen.blit(sprite1, pos)

        # Draw player sprite at current position
        screen.blit(PstandingR, player_pos)

        # Debug: Check if sprite is being drawn (print position)
        print(f"Player Position: {player_pos}")

        # Spawn enemy after a delay
        if not enemy_spawned and not enemy_queue.empty():
            enemy_pos = enemy_queue.get()
            screen.blit(sprite2, enemy_pos)
            enemy_spawned = True

        # Update the display
        pygame.display.flip()

    # Wait for enemy process to complete
    enemy_process.join()
    pygame.quit()
    sys.exit()
