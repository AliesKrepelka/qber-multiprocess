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
    block_center_x = block_x + sprite_width // 1.4  # Block center X
    block_center_y = block_y + sprite_height // 2.7  # Block center Y
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
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Qbrt")

    # Load sprites
    sprite1UN=  pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Level 1 top square unactivated.png")
    sprite1 = pygame.transform.scale(sprite1UN, (105,105))
    
    #sprite1 = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Level 1 top square unactivated.png")
    sprite2 = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/blueball.png")
    unsized = pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/pstandingr.png")
    PstandingR = pygame.transform.scale(unsized, (48, 48))  # Scale Q*Bert sprite
    sprite1.set_colorkey((255, 255, 255))  # Transparent background for base blocks

    # Block positions (pyramid layout)
    block_positions = [
        a := (330, 40),   # Top
        b := (284, 120), c := (380, 120),
        d := (235, 200), e := (330, 199), f := (428, 200),
        g := (186, 281), h := (280, 279), i := (378, 279), j := (475, 279),
        k := (136, 360), l := (232, 358), m := (328, 358), n := (423, 358), o := (520, 358),
        p := (87, 439),  q := (186, 439), r := (280, 439), s := (375, 439), t := (470, 439), u := (565, 439),
        v := (38, 519) , w := (135, 519), x := (230, 519), y := (325, 519), z := (420, 519), A := (515, 519), B := (610, 519)
    ]

    # Load and scale saucer frames
    saucer_frames = [
        pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Rainbow disc 1.png").convert_alpha(),
        pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Rainbow disc 2.png").convert_alpha(),
        pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Rainbow disc 3.png").convert_alpha(),
        pygame.image.load("C:/Users/GACarr7113/Downloads/python/Art/Rainbow disc 4.png").convert_alpha(),
    ]

    # Scale the saucer images to make them bigger
    saucer_size = (50, 50)  # Set the new size for the saucer
    saucer_frames = [pygame.transform.scale(frame, saucer_size) for frame in saucer_frames]

    # Set player position based on the first block
    current_block_index = 0
    player_pos = center_on_block(*block_positions[current_block_index], sprite1.get_width(), sprite1.get_height())

    # Enemy process setup
    enemy_queue = multiprocessing.Queue()
    enemy_process = multiprocessing.Process(target=spawn_enemy, args=(enemy_queue,))
    enemy_process.start()

    enemy_spawned = False
    run = True
    frame_index = 0
    animation_speed = 0.1

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
                    if current_block_index - 1 >= 0:
                        current_block_index -= 1
                elif event.key == pygame.K_d:  # Move down-right
                    if current_block_index + 1 < len(block_positions):
                        current_block_index += 1

                # Update player position based on the new block
                player_pos = center_on_block(*block_positions[current_block_index], sprite1.get_width(), sprite1.get_height())

        # Clear screen and redraw
        screen.fill((0, 0, 0))

        # Animation frame update
        frame_index += animation_speed
        if frame_index >= len(saucer_frames):
            frame_index = 0
        current_frame = saucer_frames[int(frame_index)]
        saucer_x, saucer_y = 110, 320
        screen.blit(current_frame, (110, 320))
        screen.blit(current_frame, (610, 320))

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
