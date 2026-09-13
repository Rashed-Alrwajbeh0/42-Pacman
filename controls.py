import pygame
from sys import exit
from game import draw_background
from menu import Button
from typing import Optional
from menu import Button


def draw_table(screen: pygame.Surface) -> None:
    # draw the outside table
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500, 100),
        end_pos=(1100, 100),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500, 100),
        end_pos=(500, 800),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(1100, 100),
        end_pos=(1100, 800),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500, 800),
        end_pos=(1100, 800),
        width=2
    )
    # draw the insisde table
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500,200),
        end_pos=(1100, 200),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500,325),
        end_pos=(1100, 325),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500,450),
        end_pos=(1100, 450),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500,575),
        end_pos=(1100, 575),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(500,700),
        end_pos=(1100, 700),
        width=2
    )

    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(800,200),
        end_pos=(800, 700),
        width=2
    )

def draw_fonts(screen: pygame.Surface, font: pygame.Font):
    text = font.render("Pacman move up", False, "white")
    screen.blit(text, (510, 250))
    text = font.render("Pacman move right", False, "white")
    screen.blit(text, (510, 370))
    text = font.render("Pacman move down", False, "white")
    screen.blit(text, (510, 490))
    text = font.render("Pacman move left", False, "white")
    screen.blit(text, (510, 610))


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

    def update_text(
            self,
            leter_id: Optional[int],
            leter: Optional[str]) -> Optional[int]:
        if self.is_active:
            self.text = ""
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

    def draw(
            self,
            screen: pygame.Surface,
            x_space: int = 10,
            y_space: int = 5) -> None:
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
            (self.Field_rect.left + x_space, self.Field_rect.top + y_space))


def show_controls(
        screen: pygame.Surface,
        frame_clock: pygame.Clock,
        font_path: pygame.Font,
        field_containers: dict[str, str],
        movimg_dict: dict[str, pygame.Event]):
    Save_button = Button(
        pos=(500, 700),
        text="Save",
        width=602,
        height=102,
        font_color="white",
        border=2,
        border_color="red",
        border_radius=0,
    )
    font = pygame.font.Font(font_path, 30)
    font2 = pygame.font.Font(font_path, 25)
    up_field = Field(
        pos=(800, 200),
        width=302,
        height=127,
        border=2,
        border_color="red",
        border_radius=0,
        font_color="white",
        font_size=50,
        font_type=font_path
    )
    right_field = Field(
        pos=(800, 325),
        width=302,
        height=127,
        border=2,
        border_color="red",
        border_radius=0,
        font_color="white",
        font_size=50,
        font_type=font_path
    )
    down_field = Field(
        pos=(800, 450),
        width=302,
        height=127,
        border=2,
        border_color="red",
        border_radius=0,
        font_color="white",
        font_size=50,
        font_type=font_path
    )
    left_field = Field(
        pos=(800, 575),
        width=302,
        height=127,
        border=2,
        border_color="red",
        border_radius=0,
        font_color="white",
        font_size=50,
        font_type=font_path
    )
    leter: Optional[str] = None
    leter_id: Optional[int] = None
    right_field.text = field_containers["right"]
    left_field.text = field_containers["left"]
    down_field.text = field_containers["down"]
    up_field.text = field_containers["top"]
    leter_key = None
    rest_button1 = Button(
        pos=(1000, 202),
        text="RESET",
        height=123,
        width=100,
        border=2,
        border_radius=0,
        border_color="red",
        font_color="white",
        font_size=50
    )
    rest_button2 = Button(
        pos=(1000, 327),
        text="RESET",
        height=123,
        width=100,
        border=2,
        border_radius=0,
        border_color="red",
        font_color="white",
        font_size=50
    )
    rest_button3 = Button(
        pos=(1000, 452),
        text="RESET",
        height=123,
        width=100,
        border=2,
        border_radius=0,
        border_color="red",
        font_color="white",
        font_size=50
    )
    rest_button4 = Button(
        pos=(1000, 577),
        text="RESET",
        height=123,
        width=100,
        border=2,
        border_radius=0,
        border_color="red",
        font_color="white",
        font_size=50
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key not in [pygame.K_TAB, pygame.K_SPACE, pygame.K_ESCAPE]:
                    leter_id = 0
                    leter = event.unicode
                    leter_key = event.key
        draw_background(screen=screen,
                        image_path="Pictures/Backgrounds/1.jpeg")
        draw_table(screen=screen)
        text = font.render("Pacman moving controls", False, "white")
        screen.blit(text, (600, 125))
        draw_fonts(screen=screen, font=font2)
        Save_button.draw(screen=screen)
        up_field.draw(screen=screen, y_space=30)
        down_field.draw(screen=screen, y_space=30)
        left_field.draw(screen=screen, y_space=30)
        right_field.draw(screen=screen, y_space=30)
        rest_button1.draw(screen=screen)
        rest_button2.draw(screen=screen)
        rest_button3.draw(screen=screen)
        rest_button4.draw(screen=screen)
        if pygame.mouse.get_just_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if up_field.collision(pos):
                up_field.is_active = True
                down_field.is_active = False
                left_field.is_active = False
                right_field.is_active = False
            elif down_field.collision(pos):
                up_field.is_active = False
                down_field.is_active = True
                left_field.is_active = False
                right_field.is_active = False
            elif left_field.collision(pos):
                up_field.is_active = False
                down_field.is_active = False
                left_field.is_active = True
                right_field.is_active = False
            elif right_field.collision(pos):
                up_field.is_active = False
                down_field.is_active = False
                left_field.is_active = False
                right_field.is_active = True
        if leter:
            valus = list(movimg_dict.values())
            if leter_key not in valus:
                if up_field.is_active:
                    up_field.update_text(leter_id=leter_id, leter=leter)
                    movimg_dict["top"] = leter_key
                    field_containers["top"] = leter
                if down_field.is_active:
                    down_field.update_text(leter_id=leter_id, leter=leter)
                    movimg_dict["down"] = leter_key
                    field_containers["down"] = leter
                if left_field.is_active:
                    left_field.update_text(leter_id=leter_id, leter=leter)
                    movimg_dict["left"] = leter_key
                    field_containers["left"] = leter
                if right_field.is_active:
                    right_field.update_text(leter_id=leter_id, leter=leter)
                    movimg_dict["right"] = leter_key
                    field_containers["right"] = leter
            leter = None
            leter_key = None
        # up right down left 
        if pygame.mouse.get_just_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if rest_button1.collision(pos):
                movimg_dict["top"] = pygame.K_UP
                up_field.text = "Top"
                field_containers["top"] = "Top"
            elif rest_button2.collision(pos):
                movimg_dict["right"] = pygame.K_RIGHT
                right_field.text = "Right"
                field_containers["right"] = "Right"
            elif rest_button3.collision(pos):
                movimg_dict["down"] = pygame.K_DOWN
                down_field.text = "Down"
                field_containers["down"] = "Down"
            elif rest_button4.collision(pos):
                movimg_dict["left"] = pygame.K_LEFT
                left_field.text = "Left"
                field_containers["left"] = "Left"
            if Save_button.collision(pos):
                return movimg_dict, field_containers

        pygame.display.update()
        frame_clock.tick(60)
