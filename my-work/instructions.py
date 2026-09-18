import pygame
from sys import exit
from game import draw_background
from menu import Button


def show_instructions(screen: pygame.Surface) -> None:
    frame_clock = pygame.time.Clock()
    font = pygame.font.Font(
        "fonts//Roboto/static/Roboto_Condensed-Regular.ttf", size=40)
    font2 = pygame.font.Font(
        "fonts//Roboto/static/Roboto_Condensed-Regular.ttf")
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
                        image_path="Pictures/Backgrounds/instructions.png",
                        alpha=300)
        back.draw(
            screen=screen,
            image_pos=(25, 25),
            radius=60)
        text = font.render("HOW TO PLAY:", True, "red")
        screen.blit(text, (250, 170))
        t = ("To play this game, you are Pac-Man, and you must eat all the "
             "Pac-Gums and the four Super Pac-Gums.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 220))
        t = ("You also have to avoid being eaten by the ghosts, because"
             " you will lose a life!")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 250))
        t = ("The default keyboard keys for controlling Pac-Man are the "
             "Up Arrow, Down Arrow, Left Arrow, and Right Arrow.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 280))
        t = ("You can change these keys from the Controls page, "
             "which you can access by pressing the Controls button.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 310))
        t = ("You have to complete all 10 levels. With each level,"
             " the ghosts' speed will automatically increase,"
             " making the game harder.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 340))
        t = ("The Super Pac-Gums give you a special power for"
             " a limited time. During this period, the ghosts "
             "will avoid you, and you can eat them to")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 370))
        t = "earn extra points."
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 400))
        t = ("When you eat a Pac-Gum, Super Pac-Gum, "
             "or ghost, your score will increase. If your "
             "score is among the top 10 scores, it will appear")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 430))
        t = ("in the Top Scores list, which you can "
             "view by pressing the Scores button.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 460))
        t = ("Each level has a time limit. If you don't finish "
             "the level before time runs out, you lose!")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 480))
        text = font.render("The cheat mode", True, "red")
        screen.blit(text, (250, 520))
        t = ("In Cheat Mode, there are several "
             "features, such as stopping the timer, "
             "stopping the ghosts, making Pac-Man faster, "
             "adding a life,")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 570))
        t = ("skipping a level, and "
             "making Pac-Man invincible. Each feature"
             " has its own keyboard key.")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 600))
        t = ("The bad news is that you have to figure out "
             "how to enter Cheat Mode by yourself,"
             " and you must guess the keyboard key for each feature")
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 630))
        t = "on your own  :)"
        text = font2.render(t, True, "white")
        screen.blit(text, (250, 660))
        if pygame.mouse.get_just_pressed()[0]:
            pos = pygame.mouse.get_pos()
            if back.collision(pos):
                return
        pygame.display.update()
        frame_clock.tick(60)
