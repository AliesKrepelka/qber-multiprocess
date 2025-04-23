import pygame
import sys
import random
import time

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

# --- Game Setup ---
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Q*bert")

    # Load assets using Alies Krepelka paths
    block_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Level 1 top square unactivated.png"),
        (105, 105)
    )
    block_activated_sprite = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Level 1 top square activated.png"),
        (105, 105)
    )

    qbert_sprites = {
        "up_left": pygame.transform.scale(
            pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Qbert back left jump.png"), (48, 48)
        ),
        "up_right": pygame.transform.scale(
            pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Qbert back right jump.png"), (48, 48)
        ),
        "down_left": pygame.transform.scale(
            pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Qbert front left jump.png"), (48, 48)
        ),
        "down_right": pygame.transform.scale(
            pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/Qbert front right jump.png"), (48, 48)
        ),
    }

    player_sprite = qbert_sprites["down_right"]

    # Load score digit images
    digit_images = {
        str(i): pygame.transform.scale(
            pygame.image.load(f"C:/Users/giann/Downloads/qbrt/Art/score {i}.png"), (40, 40)
        )
        for i in range(10)
    }

    player_text_img = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/player text no number.png"), (150, 20)
    )
    player_num_img = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/player 1 number.png"), (20, 20)
    )

    change_to_img = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/change to text.png"), (150, 20)
    )
    change_block_img = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/level 1 change to icon.png"), (25, 25)
    )
    red_ball_jump = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/red jump.png"), (28, 28))
    red_ball_squish = pygame.transform.scale(
        pygame.image.load("C:/Users/giann/Downloads/qbrt/Art/red squish.png"), (28, 28))

    # --- Red Ball Animation Setup ---
    red_ball_frames = [red_ball_jump, red_ball_squish]  # Store jump and squish frames in a list
    red_ball_frame_index = 0
    red_ball_animation_timer = 0
    red_ball_animation_speed = 0.3  # lower = faster animation

    # Saucer animation
    saucer_frames = [
        pygame.image.load(f"C:/Users/giann/Downloads/qbrt/Art/Rainbow{i}.png").convert_alpha()
        for i in range(1, 5)
    ]
    saucer_size = (50, 50)
    saucer_frames = [pygame.transform.scale(frame, saucer_size) for frame in saucer_frames]

    saucer_index = 0
    saucer_animation_speed = 0.15
    saucer_timer = 0
    left_saucer = [(570, 230)]
    right_saucer = [(160, 230)]

    # Draw score
    def draw_score(score, x=15, y=40, spacing=10):
        score_str = str(score)
        for i, digit in enumerate(score_str):
            img = digit_images[digit]
            screen.blit(img, (x + i * (img.get_width() + spacing), y))

    # Block layout
    block_positions = [  # naming like a, b, c for movement map reference
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
        g: [left_saucer, d, k, l],
        h: [d, e, l, m],
        i: [e, f, m, n],
        j: [f, right_saucer, n, o],
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

    # Game variables
    red_ball_block = block_positions[1]  # Start just below Q*bert
    red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())
    red_ball_sprite = red_ball_jump
    red_ball_timer = 0
    red_ball_jump_delay = 0.8  # seconds between bounces

    current_block = block_positions[0]
    player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
    print(f"Current block: {current_block}")
    is_falling = False
    deaths = 0
    score = 0
    activated_blocks = set()
    fall_speed = 8  
    jump_time = .2
    jump_height = 10
    jump_start = None

    clock = pygame.time.Clock()

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

            # draw title text
            title_surf = title_font.render("Q*bert", True, (255, 204, 0))
            screen.blit(title_surf, (250, 100))

            # buttons
            if draw_button(screen, "PLAY", play_btn, (0, 128, 0), (0, 200, 0), font, mpos, mclick):
                return True    # signal to start game
            if draw_button(screen, "QUIT", quit_btn, (128, 0, 0), (200, 0, 0), font, mpos, mclick):
                pygame.quit()
                sys.exit()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.flip()
            clock.tick(60)

    # Show title screen and start game
    title_screen(screen)
    running = True

    # Main game loop
    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not is_falling:
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
                        jump_start = time.time()
                        current_block = next_block
                        player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
                        if current_block not in activated_blocks:
                            activated_blocks.add(current_block)
                            score += 25
                        player_sprite = qbert_sprites[direction]
                    else:
                        is_falling = True

        # Jump animation
        if jump_start is not None:
            jump_elapsed = time.time() - jump_start
            if jump_elapsed < jump_time:
                jump_progress = jump_elapsed / jump_time
                player_pos[1] -= jump_height * (1 - jump_progress)
            else:
                jump_start = None
                player_pos[1] = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())[1]

        red_ball_animation_timer += dt
        if red_ball_animation_timer >= red_ball_animation_speed:
            red_ball_animation_timer = 0
            red_ball_frame_index = (red_ball_frame_index + 1) % len(red_ball_frames)

        if is_falling:
            player_pos[1] += fall_speed
            if player_pos[1] > 800:
                deaths += 1
                is_falling = False
                current_block = block_positions[0]
                player_pos = center_on_block(current_block[0], current_block[1], block_sprite.get_width(), block_sprite.get_height())
                player_sprite = qbert_sprites["down_right"]
                if deaths >= 2:
                    deaths = 0
                    activated_blocks.clear()
                    score = 0

        red_ball_timer += dt
        if red_ball_timer >= red_ball_jump_delay:
            red_ball_timer = 0
            next_down = get_valid_move(red_ball_block, "down_left", movement_map)
            if not next_down:
                next_down = get_valid_move(red_ball_block, "down_right", movement_map)

            if next_down:
                red_ball_block = next_down
                red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())
            else:
                red_ball_block = block_positions[1]
                red_ball_pos = center_on_block(red_ball_block[0], red_ball_block[1], block_sprite.get_width(), block_sprite.get_height())

        saucer_timer += dt
        if saucer_timer >= saucer_animation_speed:
            saucer_timer = 0
            saucer_index = (saucer_index + 1) % len(saucer_frames)

        # Drawing
        screen.fill((0, 0, 0))
        for pos in block_positions:
            if pos in activated_blocks:
                screen.blit(block_activated_sprite, pos)
            else:
                screen.blit(block_sprite, pos)

        screen.blit(player_sprite, player_pos)

        for pos in left_saucer:
            screen.blit(saucer_frames[saucer_index], pos)
        for pos in right_saucer:
            screen.blit(saucer_frames[saucer_index], pos)

        screen.blit(player_text_img, (10, 10))
        screen.blit(player_num_img, (10 + player_text_img.get_width() + 10, 10))
        screen.blit(change_to_img, (10, 120))
        screen.blit(change_block_img, (85, 150))
        screen.blit(red_ball_frames[red_ball_frame_index], red_ball_pos)

        draw_score(score)
        pygame.display.flip()

    pygame.quit()
    sys.exit()
