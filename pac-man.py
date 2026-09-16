import sys
import pygame
from conf import read_json
from menu import show_menu

argv = sys.argv
if len(argv) != 2:
    print("Error: You must enter exactly one argument !!")
    exit()
if not argv[1].endswith(".json"):
    print("Error: The file must be a .json file !!")
    exit()

configuration = read_json(argv[1])
pygame.init()

screen = pygame.display.set_mode((1600, 900))
frame_clock = pygame.time.Clock()

# try:
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#         show_menu(
#             screen=screen,
#             cofiguration=configuration,
#             fram_clock=frame_clock)
#         pygame.display.update()
#         frame_clock.tick(60)
# except KeyboardInterrupt:
#     print("\nProgram stopped by user (Ctrl+C).")
# except Exception as exc:
#     print(f"Error: Something went wrong ({exc}) !!")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    show_menu(
        screen=screen,
        cofiguration=configuration,
        fram_clock=frame_clock)
    pygame.display.update()
    frame_clock.tick(60)