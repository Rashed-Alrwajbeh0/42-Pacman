from ghost_entity import Ghost, Ghoststate
from cell import PacMan, Super_Pac_Gum
from config import confing
from maze import Maze
from hud import draw_hud
from render import draw_background
from pause import show_pause_menu
import pygame
import sys
from ghost import (
    chase_then_flee,
    next_step_towards,
    ghost_speed_for_level,
    random_walk,
    seek_pacgum_near_player,
)
from typing import Any


current_level = 0
HUD_HEIGHT = 60
MARGIN = 20
EDIBLE_DURATION = 8.0
HUD_PANEL_WIDTH = 450
MAZE_ORIGIN = (HUD_PANEL_WIDTH, 50)

BACKGROUND_IMAGE = "Pictures/Backgrounds/7.png"
WALL_COLOR = (0, 209, 255)
_ACCENT_GOLD = (255, 213, 0)


def check_ghost_collisions(
        ghosts: list[Ghost],
        pacman: PacMan,
        points_per_ghost: int,
        collision_radius: float,
        cheat: bool
) -> tuple[bool, int]:
    """Check collisions between ghosts and the player.

    Args:
        ghosts: List of active ghosts.
        pacman: The player entity.
        points_per_ghost: Points awarded for eating an edible ghost.
        collision_radius: Pixel distance under which a collision is
            registered. Should scale with the current cell size.

    Returns:
        A tuple (life_lost, points_gained): whether the player lost a
        life this frame, and any points gained from eating ghosts.
    """
    life_lost = False
    points_gained = 0
    px, py = pacman.pos

    for ghost in ghosts:
        if ghost.state in (Ghoststate.Eaten, Ghoststate.Waiting):
            continue
        if ghost.pixel_pos is None:
            continue
        gx, gy = ghost.pixel_pos
        distance_sq = (px - gx) ** 2 + (py - gy) ** 2
        if distance_sq <= collision_radius ** 2:
            if ghost.state == Ghoststate.Edible:
                if not cheat:
                    ghost.get_eaten()
                    points_gained += points_per_ghost
            else:
                life_lost = True

    return life_lost, points_gained


def compute_layout(
        window_width: int,
        window_height: int,
        maze_width: int,
        maze_height: int,
        origin: tuple[int, int] = MAZE_ORIGIN,
) -> int:
    """Compute the cell size that best fits the maze into the space
    available between `origin` and the real screen edges, keeping
    the original fixed (450, 50) maze position from your design.

    Args:
        window_width: Real screen/window width in pixels.
        window_height: Real screen/window height in pixels.
        maze_width: Maze width in cells.
        maze_height: Maze height in cells.
        origin: Fixed top-left pixel position of the maze (unchanged
            from your original design).

    Returns:
        The cell size in pixels.
    """
    origin_x, origin_y = origin
    available_width = max(window_width - origin_x - MARGIN, 1)
    available_height = max(
        window_height - origin_y - HUD_HEIGHT - MARGIN, 1)

    cell_size = min(
        available_width // maze_width,
        available_height // maze_height,
    )
    return max(cell_size, 1)


def make_level(
        configuration: confing,
        window_width: int,
        window_height: int,
) -> tuple[Maze, int]:
    """Build a new maze, with its cell size fitted to the actual
    screen resolution while keeping the (450, 50) origin."""
    global current_level
    level_conf = configuration.levels
    try:
        maze = Maze(
            width=level_conf["width"],
            height=level_conf["height"],
            seed=42 if current_level == 0 else 0,
            perfect=False,
            number_of_gums=configuration.pacgum,
        )
        cell_size = compute_layout(
            window_width, window_height, maze.width, maze.height)
        maze.put_pacgums_in_cells(
            cell_size=cell_size, origin=MAZE_ORIGIN, conf=configuration)
        current_level += 1
        return maze, cell_size
    except RuntimeError as exc:
        print(f"Warning: {exc}")
        sys.exit(1)


