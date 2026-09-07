import json
import pygame
from sys import exit
from menu import Button
from game import draw_background
from menu import show_menu


def check_name(name):
    if len(name) == 0:
        return 1
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


def add_name(name, level, score):
    if check_name(name):
        print(f"{name} name is already exsist !")
        return 0
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
            pos,
            width,
            height,
            border,
            border_color,
            border_radius,
            font_color,
            font_type="fonts/BebasNeue-Regular.ttf",
            font_size=40) -> None:

        self.pos = pos
        self.is_active = False
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
            filename=font_type,
            size=font_size)
        
    def collision(self, point):
        px, py = point
        button_x_left = self.Field_rect.left
        button_x_right = self.Field_rect.right
        button_y_top = self.Field_rect.top
        button_y_bottom = self.Field_rect.bottom
        return (px <= button_x_right and
                px >= button_x_left and
                py >= button_y_top and
                py <= button_y_bottom)

    def active(self):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.collision(mouse_pos):
                self.is_active = True

    def update_text(self, leter_id, leter):
        if self.is_active:
            if leter_id == -1:
                if len(self.text) > 0:
                    self.text = self.text[0:-1]
                    return 0
            elif leter_id == 1:
                self.is_active = False
                return 1
            else:
                if leter is not None:
                    self.text += leter
                return 0
                

    def draw(self, screen):
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


# def show_error(screen, text, pos, frame_clock):

#     error = Field(
#         pos=pos,
#         width=200,
#         height=20,
#         border=2,
#         border_color="red",
#         border_radius=10,
#         font_type="fonts/BebasNeue-Regular.ttf",
#         font_size=30,
#         font_color="red"
#     )
#     error.text = text
#     start_time = frame_clock.ger_ticks()
#     current_time = frame_clock.ger_ticks()
#     while (current_time - start_time < 5000):
#         error.draw(screen=screen)
#         current_time = frame_clock.ger_ticks()


def have_name_field(screen,
                    show_field,
                    field,
                    leter,
                    leter_id,
                    conf,
                    frame_clock):
    if show_field:
        field.draw(screen)
        if field.is_active:
            temp = field.update_text(leter_id, leter)
            if temp:
                check = check_name(field.text)
                if not check:
                    show_menu(screen=screen,
                              cofiguration=conf,
                              fram_clock=frame_clock)
                # else:
                #     show_error(screen,
                #                "This name is not ecxist !!",
                #                (500, 700),
                #                frame_clock)

        else:
            field.active()


def log_in_secreen(screen, frame_clock, conf):
    button1 = Button(
        pos=(500, 250),
        text="Have Name",
        height=110,
        width=600,
        border=10,
        font_color="white",
        border_color="yellow",
        border_radius=25,
        font_size=60)
    button2 = Button(
        pos=(500, 400),
        text="Create New Name",
        height=110,
        width=600,
        border=10,
        font_color="white",
        border_color="yellow",
        border_radius=25,
        font_size=60)
    field1 = Field(pos=(500, 550),
                   width=600,
                   height=110,
                   border=4,
                   border_color="black",
                   border_radius=20,
                   font_color="red"
                   )
    show_field_1 = False
    while True:
        leter = None
        leter_id = None
        
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
        if pygame.mouse.get_just_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if button1.collision(mouse_pos):
                show_field_1 = True
            elif button2.collision(mouse_pos):
                print(2)
        if show_field_1:
            have_name_field(screen=screen,
                            field=field1,
                            show_field=show_field_1,
                            leter_id=leter_id,
                            leter=leter,
                            conf=conf,
                            frame_clock=frame_clock)
        pygame.display.update()
        frame_clock.tick(60)