import sys
import pygame
from conf import read_json
from menu import show_menu

argv = sys.argv
if len(argv) > 2:
    print("Error: You must enter just one argument !!")
    exit()
check = ""
n = -1
for i in range(5):
    check += argv[1][n]
    n -= 1
if check != "nosj.":
    print("Error: The file must be .json")
    exit()
configuration = read_json(argv[1])
pygame.init()

screen = pygame.display.set_mode((1600, 900))
frame_clock = pygame.time.Clock()
mode = "menu"
try:
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
except KeyboardInterrupt:
    print("\nError: Stop the program from the termonal using ctrl + c !!")