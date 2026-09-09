import pygame
from sys import exit
from conf import confing
from game import draw_background
import json



def draw_cols_and_rows(screen):
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(75, 25),
        end_pos=(1525, 25))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(75, 100),
        end_pos=(1525, 100))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 175),
        end_pos=(1525, 175))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 250),
        end_pos=(1525, 250))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 325),
        end_pos=(1525, 325))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 400),
        end_pos=(1525, 400))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 475),
        end_pos=(1525, 475))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 550),
        end_pos=(1525, 550))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 625),
        end_pos=(1525, 625))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 700),
        end_pos=(1525, 700))
    pygame.draw.line(
        surface=screen,
        color="blue",
        start_pos=(75, 775),
        end_pos=(1525, 775))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(75, 850),
        end_pos=(1525, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(75, 25),
        end_pos=(75, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(1525, 25),
        end_pos=(1525, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(800, 25),
        end_pos=(800, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(125, 25),
        end_pos=(125, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(650, 25),
        end_pos=(650, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(850, 25),
        end_pos=(850, 850))
    pygame.draw.line(
        surface=screen,
        color="red",
        start_pos=(1400, 25),
        end_pos=(1400, 850))

def find_hight_scors() -> list[int]:
    try:
        with open("volum.json", "r") as f:
            json_data = json.load(f)
            scores: list[int] = json_data["scores"]
            names: list[str] = json_data["names"]
            if not scores:
                return []
            sorted_scores_by_the_idx = []
            sorted_namees_by_the_idx = []
            Range = len(scores)
            for i in range(Range):
                idx = scores.index(max(scores))
                print(idx)
                sorted_scores_by_the_idx.append(scores[idx])
                sorted_namees_by_the_idx.append(names[idx])
                names.pop(idx)
                scores.pop(idx)
            print(sorted_namees_by_the_idx)
            return (Range,
                    sorted_scores_by_the_idx,
                    sorted_namees_by_the_idx)
    except Exception:
        print("JSON file not found !")


def draw_numbers(screen: pygame.surface, font: pygame.font) -> None:
    temp = 80
    for i in range(1, 10):
        text = font.render(f"{i}", False, "white")
        screen.blit(text, (95, 40 + temp))
        temp += 75
    text = font.render("10", False, "white")
    screen.blit(text, (90, 40 + temp))
    temp = 80
    for i in range(11, 21):
        text = font.render(f"{i}", False, "white")
        screen.blit(text, (810, 40 + temp))
        temp += 75

def show_names_and_scores(screen: pygame.Surface,
                          font: pygame.Font) -> None:
    number_of_elemts, Scores, names = find_hight_scors()
    name_x_pos, name_y_pos = 150, 110
    score_x_pos, score_y_pos = 700, 110
    for i in range(number_of_elemts):
        if i == 20:
            break
        text = font.render(names[i], False, "white")
        screen.blit(text, (name_x_pos, name_y_pos))
        text = font.render(f"{Scores[i]}", False, "white")
        screen.blit(text, (score_x_pos, score_y_pos))
        name_y_pos += 75
        score_y_pos += 75
        if(i == 9):
            name_x_pos = 880
            score_x_pos = 1440
            name_y_pos = 110
            score_y_pos = 110


def show_score(screen: pygame.Surface,
               conf: confing) -> None:
    frame_clock = pygame.time.Clock()
    font = pygame.font.Font("fonts/BebasNeue-Regular.ttf", 30)
    font2 = pygame.font.Font("fonts/BebasNeue-Regular.ttf", 70)
    font3 = pygame.font.Font("fonts/BebasNeue-Regular.ttf", 50)
    from menu import Button
    back = Button(
        pos=(0, 0),
        text="",
        height=50,
        width=50,
        border=10,
        font_color="white",
        border_color="red",
        border_radius=50,
        image="Pictures/menu/back.png",
    )
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
        draw_background(screen=screen,
                        image_path="Pictures/Backgrounds/1.jpeg")
        draw_cols_and_rows(screen=screen)
        draw_numbers(screen=screen, font=font)
        text = font2.render("Name", False, "white")
        screen.blit(text, (320, 25))
        screen.blit(text, (1100, 25))
        text = font3.render("score", False, "white")
        screen.blit(text, (680, 35))
        screen.blit(text, (1415, 35))
        show_names_and_scores(screen=screen, font=font3)
        back.draw(
            screen=screen,
            image_pos=(25, 25),
            radius=60)
        if pygame.mouse.get_just_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if back.collision(pos):
                return
        pygame.display.update()
        frame_clock.tick(60)

    