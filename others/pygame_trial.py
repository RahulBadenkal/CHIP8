import pygame
import time
import sys

pygame.init()

start_time = time.time()

locs = [(10, 15), (12, 15), (15, 15), (16, 15), (19, 15), (22, 15), (25, 15), (30, 15), (32, 15), (35, 15)]
i = 0

white = (255, 255, 255)
black = (0, 0, 0)
clock = pygame.time.Clock()
buf = pygame.Surface((64, 32))
scaled_res = (64*20, 32*20)
window = pygame.display.set_mode(scaled_res)
pygame.display.set_caption("CHIP-8")

count = 1
while True:
    buf.set_at(locs[i], white)
    pygame.transform.scale(buf, scaled_res, window)
    buf.fill(black)
    pygame.display.flip()
    clock.tick(2)  # Execute for loop n times per second
    print(count)

    i += 1

    if i >= len(locs):
        i = 0
    count += 1
    if time.time() - start_time >= 5:
        x = input()
        pygame.display.quit()
        pygame.quit()
        sys.exit()