def where_i_am(
        point: tuple[int, int],
        cell_size: int,
        origin: tuple[int, int],
        maze: Maze,
) -> tuple[int, int]:
    """Thi functio take the pos in pixel and determain
    the index of the cell that contain it"""
    ox, oy = origin
    px, py = point
    grid_x = max(0, min(maze.width - 1, (px - ox) // cell_size))
    grid_y = max(0, min(maze.height - 1, (py - oy) // cell_size))
    return grid_x, grid_y


def game_init(screen: pygame.Surface, cofiguration: confing) -> Any:
    origin = MAZE_ORIGIN
    window_width, window_height = screen.get_size()
    level_maze, size = make_level(
        configuration=cofiguration,
        window_width=window_width,
        window_height=window_height,
    )
    """
    Initializes the game state, maze structure, player (Pac-Man),
    ghosts, timers, and configuration settings required to run a level.

    Args:
        screen (pygame.Surface): The main Pygame display surface for the game.
        cofiguration (confing):
            The configuration object containing level settings, lives,
                and timing rules.

    Returns:
        tuple: A large tuple containing all initialized game variables:
            - fram_clock (pygame.time.Clock):
                Clock object for managing the frame rate.
            - pacman (PacMan):
                The initialized player instance.
            - level_maze (Maze):
                The generated level maze layout.
            - size (int/float):
                The calculated cell size for the maze.
            - origin (tuple):
                The origin coordinate offset of the maze.
            - hight (int):
                The height dimensions from the configuration.
            - width (int):
                The width dimensions from the configuration.
            - ghosts (list[Ghost]):
                A list of initialized ghost instances.
            - collision_radius (float):
                The collision radius boundary for entities.
            - ghost_speed (float/int):
                The movement speed calculated for the ghosts.
            - Invincibility (bool):
                Flag indicating invincibility status (default False).
            - Ghost_freeze (bool):
                Flag indicating if ghosts are frozen (default False).
            - Increased_speed (bool):
                Flag indicating speed boost status (default False).
            - score (int):
                The initial player score (0).
            - edible_timer (float):
                Timer for edible ghosts mechanic (0.0).
            - time_left (float):
                Remaining time for the level.
            - direction (str):
                Initial movement direction ("right").
            - Stop_timer (bool):
                Flag indicating if the level timer is stopped (default False).
    """
    fram_clock = pygame.time.Clock()
    width = cofiguration.levels["width"]
    hight = cofiguration.levels["height"]
    edible_timer = 0.0
    lives = cofiguration.lives
    time_left = float(cofiguration.level_max_time)

    level_maze.get_pos(origin, size)
    center_cell = level_maze.center_cell()
    direction = "right"
    score = 0
    if (center_cell.left is None or center_cell.right is None or
            center_cell.top is None or center_cell.bottom is None):
        raise RuntimeError("center cell position was not computed")
    x = (center_cell.left + center_cell.right) // 2
    y = (center_cell.top + center_cell.bottom) // 2
    pacman = PacMan(pos=(x, y), screen=screen, cell_size=size, lives=lives)

    corners = [
        (0, 0),
        (level_maze.width - 1, 0),
        (0, level_maze.height - 1),
        (level_maze.width - 1, level_maze.height - 1),
    ]
    ghost_speed = ghost_speed_for_level(current_level, 100, 5, 140)
    ghosts = [
        Ghost(
            corners[0],
            corners[0],
            (255, 0, 0),
            chase_then_flee,
            speed=ghost_speed),
        Ghost(
            corners[1],
            corners[1],
            (255, 165, 0),
            next_step_towards,
            speed=ghost_speed),
        Ghost(
            corners[2],
            corners[2],
            (255, 105, 180),
            seek_pacgum_near_player,
            speed=ghost_speed),
        Ghost(
            corners[3],
            corners[3],
            (0, 200, 255),
            random_walk,
            speed=ghost_speed),
    ]
    collision_radius = max(size / 2, 12.0)
    Invincibility = False
    Ghost_freeze = False
    Increased_speed = False
    Stop_timer = False
    return (fram_clock,
            pacman,
            level_maze,
            size,
            origin,
            hight,
            width,
            ghosts,
            collision_radius,
            ghost_speed,
            Invincibility,
            Ghost_freeze,
            Increased_speed,
            score,
            edible_timer,
            time_left,
            direction,
            Stop_timer)


def game_play(
        screen: pygame.Surface,
        cofiguration: confing,
        direction_key: dict[str, int],
        cheat: bool = False) -> tuple[str, int]:
    """
    Manages the main game loop for a Pac-Man level, handling player movement,
    ghost updates, collision detection, score keeping, timers, and cheat keys.

    Args:
        screen (pygame.Surface):
            The main Pygame display surface for rendering the game.
        cofiguration (confing):
            The configuration object providing level rules, dimensions,
                lives, and timing limits.
        direction_key (dict[str, int]):
            A dictionary mapping direction strings ("top", "bottom",
                "left", "right") to Pygame key constants.
        cheat (bool):
            Flag enabling special cheat key bindings (F1-F6) for testing.

    Returns:
        tuple[str, int]:
            A tuple containing the game outcome status ("win" or "lose")
                and the final player score achieved.
    """
    global current_level
    if current_level:
        current_level = 0
    (fram_clock,
     pacman,
     level_maze,
     size,
     origin,
     hight,
     width,
     ghosts,
     collision_radius,
     ghost_speed,
     Invincibility,
     Ghost_freeze,
     Increased_speed,
     score,
     edible_timer,
     time_left,
     direction,
     Stop_timer) = game_init(screen=screen, cofiguration=cofiguration)

    pause_button_rect = pygame.Rect(20, 20, 100, 40)
    while True:
        dt = fram_clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    action = show_pause_menu(screen, fram_clock)
                    if action == "lose":
                        return "lose", score
                if cheat:
                    if event.key == pygame.K_F1:
                        Invincibility = not Invincibility
                    if event.key == pygame.K_F2:
                        (fram_clock,
                         pacman,
                         level_maze,
                         size,
                         origin,
                         hight,
                         width,
                         ghosts,
                         collision_radius,
                         ghost_speed,
                         Invincibility,
                         Ghost_freeze,
                         Increased_speed,
                         score,
                         edible_timer,
                         time_left,
                         direction,
                         Stop_timer) = game_init(
                             screen=screen,
                             cofiguration=cofiguration)
                        continue
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button_rect.collidepoint(event.pos):
                    action = show_pause_menu(screen, fram_clock)
                    if action == "menu":
                        return "menu", score
                    if event.key == pygame.K_F3:
                        pacman.lives += 1
                    if event.key == pygame.K_F4:
                        Increased_speed = not Increased_speed
                    if event.key == pygame.K_F5:
                        Ghost_freeze = not Ghost_freeze
                    if event.key == pygame.K_F6:
                        Stop_timer = not Stop_timer

        draw_background(screen=screen, image_path=BACKGROUND_IMAGE, alpha=100)
        level_maze.draw(
            screen,
            size,
            origin,
            wall_color=WALL_COLOR,
            pattern_color=WALL_COLOR)

        pygame.draw.rect(
            screen, _ACCENT_GOLD, pause_button_rect, border_radius=10)
        pause_text = pygame.font.SysFont(None, 28).render("Pause",
                                                          True, "black")
        screen.blit(
            pause_text, pause_text.get_rect(center=pause_button_rect.center))

        keyboard = pygame.key.get_pressed()
        if keyboard[direction_key["top"]]:
            direction = "top"
        elif keyboard[direction_key["down"]]:
            direction = "bottom"
        elif keyboard[direction_key["right"]]:
            direction = "right"
        elif keyboard[direction_key["left"]]:
            direction = "left"

        if cheat and Increased_speed:
            P_speed = 4
        else:
            P_speed = 2
        pacman.move(
            grid_hight=hight,
            grid_width=width,
            grid_list=level_maze.grid,
            direction=direction,
            destance=P_speed,
            size=size,
        )

        player_x, player_y = where_i_am(
            point=pacman.pos, cell_size=size, origin=origin, maze=level_maze
        )
        current_cell = level_maze.grid[player_y][player_x]

        if current_cell.content_id != 0 and current_cell.content is not None:
            score += getattr(current_cell.content, 'points', 10)

            if isinstance(current_cell.content, Super_Pac_Gum):
                for ghost in ghosts:
                    if ghost.state != Ghoststate.Eaten:
                        ghost.become_eddible()
                edible_timer = EDIBLE_DURATION

            current_cell.content = None
            current_cell.content_id = 0

        if edible_timer > 0:
            edible_timer -= dt
        for ghost in ghosts:
            if edible_timer <= 0 and ghost.state in (
                                            Ghoststate.Edible,
                                            Ghoststate.Waiting):
                ghost.state = Ghoststate.Chasing
        player_cell = where_i_am(
            point=pacman.pos, cell_size=size, origin=origin, maze=level_maze)
        if cheat and Ghost_freeze:
            G_speed = 0
        else:
            G_speed = ghost_speed
        for ghost in ghosts:
            ghost.update(level_maze, player_cell, dt, size, origin, G_speed)

        life_lost, points_gained = check_ghost_collisions(
            ghosts,
            pacman,
            cofiguration.points_per_ghost,
            collision_radius,
            Invincibility)
        score += points_gained
        if not Stop_timer:
            time_left -= dt
        if time_left <= 0 or life_lost:
            try:
                if cheat and Invincibility:
                    Cheat = 1
                else:
                    Cheat = 0
                pacman.reset_atfer_eaten(cheat=Cheat)
            except ValueError:
                return "lose", score
            time_left = float(cofiguration.level_max_time)
            if not Invincibility:
                for ghost in ghosts:
                    ghost.grid_pos = ghost.corner
                    ghost.target_pos = ghost.corner
                    ghost.pixel_pos = None
                    ghost.state = Ghoststate.Chasing

        if level_maze.remaining_pacgums() == 0:
            if current_level >= 10:
                current_level = 0
                return "win", score
            remaining_lives = pacman.lives
            (fram_clock,
             pacman,
             level_maze,
             size,
             origin,
             hight,
             width,
             ghosts,
             collision_radius,
             ghost_speed,
             Invincibility,
             Ghost_freeze,
             Increased_speed,
             _unused_score,
             edible_timer,
             time_left,
             direction,
             Stop_timer) = game_init(screen=screen, cofiguration=cofiguration)
            pacman.lives = remaining_lives
            continue
        if current_level > 10:
            current_level = 0
            return "win", score
        for ghost in ghosts:
            ghost.draw(screen, size, origin)

        draw_hud(
            screen, score, pacman.lives, current_level,
            maze_origin=origin,
            time_left=time_left,
            maze_pixel_w=level_maze.width * size)
        pygame.display.update()
