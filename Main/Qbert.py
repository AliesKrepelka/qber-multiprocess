import pygame
import sys
import random
import time
import multiprocessing 


# Define the red ball logic function
def red_ball_logic(movement_map, start_block, queue, jump_delay):
    red_ball_block = start_block
    last_jump_time = time.time()

    while True:
        current_time = time.time()

        # Time to move the ball?
        if current_time - last_jump_time >= jump_delay:
            last_jump_time = current_time
            possible_moves = [move for move in movement_map.get(red_ball_block, []) if move is not None]
            valid_moves = [move for move in possible_moves if move[1] > red_ball_block[1]]

            if valid_moves:
                red_ball_block = random.choice(valid_moves)

            # Check if it hit the bottom
            if red_ball_block[1] >= 510:
                red_ball_block = start_block


            # Send updated block back to main process
            queue.put(red_ball_block)

        time.sleep(0.01)  # Short sleep to reduce CPU load


pygame.mixer.init()

jump_sound = pygame.mixer.Sound("C:\\Users\\Alies Krepelka\\Downloads\\qber-multiprocess-main\\jump.mp3")

# --- Helper Functions ---
def center_on_block(block_x, block_y, sprite_width, sprite_height):
    block_center_x = block_x + (sprite_width // 1.9)
    block_center_y = block_y + (sprite_height // 6)
    return [block_center_x - 24, block_center_y - 24]

def get_valid_move(current_block, direction, movement_map):
    destinations = movement_map.get(current_block, [])
    direction_map = {
        "up_left": 0,
        "up_right": 1,
        "down_left": 2,
        "down_right": 3
    }
    idx = direction_map.get(direction, -1)
    return destinations[idx] if 0 <= idx < len(destinations) else None

# --- Saucer Worker Process ---
def saucer_worker(queue):
    """Handles saucer movement in a separate process"""
    left_x, right_x = 575, 150  # Initial positions
    left_dx = 1
    right_dx = 1

    while True:
        # Update positions with bouncing logic
        left_x += left_dx
        right_x += right_dx

        # Reverse direction at boundaries
        if left_x < 540 or left_x > 575:
            left_dx *= -1
        if right_x < 150 or right_x > 185:
            right_dx *= -1

        # Send updated positions through the queue
        queue.put([(left_x, 230), (right_x, 230)])
        time.sleep(0.05)


def sound_worker(queue):
    """Handles sound playback in a separate process"""
    while True:
        # Wait for a sound play command from the main process
        sound_command = queue.get()
        
        if sound_command == 'jump':
            jump_sound.play()


# --- Game Setup ---
if __name__ == "__main__":
    # Required for Windows multiprocessing
    multiprocessing.set_start_method('spawn')
    
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Q*bert")

    sound_queue = multiprocessing.Queue()
   
    sound_process = multiprocessing.Process(target=sound_worker, args=(sound_queue,))
    sound_process.start()

    # --- Asset Loading ---
    block_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Level 1 top square unactivated.png"),
        (105, 105)
    )
    block_activated_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Level 1 top square activated.png"),
        (105, 105)
    )

    qbert_sprites = {
        "up_left": pygame.transform.scale(
            pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Qbert back left jump.png"), (48, 48)
        ),
        "up_right": pygame.transform.scale(
            pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Qbert back right jump.png"), (48, 48)
        ),
        "down_left": pygame.transform.scale(
            pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Qbert front left jump.png"), (48, 48)
        ),
        "down_right": pygame.transform.scale(
            pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Qbert front right jump.png"), (48, 48)
        ),
    }

    Life_sprite = {"life": pygame.transform.scale(
            pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Life counter.png"), (15, 15)
    )}
    player_sprite = qbert_sprites["down_right"]

    digit_images = {
        str(i): pygame.transform.scale(
            pygame.image.load(f"C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/score {i}.png"), (40, 40)
        )
        for i in range(10)
    }

    player_text_img = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/player text no number.png"), (150, 20)
    )
    player_num_img = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/player 1 number.png"), (20, 20)
    )

    change_to_img = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/change to text.png"), (150, 20)
    )
    change_block_img = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/level 1 change to icon.png"), (25, 25)
    )

    red_ball_jump = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/red jump.png"), (28, 28)
    )
    red_ball_squish = pygame.transform.scale(
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/red squish.png"), (28, 28)
    )

    red_ball_frames = [red_ball_jump, red_ball_squish]
    red_ball_frame_index = 0
    red_ball_animation_timer = 0
    red_ball_animation_speed = 0.3

    saucer_frames = [
        pygame.image.load(f"C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Rainbow disc {i}.png").convert_alpha()
        for i in range(1, 5)
    ]
    saucer_size = (50, 50)
    saucer_frames = [pygame.transform.scale(frame, saucer_size) for frame in saucer_frames]

    saucer_index = 0
    saucer_animation_speed = 0.15
    saucer_timer = 0

    def draw_score(score, x=15, y=40, spacing=10):
        score_str = str(score)
        for i, digit in enumerate(score_str):
            img = digit_images[digit]
            screen.blit(img, (x + i * (img.get_width() + spacing), y))

    # --- Game World Setup ---
    block_positions = [
        a := (330, 40),
        b := (284, 120), c := (380, 120),
        d := (235, 200), e := (330, 200), f := (428, 200),
        g := (186, 280), h := (280, 280), i := (378, 280), j := (475, 280),
        k := (136, 360), l := (232, 360), m := (328, 360), n := (423, 360), o := (520, 360),
        p := (87, 440), q := (186, 440), r := (280, 440), s := (375, 440), t := (470, 440), u := (565, 440),
        v := (40, 520), w := (136, 520), x := (232, 520), y := (328, 520), z := (423, 520), aa := (520, 520), ab := (615, 520)
    ]

    movement_map = {
        a: [None, None, b, c],
        b: [None, a, d, e],
        c: [a, None, e, f],
        d: [None, b, g, h],
        e: [b, c, h, i],
        f: [c, None, i, j],
        g: [None, d, k, l],  # Modified for saucer process
        h: [d, e, l, m],
        i: [e, f, m, n],
        j: [f, None, n, o],  # Modified for saucer process
        k: [None, g, p, q],
        l: [g, h, q, r],
        m: [h, i, r, s],
        n: [i, j, s, t],
        o: [j, None, t, u],
        p: [None, k, v, w],
        q: [k, l, w, x],
        r: [l, m, x, y],
        s: [m, n, y, z],
        t: [n, o, z, aa],
        u: [o, None, aa, ab],
        v: [None, p, None, None],
        w: [p, q, None, None],
        x: [q, r, None, None],
        y: [r, s, None, None],
        z: [s, t, None, None],
        aa: [t, u, None, None],
        ab: [u, None, None, None]
    }

    # --- Initialize Game State ---
    red_ball_block = block_positions[1]
    red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())
    red_ball_timer = 0
    red_ball_jump_delay = 0.8


    red_ball_queue = multiprocessing.Queue()

