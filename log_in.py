import json
import pygame
from sys import exit
from typing import Any, Optional, Union

from menu import Button
from conf import confing
from game import draw_background
from menu import show_menu


def check_name(name: str) -> Union[int, tuple[Any, Any]]:
    if len(name) == 0:
        return 0
    try:
        with open("volum.json", "r") as f:
            json_data = json.load(f)
            names = json_data["names"]
            if not names:
                return 0
            if name in names:
                idx = names.index(name)
                return (json_data["levels"][idx], json_data["scores"][idx])
            return 0
    except Exception:
        return 0


def add_name(name: str, level: int, score: int) -> None:
    with open("volum.json", "r") as f:
        json_data = json.load(f)
    with open("volum.json", "w") as f:
        names = json_data["names"]
        levels = json_data["levels"]
        scores = json_data["scores"]
        if not names:
            names = [name]
        else:
            names.append(name)
        if not levels:
            levels = [level]
        else:
            levels.append(level)
        if not scores:
            scores = [score]
        else:
            scores.append(score)
        json_dictt = {"names": names, "levels": levels, "scores": scores}
        json.dump(json_dictt, f)


class Field:
    def __init__(
            self,
            pos: tuple[int, int],
            width: int,
            height: int,
            border: int,
            border_color: str,
            border_radius: int,
            font_color: str,
            font_type: str = "fonts/1.ttf",
            font_size: int = 40) -> None:

        self.pos = pos
        self.is_active = False
        self.show_error = False
        self.Field_rect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            width,
            height
        )

        self.border = border
        self.border_color = border_color
        self.border_radius = border_radius

        self.text = ""
        self.font_color = font_color
        self.field_font_type = pygame.font.Font(
            font_type,
            font_size)

    def collision(self, point: tuple[int, int]) -> bool:
        px, py = point
        button_x_left = self.Field_rect.left
        button_x_right = self.Field_rect.right
        button_y_top = self.Field_rect.top
        button_y_bottom = self.Field_rect.bottom
        return (px <= button_x_right and
                px >= button_x_left and
                py >= button_y_top and
                py <= button_y_bottom)

    def active(self) -> None:
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.collision(mouse_pos):
                self.is_active = True

    def update_text(
            self,
            leter_id: Optional[int],
            leter: Optional[str]) -> Optional[int]:
        if self.is_active:
            if leter_id == -1:
                self.show_error = False
                if len(self.text) > 0:
                    self.text = self.text[0:-1]
                    return 0
            elif leter_id == 1:
                self.is_active = False
                return 1
            else:
                self.show_error = False
                if leter is not None:
                    self.text += leter
                return 0
        return None

    def draw(self, screen: pygame.Surface) -> None:
        self.font = self.field_font_type.render(
                self.text, False, self.font_color)
        pygame.draw.rect(
            surface=screen,
            color=self.border_color,
            border_radius=self.border_radius,
            width=self.border,
            rect=self.Field_rect
        )
        screen.blit(
            self.font,
            (self.Field_rect.left + 10, self.Field_rect.top + 5))


def show_error(screen: pygame.Surface, text: str,
               pos: tuple[int, int]) -> None:

    font = pygame.font.Font("fonts/1.ttf", size=20)
    text_in_font = font.render(text, False, "red")
    screen.blit(text_in_font, pos)


def use_name_field(
        screen: pygame.Surface,
        show_field: bool,
        field: Field,
        leter: Optional[str],
        leter_id: Optional[int],
        conf: confing,
        text_pos: tuple[int, int],
        text: str,
        text_height: int,
        text_width: int,
        frame_clock: pygame.time.Clock) -> None:
    if show_field:
        font = pygame.font.Font("fonts/1.ttf", size=20)
        text_in_font = font.render(text, False, "white")
        screen.blit(text_in_font, text_pos)
        field.draw(screen)
        if field.is_active:
            temp = field.update_text(leter_id, leter)
            if temp:
                check = check_name(field.text)
                if check:
                    show_menu(screen=screen,
                              cofiguration=conf,
                              fram_clock=frame_clock)
                else:
                    field.show_error = True
        else:
            field.active()


