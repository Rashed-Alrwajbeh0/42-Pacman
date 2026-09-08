import sys
import pygame
from conf import read_json
from log_in import log_in_secreen

argv = sys.argv
configuration = read_json(argv[1])
pygame.init()

screen = pygame.display.set_mode((1600, 900))
frame_clock = pygame.time.Clock()
mode = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if mode == "game":
                mode = "menu"
            else:
                sys.exit()

    log_in_secreen(screen=screen,
                   frame_clock=frame_clock,
                   conf=configuration)

    pygame.display.update()
    frame_clock.tick(60)
