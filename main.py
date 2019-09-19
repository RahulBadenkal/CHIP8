from chip8 import Chip8State
import pygame
import sys


def update_keypad(chip8, keys):
    chip8.keypad[0] = keys[pygame.K_1]
    chip8.keypad[1] = keys[pygame.K_2]
    chip8.keypad[2] = keys[pygame.K_3]
    chip8.keypad[3] = keys[pygame.K_4]
    chip8.keypad[4] = keys[pygame.K_q]
    chip8.keypad[5] = keys[pygame.K_w]
    chip8.keypad[6] = keys[pygame.K_e]
    chip8.keypad[7] = keys[pygame.K_r]
    chip8.keypad[8] = keys[pygame.K_a]
    chip8.keypad[9] = keys[pygame.K_s]
    chip8.keypad[10] = keys[pygame.K_d]
    chip8.keypad[11] = keys[pygame.K_f]
    chip8.keypad[12] = keys[pygame.K_z]
    chip8.keypad[13] = keys[pygame.K_x]
    chip8.keypad[14] = keys[pygame.K_c]
    chip8.keypad[15] = keys[pygame.K_v]


def refresh_screen(chip8, buffer, white, black):
    for x in range(chip8.width):
        for y in range(chip8.height):
            if chip8.display[x][y] == 1:
                buffer.set_at((x, y), white)
            else:
                buffer.set_at((x, y), black)


def main():
    # Reading the rom data from file
    filename = "/home/rahul/projects/CHIP8/ROMS/PongForOne.ch8"
    with open(filename, 'rb') as f:
        rom_bytes = f.read()

    # Creating an instance of Chip8
    chip8 = Chip8State()

    # Set initial Chip8 states
    chip8.initialise()

    # Load the ROM in memory
    chip8.load_rom(rom_bytes)

    # Set up display and input systems using pygame
    pygame.init()
    white = (255, 255, 255)
    black = (0, 0, 0)
    scale = 20
    clock = pygame.time.Clock()
    resolution = (chip8.width, chip8.height)
    buf = pygame.Surface(resolution)
    scaled_res = (resolution[0] * scale, resolution[1] * scale)
    window = pygame.display.set_mode(scaled_res)
    pygame.display.set_caption("CHIP8")

    # Emulate cycles
    x = 0
    y = 0
    import time
    time_start = time.time()
    while True:
        x += 1
        y += 1
        clock.tick()  # Execute for loop n times per second
        events = pygame.event.get()

        # if x >= 10000:
        #     pygame.display.quit()
        #     pygame.quit()
        #     sys.exit()

        # Check if game is closed
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()

        # Read the key pressed info from pygame and change the keypad state
        keys = pygame.key.get_pressed()
        update_keypad(chip8, keys)

        # Emulate a cpu cycle (fetch-decode-execute)
        chip8.cpu_cycle()

        # Refresh the screen using pygame
        refresh_screen(chip8, buf, white, black)

        # TODO: What does this do
        pygame.transform.scale(buf, scaled_res, window)
        buf.fill(black)
        pygame.display.flip()
        clock.tick()

        # Decrement the delay timer
        if chip8.delay_timer > 0:
            chip8.delay_timer += -1

        # if time.time() - time_start > 1:
        #     print(y)
        #     y = 0
        #     time_start = time.time()


if __name__ == "__main__":
    # For pong multiplayer
    # For left player: 2-> Move up, q-> Move down,
    # For right player: z-> Move up, x->Move down
    main()





