import pygame
from sys import exit
from conf import confing
from game import draw_background


def show_score(screen: pygame.Surface,
               conf: confing):
    frame_clock = pygame.time.Clock()
    # font = pygame.font.Font(filename="onts/login.ttf", size=20)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        draw_background(screen=screen,
                        image_path="Pictures/Backgrounds/1.jpeg")
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 25),
                         end_pos=(1525, 25))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 100),
                         end_pos=(1525, 100))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 175),
                         end_pos=(1525, 175))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 250),
                         end_pos=(1525, 250))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 325),
                         end_pos=(1525, 325))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 400),
                         end_pos=(1525, 400))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 475),
                         end_pos=(1525, 475))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 550),
                         end_pos=(1525, 550))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 625),
                         end_pos=(1525, 625))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 700),
                         end_pos=(1525, 700))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 775),
                         end_pos=(1525, 775))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 850),
                         end_pos=(1525, 850))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(75, 25),
                         end_pos=(75, 850))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(1525, 25),
                         end_pos=(1525, 850))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(800, 25),
                         end_pos=(800, 850))
        pygame.draw.line(surface=screen,
                         color="white",
                         start_pos=(125, 25),
                         end_pos=(125, 850))     
        # text = font.render(text=1, antialias=False, color="white")
        # screen.blit(text, ())
        pygame.display.update()
        frame_clock.tick(60)

    