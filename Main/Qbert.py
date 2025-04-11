import pygame
import sys
import random
import time
import multiprocessing

# --- Helper Functions ---
def center_on_block(block_x, block_y, sprite_width, sprite_height):
    """Center the player sprite on a pyramid block."""
    block_center_x = block_x + (sprite_width // 1.9)
    block_center_y = block_y + (sprite_height // 6)
    return [block_center_x - 24, block_center_y - 24]  # Adjusted for 48x48 sprite

def get_valid_move(current_block, direction, movement_map):
    """Get next block in specified direction if valid."""
    destinations = movement_map.get(current_block, [])
    direction_map = {
        "up_left": 0,
        "up_right": 1,
        "down_left": 2,
        "down_right": 3
    }
    idx = direction_map.get(direction, -1)
    return destinations[idx] if 0 <= idx < len(destinations) else None

# --- Game Setup ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Q*bert")

    # Load assets
    block_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Level 1 top square unactivated.png"), 
        (105, 105)
    )
    player_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/pstandingr.png"), 
        (48, 48)
    )
    saucer_frames = [
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Rainbow disc 1.png").convert_alpha(),
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Rainbow disc 2.png").convert_alpha(),
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Rainbow disc 3.png").convert_alpha(),
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Rainbow disc 4.png").convert_alpha(),
    ]
    saucer_size = (50, 50)
    saucer_frames = [pygame.transform.scale(frame, saucer_size) for frame in saucer_frames]
    # Pyramid block positions (x, y coordinates)
    block_positions = [
        # Row 1 (top)
        a := (330, 40),
        
        # Row 2
        b := (284, 120), c := (380, 120),
        
        # Row 3
        d := (235, 200), e := (330, 200), f := (428, 200),
        
        # Row 4
        g := (186, 280), h := (280, 280), i := (378, 280), j := (475, 280),
        
        # Row 5
        k := (136, 360), l := (232, 360), m := (328, 360), n := (423, 360), o := (520, 360),
        
        # Row 6 (bottom)
        p := (87, 440), q := (186, 440), r := (280, 440), s := (375, 440), t := (470, 440), u := (565, 440)
    ]

    # Movement map: [up_left, up_right, down_left, down_right]
    movement_map = {
        # Row 1
        a: [None, None, b, c],
        
        # Row 2
        b: [a, None, d, e],
        c: [None, a, e, f],
        
        # Row 3
        d: [b, None, g, h],
        e: [b, c, h, i],
        f: [None, c, i, j],
        
        # Row 4
        g: [d, None, k, l],
        h: [d, e, l, m],
        i: [e, f, m, n],
        j: [None, f, n, o],
        
        # Row 5
        k: [g, None, p, q],
        l: [g, h, q, r],
        m: [h, i, r, s],
        n: [i, j, s, t],
        o: [None, j, t, u],
        
        # Row 6 (can't move down)
        p: [k, None, None, None],
        q: [k, l, None, None],
        r: [l, m, None, None],
        s: [m, n, None, None],
        t: [n, o, None, None],
        u: [None, o, None, None]
    }

    # Game state
    current_block = a
    player_pos = center_on_block(*current_block, block_sprite.get_width(), block_sprite.get_height())
    is_falling = False
    fall_speed = 8

    # --- Main Loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN and not is_falling:
                # Movement keys: Q/W (up), A/S (down)
                direction = None
                if event.key in (pygame.K_q, pygame.K_7):
                    direction = "up_left"
                elif event.key in (pygame.K_w, pygame.K_9):
                    direction = "up_right"
                elif event.key in (pygame.K_a, pygame.K_1):
                    direction = "down_left"
                elif event.key in (pygame.K_s, pygame.K_3):
                    direction = "down_right"

                if direction:
                    next_block = get_valid_move(current_block, direction, movement_map)
                    if next_block:
                        current_block = next_block
                        player_pos = center_on_block(*current_block, 
                                                     block_sprite.get_width(), 
                                                     block_sprite.get_height())
                    else:
                        is_falling = True

        # Falling mechanics
        if is_falling:
            player_pos[1] += fall_speed
            if player_pos[1] > 800:  # Reset when off-screen
                current_block = a
                player_pos = center_on_block(*current_block, 
                                           block_sprite.get_width(), 
                                           block_sprite.get_height())
                is_falling = False

        # --- Drawing ---
        screen.fill((0, 0, 0))
        
        # Draw pyramid
        for pos in block_positions:
            screen.blit(block_sprite, pos)
            
        # Draw player
        screen.blit(player_sprite, player_pos)
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()
