import sys
import pygame
from conf import read_json
from menu import show_menu

argv = sys.argv
t = read_json(argv[1])

pygame.init()
screen = pygame.display.set_mode((1600, 900))

fram_clock = pygame.time.Clock()
mode = "menu"
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    if mode == "menu":
        mode = show_menu(screen)
    elif mode == "exit":
        sys.exit()
    print(mode)
    pygame.display.update()
    fram_clock.tick(60)