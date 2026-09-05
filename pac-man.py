import sys
import pygame
from conf import read_json
from menu import show_menu
from maze import Maze
from cell import Cell

argv = sys.argv
configuration = read_json(argv[1])
pygame.init()

info = pygame.display.Info()
window_width = min(1600, info.current_w - 100)
window_height = min(900, info.current_h - 100)

screen = pygame.display.set_mode((window_width, window_height))
fram_clock = pygame.time.Clock()
mode = "menu"

maze = None
levels_list = [0]*10


def make_maszes(levels):
    global mode
    current_level = 0
    mode = "menu"

    while (current_level < 10):
        level_conf = configuration.levels[current_level]
        try:
            maze = Maze(
                width=level_conf["width"],
                height=level_conf["height"],
                seed=42 if current_level == 0 else 0,
                perfect=False,
                number_of_gums=configuration.pacgum
            )
            levels[current_level] = (
                maze,
                maze.cell_size_for(
                            window_width - 100,
                            window_height - 150
                            )
                    )
            current_level += 1
        except RuntimeError as exc:
            print(f"Warning: {exc}")
            levels = []
            break


mazes = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if mode == "game":
                mode = "menu"
            else:
                sys.exit()
    if not mazes:
        make_maszes(levels_list)
        if levels_list == []:
            print("Warning: The maze generator not found !!")
            sys.exit()
        mazes = True
    if mode == "menu":
        mode = show_menu(screen, levels=levels_list,cofiguration=configuration)

    elif mode == "exit":
        sys.exit()

    pygame.display.update()
    fram_clock.tick(60)