# Start the red ball logic in a separate process
    red_ball_process = multiprocessing.Process(
    target=red_ball_logic,
    args=(movement_map, block_positions[1], red_ball_queue, red_ball_jump_delay)
)

    red_ball_process.start()




   
    current_block = block_positions[0]
    player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
    is_falling = False
    lives = 3
    score = 0
    activated_blocks = set()
    fall_speed = 8
    jump_time = 0.2
    jump_height = 10
    jump_start = None
    clock = pygame.time.Clock()
    dt = clock.tick(60) / 1000 
    # --- Saucer Process Setup ---
    saucer_queue = multiprocessing.Queue()
    saucer_process = multiprocessing.Process(
        target=saucer_worker,
        args=(saucer_queue,)
    )
    saucer_process.start()
    saucer_positions = [(570, 230), (160, 230)]  # Initial positions


#WIN SCREEN
    def draw_win_screen():
        screen.fill((0, 0, 0))  # Black background
        font = pygame.font.SysFont(None, 80)
        text = font.render("YOU WIN!", True, (255, 215, 0))  # Gold text
        rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(text, rect)

    def check_win_condition():
        return all(blocks)



    # --- Title Screen ---
    def draw_button(screen, text, rect, color, hover_color, font, mouse_pos, mouse_click):
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, hover_color, rect)
            if mouse_click[0]:
                return True
        else:
            pygame.draw.rect(screen, color, rect)
        surf = font.render(text, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=rect.center))
        return False

    def title_screen(screen):
        font = pygame.font.SysFont(None, 60)
        title_font = pygame.font.SysFont(None, 100)
        play_btn = pygame.Rect(300, 250, 200, 80)
        quit_btn = pygame.Rect(300, 360, 200, 80)

        while True:
            screen.fill((30, 30, 30))
            mpos = pygame.mouse.get_pos()
            mclick = pygame.mouse.get_pressed()

            title_surf = title_font.render("Q*bert", True, (255, 204, 0))
            screen.blit(title_surf, (250, 100))

            if draw_button(screen, "PLAY", play_btn, (0, 128, 0), (0, 200, 0), font, mpos, mclick):
                return True
            if draw_button(screen, "QUIT", quit_btn, (128, 0, 0), (200, 0, 0), font, mpos, mclick):
                pygame.quit()
                sys.exit()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

    title_screen(screen)
    running = True

    # --- Game Over ---
    def game_over_screen(screen):
        font = pygame.font.SysFont(None, 100)
        start_time = time.time()

        while True:
            screen.fill((30, 30, 30))
            title_surf = font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(title_surf, (200, 350))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

            if time.time() - start_time >= 2:  # game over shows for 2 seconds
                return  
            
    # --- Main Game Loop ---
    while running:
        dt = clock.tick(60) / 1000.0

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not is_falling:
                direction = None
                if event.key in (pygame.K_q, pygame.K_7):
                    direction = "up_left"
                    sound_queue.put('jump')
                elif event.key in (pygame.K_w, pygame.K_9):
                    direction = "up_right"
                    sound_queue.put('jump')
                elif event.key in (pygame.K_a, pygame.K_1):
                    direction = "down_left"
                    sound_queue.put('jump') 
                elif event.key in (pygame.K_s, pygame.K_3):
                    direction = "down_right"
                    sound_queue.put('jump') 

                if direction:
                    next_block = get_valid_move(current_block, direction, movement_map)
                    if isinstance(next_block, list):
                        is_falling = True
                    elif next_block:
                        jump_start = time.time()
                        current_block = next_block
                        player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
                        if current_block not in activated_blocks:
                            activated_blocks.add(current_block)
                            score += 25
                        player_sprite = qbert_sprites[direction]
                    else:
                        is_falling = True


        # Player jump animation
        if jump_start:
            jump_elapsed = time.time() - jump_start
            if jump_elapsed < jump_time:
                jump_progress = jump_elapsed / jump_time
                player_pos[1] -= jump_height * (1 - jump_progress)
            else:
                jump_start = None
                player_pos[1] = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())[1]

        while not red_ball_queue.empty():
            red_ball_block = red_ball_queue.get()
            red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())


   # --- Red Ball Animation ---
        red_ball_animation_timer += dt
        if red_ball_animation_timer >= red_ball_animation_speed:
            red_ball_animation_timer = 0
            red_ball_frame_index = (red_ball_frame_index + 1) % len(red_ball_frames)

   # --- Red Ball Movement (get from the multiprocessing queue) ---
        try:
            while not red_ball_queue.empty():
                red_ball_block = red_ball_queue.get_nowait()
                red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())

        # Saucer animation
        except:
            saucer_timer += dt
        if saucer_timer >= saucer_animation_speed:
            saucer_timer = 0
            saucer_index = (saucer_index + 1) % len(saucer_frames)

        # Get updated saucer positions
        try:
            while True:  # Get latest positions
                saucer_positions = saucer_queue.get_nowait()
        except:
            pass

        # Falling logic
        if is_falling:
            player_pos[1] += fall_speed
            if player_pos[1] > 800:
                lives -= 1
                is_falling = False
                current_block = block_positions[0]
                player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
                player_sprite = qbert_sprites["down_right"]
                if lives <= 0:
                    game_over_screen(screen)
                    title_screen(screen)

                    lives = 3
                    activated_blocks.clear()
                    score = 0
                    current_block = block_positions[0]
                    player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
                    player_sprite = qbert_sprites["down_right"]


        # Collision detection
        if red_ball_block == current_block and not is_falling:
            is_falling = True

        # --- Rendering ---
        screen.fill((0, 0, 0))
        for pos in block_positions:
            sprite = block_activated_sprite if pos in activated_blocks else block_sprite
            screen.blit(sprite, pos)

        screen.blit(player_sprite, player_pos)

        # Draw moving saucers
        for pos in saucer_positions:
            screen.blit(saucer_frames[saucer_index], pos)

        screen.blit(player_text_img, (10, 10))
        screen.blit(player_num_img, (10 + player_text_img.get_width() + 10, 10))
        screen.blit(change_to_img, (10, 120))
        screen.blit(change_block_img, (85, 150))
        screen.blit(red_ball_frames[red_ball_frame_index], red_ball_pos)
    
        draw_score(score)

        def draw_lives(screen, lives, sprite):
            for i in range(lives):
                x = 20  # 20 pixels from the left
                y = 250 + i * (sprite.get_height() + 10)  # space between lives
                screen.blit(sprite, (x, y))

        draw_lives(screen, lives, Life_sprite["life"])

        pygame.display.flip()

    # --- Cleanup ---
    sound_process.terminate()
    sound_process.terminate()
    red_ball_process.terminate()
    red_ball_process.join()
    saucer_process.terminate()
    saucer_process.join()
    pygame.quit()
    sys.exit()
