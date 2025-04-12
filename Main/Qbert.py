import pygame
import sys
import random
import time
import multiprocessing

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

    # Load assets
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

    player_sprite = qbert_sprites["down_right"]

    saucer_frames = [
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Rainbow1.png").convert_alpha(),
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Rainbow2.png").convert_alpha(),
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Rainbow3.png").convert_alpha(),
        pygame.image.load("C:/Users/Alies Krepelka/Downloads/qber-multiprocess-main/Main/Art/Rainbow4.png").convert_alpha(),
    ]
    saucer_size = (50, 50)
    saucer_frames = [pygame.transform.scale(frame, saucer_size) for frame in saucer_frames]

    saucer_index = 0
    saucer_animation_speed = 0.15
    saucer_timer = 0

    saucer_positions = [
        (570, 230),
        (160, 230),
    ]

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
        b: [a, None, d, e],
        c: [None, a, e, f],
        d: [b, None, g, h],
        e: [b, c, h, i],
        f: [None, c, i, j],
        g: [d, None, k, l],
        h: [d, e, l, m],
        i: [e, f, m, n],
        j: [None, f, n, o],
        k: [g, None, p, q],
        l: [g, h, q, r],
        m: [h, i, r, s],
        n: [i, j, s, t],
        o: [None, j, t, u],
        p: [k, None, v, w],
        q: [k, l, w, x],
        r: [l, m, x, y],
        s: [m, n, y, z],
        t: [n, o, z, aa],
        u: [None, o, aa, ab],
        v: [p, None, None, None],
        w: [p, q, None, None],
        x: [q, r, None, None],
        y: [r, s, None, None],
        z: [s, t, None, None],
        aa: [t, u, None, None],
        ab: [u, None, None, None]
    }

    current_block = a
    player_pos = center_on_block(*current_block, block_sprite.get_width(), block_sprite.get_height())
    is_falling = False
    fall_speed = 8
    deaths = 0
    activated_blocks = set()

    clock = pygame.time.Clock()

    running = True
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
                        current_block = next_block
                        player_pos = center_on_block(*current_block,
                                                     block_sprite.get_width(),
                                                     block_sprite.get_height())
                        activated_blocks.add(current_block)
                        player_sprite = qbert_sprites[direction]
                    else:
                        is_falling = True

        if is_falling:
            player_pos[1] += fall_speed
            if player_pos[1] > 800:
                current_block = a
                player_pos = center_on_block(*current_block,
                                             block_sprite.get_width(),
                                             block_sprite.get_height())
                is_falling = False
                deaths += 1
                player_sprite = qbert_sprites["down_right"]

                if deaths >= 2:
                    current_block = a
                    player_pos = center_on_block(*current_block, block_sprite.get_width(), block_sprite.get_height())
                    is_falling = False
                    deaths = 0
                    player_sprite = qbert_sprites["down_right"]

        saucer_timer += dt
        if saucer_timer >= saucer_animation_speed:
            saucer_timer = 0
            saucer_index = (saucer_index + 1) % len(saucer_frames)

        screen.fill((0, 0, 0))

        for pos in block_positions:
            if pos in activated_blocks:
                screen.blit(block_activated_sprite, pos)
            else:
                screen.blit(block_sprite, pos)

        screen.blit(player_sprite, player_pos)

        for pos in saucer_positions:
            screen.blit(saucer_frames[saucer_index], pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()
