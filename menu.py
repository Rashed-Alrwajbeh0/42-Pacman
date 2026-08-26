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
        return self.button_rec.collidepoint(point)


def in_pac_man(point):
    x, y = point
    return pow((x-280), 2) + pow((y-608), 2) <= pow(136, 2)


def show_menu(screen):
    menu_image = pygame.image.load("Pictures/menu/menu.png").convert()
    resized_menu = pygame.transform.scale(menu_image, (1600, 900))
    pac_man_rec = resized_menu.get_rect(center=(800, 450))
    screen.blit(resized_menu, pac_man_rec)
    start_button = Button(
        pos=(550, 330),
        text="Start Game",
        width=465,
        height=75,
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 255, 0),
        border_radius=100)
    high_score_button = Button(
        pos=(550, 410),
        text="High Scores",
        width=465,
        height=75,
        border=0,
        font_color=(0, 0, 0),
        border_color=(0, 0, 255),
        border_radius=100)
    controls_button = Button(
        pos=(550, 490),
        text="Controls",
        width=465,
        height=75,
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 0, 162),
        border_radius=100)
    sitting_button = Button(
        pos=(550, 570),
        text="Sitting",
        width=465,
        height=75,
        border=0,
        font_color=(0, 0, 0),
        border_color=(224, 224, 224),
        border_radius=100)
    exit_button = Button(
        pos=(550, 650),
        text="Exit Game",
        width=465,
        height=75,
        border=0,
        font_color=(0, 0, 0),
        border_color=(255, 128, 0),
        border_radius=100)

    start_button.draw(screen)
    high_score_button.draw(screen)
    controls_button.draw(screen)
    sitting_button.draw(screen)
    exit_button.draw(screen)
    if pygame.mouse.get_just_pressed()[0]:
        mouse_point = pygame.mouse.get_pos()
        if start_button.collision(mouse_point):
            return "start"
        elif high_score_button.collision(mouse_point):
            return "score"
        elif controls_button.collision(mouse_point):
            return "controls"
        elif sitting_button.collision(mouse_point):
            return "sitting"
        elif exit_button.collision(mouse_point):
            return "exit"
        return "menu"
    elif pygame.mouse.get_just_pressed()[2]:
        mouse_point = pygame.mouse.get_pos()
        if in_pac_man(mouse_point):
            return "cheet"
        return "menu"
    else:
        return "menu"