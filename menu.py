import pygame
from math import pow
from game import game_play
from sys import exit


class Button:
    def __init__(
            self,
            pos,
            text,
            width,
            height,
            border,
            font_color,
            border_color,
            border_radius,
            image=None,
            font_path="fonts/BebasNeue-Regular.ttf",
            font_size=50
            ) -> None:
        self.pos = pos
        self.text = text
        self.width = width
        self.height = height
        self.border = border
        self.font = font_path
        self.font_size = font_size
        self.font_color = font_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.image_border_color = "white"
        if image is not None:
            self.image = pygame.image.load(image)
            self.resized_image = pygame.transform.smoothscale(
                self.image, (50, 50))
        self.button_rec = pygame.Rect(
                self.pos[0], self.pos[1], self.width, self.height)

    def draw(self, screen, image_pos=None):
        font = pygame.font.Font(self.font, size=self.font_size)
        button_text = font.render(self.text, False, self.font_color)
        button_text_rec = button_text.get_rect(
            center=(self.button_rec.center))
        pygame.draw.rect(
                surface=screen,
                color=self.border_color,
                rect=(self.pos[0], self.pos[1], self.width, self.height),
                width=self.border,
                border_radius=self.border_radius)
        screen.blit(button_text, button_text_rec)
        if image_pos:
            self.image_rect = self.resized_image.get_rect(center=image_pos)
            pygame.draw.rect(
                surface=screen,
                color="white",
                rect=self.image_rect,
                width=0,
                border_radius=15
            )
            screen.blit(self.resized_image, self.image_rect)

    def collision(self, point):
        px, py = point
        button_x_left = self.button_rec.left
        button_x_right = self.button_rec.right
        button_y_top = self.button_rec.top
        button_y_bottom = self.button_rec.bottom
        return (px <= button_x_right and
                px >= button_x_left and
                py >= button_y_top and
                py <= button_y_bottom)


def in_pac_man(point, screen_width, screen_height):
    x, y = point
    cx = 280 * screen_width / 1600
    cy = 608 * screen_height / 900
    radius = 136 * min(screen_width / 1600, screen_height / 900)
    return pow((x - cx), 2) + pow((y - cy), 2) <= pow(radius, 2)


def menu_init(screen):
    screen_width, screen_height = screen.get_size()
    menu_image = pygame.image.load("Pictures/menu/menu.png").convert()
    resized_menu = pygame.transform.scale(
        menu_image, (screen_width, screen_height))
    screen.blit(resized_menu, (0, 0))

    sx = screen_width / 1600
    sy = screen_height / 900
    button_width = int(465 * sx)
    button_height = int(75 * sy)
    button_x = int(550 * sx)
    font_size = max(int(50 * min(sx, sy)), 10)

    start_button = Button(
        pos=(button_x, int(330 * sy)),
        text="Start Game",
        width=button_width,
        height=button_height,
        border=5,
        image="Pictures/bottoms/Start.png",
        font_color="white",
        border_color=(255, 255, 0),
        border_radius=100,
        font_size=font_size)
    high_score_button = Button(
        pos=(button_x, int(410 * sy)),
        text="High Scores",
        width=button_width,
        height=button_height,
        border=5,
        image="Pictures/bottoms/scores.png",
        font_color="white",
        border_color="pink",
        border_radius=100,
        font_size=font_size)
    controls_button = Button(
        pos=(button_x, int(490 * sy)),
        text="Controls",
        width=button_width,
        height=button_height,
        border=5,
        image="Pictures/bottoms/control.png",
        font_color="white",
        border_color="purple",
        border_radius=100,
        font_size=font_size)
    setting_button = Button(
        pos=(button_x, int(570 * sy)),
        text="Setting",
        width=button_width,
        height=button_height,
        border=5,
        image="Pictures/bottoms/setting.png",
        font_color="white",
        border_color="blue",
        border_radius=100,
        font_size=font_size)
    exit_button = Button(
        pos=(button_x, int(650 * sy)),
        text="Exit Game",
        width=button_width,
        height=button_height,
        border=5,
        image="Pictures/bottoms/exit.png",
        font_color="white",
        border_color=(255, 128, 0),
        border_radius=100,
        font_size=font_size)
    return [start_button,
            high_score_button,
            controls_button,
            setting_button,
            exit_button]


def show_menu(screen, cofiguration, fram_clock):
    bottoms = menu_init(screen=screen)
    start_button = bottoms[0]
    high_score_button = bottoms[1]
    controls_button = bottoms[2]
    setting_button = bottoms[3]
    exit_button = bottoms[4]
    screen_width, screen_height = screen.get_size()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        start_button.draw(screen, (620, 367))
        high_score_button.draw(screen, (620, 450))
        controls_button.draw(screen, (620, 527))
        setting_button.draw(screen, (620, 607))
        exit_button.draw(screen, (620, 687))

        if pygame.mouse.get_pressed()[0]:
            mouse_point = pygame.mouse.get_pos()
            if start_button.collision(mouse_point):
                game_play(screen=screen, cofiguration=cofiguration)
            elif high_score_button.collision(mouse_point):
                return "score"
            elif controls_button.collision(mouse_point):
                return "controls"
            elif setting_button.collision(mouse_point):
                return "sitting"
            elif exit_button.collision(mouse_point):
                return "exit"
            return "menu"
        elif pygame.mouse.get_pressed()[2]:
            mouse_point = pygame.mouse.get_pos()
            if in_pac_man(mouse_point, screen_width, screen_height):
                print(1)
        pygame.display.update()
        fram_clock.tick(60)
