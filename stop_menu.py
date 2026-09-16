import pygame
from sys import exit

def show_stop_menu(screen: pygame.Surface):
    frame_clock = pygame.time.Clock
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        # --------------------------------------
        # |Wrtie The code of the Stop menu here|
        # --------------------------------------
         
        # return the value of the function and in the game file check 
        pygame.display.update()
        frame_clock.tick(60)





