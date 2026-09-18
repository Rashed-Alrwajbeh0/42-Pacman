import pygame
from sys import exit
from render import draw_background
from menu import Button
from typing import Optional


def draw_table(screen: pygame.Surface) -> None:
    "This function just draw some lines on the screen"
    pygame.draw.line(
            surface=screen,
            color="yellow",
            start_pos=(440, 250),
            end_pos=(1160, 250),
            width=3)

    pygame.draw.line(
            surface=screen,
            color="yellow",
            start_pos=(440, 380),
            end_pos=(1160, 380),
            width=3)

    pygame.draw.line(
            surface=screen,
            color="yellow",
            start_pos=(440, 510),
            end_pos=(1160, 510),
            width=3)

    pygame.draw.line(
            surface=screen,
            color="yellow",
            start_pos=(440, 635),
            end_pos=(1160, 635),
            width=3)


def draw_fonts(screen: pygame.Surface, font: pygame.Font) -> None:
    "This function just draw some fontts on the screen"
    text = font.render("Pacman move up", True, "white")
    screen.blit(text, (460, 290))
    text = font.render("Pacman move right", True, "white")
    screen.blit(text, (460, 420))
    text = font.render("Pacman move down", True, "white")
    screen.blit(text, (460, 550))
    text = font.render("Pacman move left", True, "white")
    screen.blit(text, (460, 670))


class Field:
    """
    A class representing an interactive text input field in Pygame.
    Attributes:-
        pos (tuple[int, int]):-
            The (x, y) coordinates of the top-left corner of the field.
        is_active (bool):-
            Flag indicating whether the field is currently active/selected.
        show_error (bool):-
            Flag indicating whether an error state is active.
        Field_rect (pygame.Rect):-
            The rectangular boundary of the text field.
        border (int):-
            The thickness of the field's border (0 for no fill/border styling).
        border_color (str | tuple[int, int, int]):-
            The color of the field's border.
        border_radius (int):-
            The corner radius for rounded borders.
        text (str):-
            The current text entered in the field.
        font_color (str | tuple[int, int, int]):-
            The color of the rendered text.
        field_font_type (pygame.font.Font):-
            The font object used for rendering text.
    """
    def __init__(
            self,
            pos: tuple[int, int],
            width: int,
            height: int,
            border: int,
            border_color: str | tuple[int, int, int],
            border_radius: int,
            font_color: str | tuple[int, int, int],
            font_type: str = "fonts/1.ttf",
            font_size: int = 40) -> None:
        """Initializes the Field instance with position,
        dimensions, and styling properties."""

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
        """
        Checks if a given point collides with the field.

        Args:
            point (tuple[int, int]): The (x, y) coordinates to check.

        Returns:
            bool:-
                True if the point is inside the field, False otherwise.
        """
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
        """
        Updates the text content based on
        user keyboard input when the field is active.

        Args:
            leter_id (Optional[int]):-
                Action identifier(-1 for backspace, 1 for enter, 0 for typing).
            leter (Optional[str]):-
                The unicode character typed by the user.

        Returns:
                1 if Enter is pressed
                0 during normal typing
                or None if inactive.
        """
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
        """
        Renders the text field border and its
        current text onto the game screen.

        Args:
            screen (pygame.Surface):-
                The target Pygame surface to draw onto.
            x_space (int):-
                Horizontal padding offset for the text inside the field.
            y_space (int):-
                Vertical padding offset for the text inside the field.

        Returns:
            None
        """
        self.font = self.field_font_type.render(
                self.text, True, self.font_color)
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
        font_path: str,
        field_containers: dict[str, str],
        movimg_dict: dict[str, int]) -> tuple[dict[str, int], dict[str, str]]:
    """
    Manages the controls configuration screen,
    allowing the user to view, customize,
    and reset movement keybindings for Pac-Man.

    Args:
        screen (pygame.Surface):
            The main Pygame display surface where elements are drawn.
        frame_clock (pygame.Clock):
            The clock object used to control the frame rate (FPS).
        font_path (str):
            The file path to the font used for rendering text.
        field_containers (dict[str, str]):
            A dictionary containing current text representations
            of the key bindings for directions("top", "down", "left", "right").
        movimg_dict (dict[str, int]):
            A dictionary mapping movement directions to Pygame key constants.

    Returns:
        tuple[dict[str, int], dict[str, str]]:-
            A tuple containing the updated 'movimg_dict'
        and 'field_containers' dictionaries after saving changes.
    """
    Save_button = Button(
        pos=(700, 800),
        text="Save",
        width=180,
        height=50,
        font_color="black",
        border=0,
        border_color=(255, 213, 0),
        border_radius=5,
        font_size=30
    )
    font = pygame.font.Font(font_path, 40)
    font2 = pygame.font.Font(font_path, 30)
    up_field = Field(
        pos=(800, 275),
        width=150,
        height=80,
        border=0,
        border_color=(255, 213, 0),
        border_radius=20,
        font_color="black",
        font_size=50,
        font_type=font_path
    )
    right_field = Field(
        pos=(800, 405),
        width=150,
        height=80,
        border=0,
        border_color=(255, 213, 0),
        border_radius=20,
        font_color="black",
        font_size=50,
        font_type=font_path
    )
    down_field = Field(
        pos=(800, 535),
        width=150,
        height=80,
        border=0,
        border_color=(255, 213, 0),
        border_radius=20,
        font_color="black",
        font_size=50,
        font_type=font_path
    )
    left_field = Field(
        pos=(800, 660),
        width=150,
        height=80,
        border=0,
        border_color=(255, 213, 0),
        border_radius=20,
        font_color="black",
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
        pos=(1000, 265),
        text="RESET",
        height=100,
        width=100,
        border=0,
        border_radius=100,
        border_color=(255, 213, 0),
        font_color="black",
        font_size=45
    )
    rest_button2 = Button(
        pos=(1000, 395),
        text="RESET",
        height=100,
        width=100,
        border=0,
        border_radius=100,
        border_color=(255, 213, 0),
        font_color="black",
        font_size=45
    )
    rest_button3 = Button(
        pos=(1000, 520),
        text="RESET",
        height=100,
        width=100,
        border=0,
        border_radius=100,
        border_color=(255, 213, 0),
        font_color="black",
        font_size=45
    )
    rest_button4 = Button(
        pos=(1000, 650),
        text="RESET",
        height=100,
        width=100,
        border=0,
        border_radius=100,
        border_color=(255, 213, 0),
        font_color="black",
        font_size=45
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key not in [pygame.K_TAB,
                                     pygame.K_SPACE,
                                     pygame.K_ESCAPE]:
                    leter_id = 0
                    leter = event.unicode
                    leter_key = event.key
        draw_background(
            screen=screen,
            image_path="Pictures/Backgrounds/controls.png",
            alpha=200)
        draw_table(screen=screen)
        text = font.render("Pacman moving controls", True, "yellow")
        screen.blit(text, (550, 170))
        draw_fonts(screen=screen, font=font2)
        Save_button.draw(screen=screen)
        up_field.draw(screen=screen, y_space=10)
        down_field.draw(screen=screen, y_space=10)
        left_field.draw(screen=screen, y_space=10)
        right_field.draw(screen=screen, y_space=10)
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
        if leter and leter_key:
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
