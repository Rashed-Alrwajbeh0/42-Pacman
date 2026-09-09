import sys
import pygame
from conf import read_json
from log_in import log_in_secreen
from scores import show_score
from menu import show_menu

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
    # show_score(screen=screen, conf=configuration)
    # log_in_secreen(screen=screen,
    #                frame_clock=frame_clock,
    #                conf=configuration)
    show_menu(
        screen=screen,
        cofiguration=configuration,
        fram_clock=frame_clock)
    pygame.display.update()
    frame_clock.tick(60)