def create_name_field(
        screen: pygame.Surface,
        show_field: bool,
        field: Field,
        leter: Optional[str],
        leter_id: Optional[int],
        conf: confing,
        text_pos: tuple[int, int],
        text: str,
        text_height: int,
        text_width: int,
        frame_clock: pygame.time.Clock) -> None:
    if show_field:
        font = pygame.font.Font("fonts/1.ttf", size=20)
        text_in_font = font.render(text, False, "white")
        screen.blit(text_in_font, text_pos)
        field.draw(screen)
        if field.is_active:
            temp = field.update_text(leter_id, leter)
            if temp:
                check = check_name(field.text)
                if not check:
                    print(check)
                    add_name(field.text, 1, 0)
                    show_menu(screen=screen,
                              cofiguration=conf,
                              fram_clock=frame_clock)
                else:
                    field.show_error = True
        else:
            field.active()


def log_in_secreen(
        screen: pygame.Surface,
        frame_clock: pygame.time.Clock,
        conf: confing) -> None:
    button1 = Button(
        pos=(900, 250),
        text="Use Name",
        height=110,
        width=600,
        border=10,
        font_color="white",
        border_color="yellow",
        border_radius=25,
        font_size=60)
    button2 = Button(
        pos=(900, 400),
        text="Create New Name",
        height=110,
        width=600,
        border=10,
        font_color="white",
        border_color="yellow",
        border_radius=25,
        font_size=60)
    field1 = Field(pos=(900, 580),
                   width=600,
                   height=50,
                   border=0,
                   border_color="white",
                   border_radius=20,
                   font_color="black"
                   )
    show_field_1 = False
    field2 = Field(pos=(900, 580),
                   width=600,
                   height=50,
                   border=0,
                   border_color="white",
                   border_radius=20,
                   font_color="black")
    show_field_2 = False
    pacman = pygame.image.load("Pictures/login/pacman.png")
    resized_pacman = pygame.transform.smoothscale(pacman, (800, 900))
    while True:
        leter: Optional[str] = None
        leter_id: Optional[int] = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    leter_id = -1
                elif event.key == pygame.K_RETURN:
                    leter_id = 1
                else:
                    leter_id = 0
                    leter = event.unicode
        draw_background(
            screen=screen,
            image_path="Pictures/Backgrounds/1.jpeg",
            alpha=100)
        button1.draw(screen=screen)
        button2.draw(screen=screen)
        screen.blit(resized_pacman, (0, 0))
        if pygame.mouse.get_just_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if button1.collision(mouse_pos):
                show_field_1 = True
                show_field_2 = False
            elif button2.collision(mouse_pos):
                show_field_2 = True
                show_field_1 = False

        if show_field_1:
            use_name_field(screen=screen,
                           field=field1,
                           show_field=show_field_1,
                           leter_id=leter_id,
                           leter=leter,
                           conf=conf,
                           text_pos=(900, 550),
                           text_height=30,
                           text_width=120,
                           text="Enter yourname",
                           frame_clock=frame_clock)
            if field1.show_error:
                show_error(screen,
                           "This name is not exist !!", (900, 630))
        if show_field_2:
            create_name_field(screen=screen,
                              field=field2,
                              show_field=show_field_2,
                              leter_id=leter_id,
                              leter=leter,
                              conf=conf,
                              text_pos=(900, 550),
                              text_height=30,
                              text_width=120,
                              text="Enter The New name",
                              frame_clock=frame_clock)
            if field2.show_error:
                show_error(
                    screen,
                    "This name is used, try another one !!", (900, 630))
        pygame.display.update()
        frame_clock.tick(60)
