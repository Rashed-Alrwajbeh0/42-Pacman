import pygame
import sys
from clones import PacMan


def draw_background(screen, image_path):
    screen.fill((0, 0, 0))

    image = pygame.image.load(image_path).convert()
    resized_image = pygame.transform.smoothscale(image, (1600, 900)).convert_alpha()

    resized_image.set_alpha(50)
    screen.blit(resized_image, (0, 0))


level_idx = 0


def get_level(cofiguration):
    global level_idx
    return cofiguration.levels[level_idx]


def game_play(screen, levels, cofiguration):
    level_maze, size = levels[0]
    level_conf = get_level(cofiguration)
    fram_clock = pygame.time.Clock()
    width = level_conf["width"]
    hight = level_conf["height"]
    center_cell = level_maze.center_cell()
    level_maze.get_pos((450, 50), size)
    x = (center_cell.left + center_cell.right) // 2
    y = (center_cell.top + center_cell.bottom) // 2
    pacman = PacMan(
        pos=(x, y),
        screen=screen,
        cell_size=size)
    direction = "right"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        draw_background(
                screen=screen, image_path="Pictures/Backgrounds/1.jpeg")
        level_maze.draw(screen, size, (450, 50))
        pygame.draw.circle(surface=screen,color="red",center=(x, y),radius=10)

        keyboard = pygame.key.get_just_pressed()
        if keyboard[pygame.K_UP]:
            direction = "top"
        elif keyboard[pygame.K_DOWN]:
            direction = "bottom"
        elif keyboard[pygame.K_RIGHT]:
            direction = "right"
        elif keyboard[pygame.K_LEFT]:
            direction = "left"
        pacman.move(
            grid_hight=hight,
            grid_width=width,
            grid_list=level_maze.grid,
            direction=direction,
            destance=7,
            size=size)
        pygame.display.update()
        fram_clock.tick(60)