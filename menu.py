import pygame
from math import pow


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
            font_path="fonts/Dunker.otf",
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
        self.button_rec = pygame.Rect(
                self.pos[0], self.pos[1], self.width, self.height)

    def draw(self, screen):
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


def show_menu(screen):
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
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 255, 0),
        border_radius=100,
        font_size=font_size)
    high_score_button = Button(
        pos=(button_x, int(410 * sy)),
        text="High Scores",
        width=button_width,
        height=button_height,
        border=0,
        font_color=(0, 0, 0),
        border_color=(0, 0, 255),
        border_radius=100,
        font_size=font_size)
    controls_button = Button(
        pos=(button_x, int(490 * sy)),
        text="Controls",
        width=button_width,
        height=button_height,
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 0, 162),
        border_radius=100,
        font_size=font_size)
    setting_button = Button(
        pos=(button_x, int(570 * sy)),
        text="Setting",
        width=button_width,
        height=button_height,
        border=0,
        font_color=(0, 0, 0),
        border_color=(224, 224, 224),
        border_radius=100,
        font_size=font_size)
    exit_button = Button(
        pos=(button_x, int(650 * sy)),
        text="Exit Game",
        width=button_width,
        height=button_height,
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 128, 0),
        border_radius=100,
        font_size=font_size)

    start_button.draw(screen)
    high_score_button.draw(screen)
    controls_button.draw(screen)
    setting_button.draw(screen)
    exit_button.draw(screen)

    if pygame.mouse.get_pressed()[0]:
        mouse_point = pygame.mouse.get_pos()
        if start_button.collision(mouse_point):
            return "game"
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
            return "cheet"
        return "menu"
    else:
        return "menu"
