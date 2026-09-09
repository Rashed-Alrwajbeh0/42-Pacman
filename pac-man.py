import sys
import pygame
from conf import read_json
#from log_in import log_in_secreen
from menu import show_menu

argv = sys.argv
configuration = read_json(argv[1])
pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width, window_height = screen.get_size()
frame_clock = pygame.time.Clock()
mode = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        """if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if mode == "game":
                mode = "menu"
            else:
               sys.exit()"""

    show_menu(screen=screen,
              cofiguration=configuration,
              fram_clock=frame_clock)

    pygame.display.update()
    frame_clock.tick(60)
