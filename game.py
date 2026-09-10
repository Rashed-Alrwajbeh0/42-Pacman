import sys

import pygame

from cell import PacMan, Super_Pac_Gum
from conf import confing
from ghost import (
    chase_then_flee, next_step_towards, random_walk, seek_pacgum_near_player,
)
from ghost_entity import Ghost, Ghoststate
from maze import Maze

current_level = 0
HUD_HEIGHT = 60
MARGIN = 20
EDIBLE_DURATION = 8.0
HUD_PANEL_WIDTH = 450
MAZE_ORIGIN = (HUD_PANEL_WIDTH, 50)

BACKGROUND_IMAGE = "Pictures/Backgrounds/pacman_maze_background_v2 (1).png"
WALL_COLOR = (0, 209, 255)


def check_ghost_collisions(
        ghosts: list[Ghost],
        pacman: PacMan,
        points_per_ghost: int,
        collision_radius: float,
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
        if ghost.state == Ghoststate.Eaten:
            continue
        if ghost.pixel_pos is None:
            continue
        gx, gy = ghost.pixel_pos
        distance_sq = (px - gx) ** 2 + (py - gy) ** 2
        if distance_sq <= collision_radius ** 2:
            if ghost.state == Ghoststate.Edible:
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
        maze.put_pacgums_in_cells(cell_size=cell_size, origin=MAZE_ORIGIN)
        current_level += 1
        return maze, cell_size
    except RuntimeError as exc:
        print(f"Warning: {exc}")
        sys.exit(1)


_BACKGROUND_CACHE: dict[tuple[str, tuple[int, int]], pygame.Surface] = {}


def draw_background(
        screen: pygame.Surface,
        image_path: str,
        alpha: int = 50,
        base_color: tuple[int, int, int] = (8, 10, 28)) -> None:
    """Fill the screen with a base color, then blend a background image
    on top of it (cached so it isn't rescaled every single frame).

    ``base_color`` is the deep navy tone showing through the transparent
    image and also used as a safe fallback if the image can't be loaded,
    so a missing/corrupt asset never crashes the game.
    """
    screen.fill(base_color)

    window_size = screen.get_size()
    cache_key = (image_path, window_size)
    resized_image = _BACKGROUND_CACHE.get(cache_key)
    if resized_image is None:
        try:
            image = pygame.image.load(image_path).convert()
            resized_image = pygame.transform.smoothscale(
                image, window_size).convert_alpha()
            _BACKGROUND_CACHE[cache_key] = resized_image
        except (pygame.error, FileNotFoundError) as exc:
            print(f"Warning: could not load background '{image_path}': "
                  f"{exc}")
            return

    resized_image.set_alpha(alpha)
    screen.blit(resized_image, (0, 0))


def where_i_am(
        point: tuple[int, int],
        cell_size: int,
        origin: tuple[int, int],
        maze: Maze,
) -> tuple[int, int]:
    ox, oy = origin
    px, py = point
    grid_x = max(0, min(maze.width - 1, (px - ox) // cell_size))
    grid_y = max(0, min(maze.height - 1, (py - oy) // cell_size))
    return grid_x, grid_y

_HUD_ACCENT = (255, 213, 0)
_HUD_BG = (18, 18, 40)
_HUD_BG_LIGHT = (32, 32, 64)
_HUD_TEXT = (235, 235, 245)
_HUD_DIM = (150, 150, 170)


def _rounded_panel(
        screen: pygame.Surface,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        border_color: tuple[int, int, int] | None = None,
        radius: int = 18) -> None:
    pygame.draw.rect(screen, color, rect, border_radius=radius)
    if border_color is not None:
        pygame.draw.rect(
            screen, border_color, rect, width=2, border_radius=radius)


def draw_hud(
        screen: pygame.Surface,
        score: int,
        lives: int,
        level: int,
        time_left: float,
        level_max_time: float = 90.0,
        panel_width: int = HUD_PANEL_WIDTH,
) -> None:
    """Draw a large, card-styled HUD panel in the empty space to the
    left of the maze (the maze is always drawn starting at x=HUD_PANEL_WIDTH).

    Shows the score, lives (as small Pac-Man icons), current level and
    a time-remaining progress bar, plus a short controls reminder.
    """
    window_height = screen.get_height()
    pad = MARGIN
    panel_rect = pygame.Rect(
        pad, pad, panel_width - 2 * pad, window_height - 2 * pad)
    _rounded_panel(screen, panel_rect, _HUD_BG, border_color=_HUD_ACCENT)

    inner_x = panel_rect.left + 24
    inner_width = panel_rect.width - 48
    y = panel_rect.top + 24

    title_font = pygame.font.SysFont(None, 56, bold=True)
    label_font = pygame.font.SysFont(None, 26)
    value_font = pygame.font.SysFont(None, 46, bold=True)
    small_font = pygame.font.SysFont(None, 22)

    title = title_font.render("PAC-MAN", True, _HUD_ACCENT)
    screen.blit(title, (inner_x, y))
    y += title.get_height() + 28

    def draw_stat(label: str, value: str, box_height: int = 78) -> int:
        nonlocal y
        box_rect = pygame.Rect(inner_x, y, inner_width, box_height)
        _rounded_panel(screen, box_rect, _HUD_BG_LIGHT, radius=14)
        label_surf = label_font.render(label.upper(), True, _HUD_DIM)
        screen.blit(label_surf, (box_rect.left + 16, box_rect.top + 10))
        value_surf = value_font.render(value, True, _HUD_TEXT)
        screen.blit(value_surf, (box_rect.left + 16, box_rect.top + 34))
        y += box_height + 16
        return box_rect.bottom

    draw_stat("Score", f"{score:,}")
    lives_bottom = draw_stat("Lives", "")
    lives_row_y = lives_bottom - 78 + 44
    for i in range(max(lives, 0)):
        cx = inner_x + 30 + i * 34
        pygame.draw.circle(screen, _HUD_ACCENT, (cx, lives_row_y), 12)
        pygame.draw.polygon(
            screen, _HUD_BG_LIGHT,
            [(cx, lives_row_y),
             (cx + 14, lives_row_y - 7),
             (cx + 14, lives_row_y + 7)])

    draw_stat("Level", str(level))

    time_box = pygame.Rect(inner_x, y, inner_width, 78)
    _rounded_panel(screen, time_box, _HUD_BG_LIGHT, radius=14)
    label_surf = label_font.render("TIME LEFT", True, _HUD_DIM)
    screen.blit(label_surf, (time_box.left + 16, time_box.top + 10))
    ratio = 0.0
    if level_max_time > 0:
        ratio = max(0.0, min(1.0, time_left / level_max_time))
    bar_bg = pygame.Rect(
        time_box.left + 16, time_box.top + 46, inner_width - 32, 16)
    pygame.draw.rect(screen, (50, 50, 70), bar_bg, border_radius=8)
    if ratio > 0:
        bar_fill = pygame.Rect(
            bar_bg.left, bar_bg.top, int(bar_bg.width * ratio), bar_bg.height)
        bar_color = (
            int(220 - 120 * ratio), int(70 + 150 * ratio), 70)
        pygame.draw.rect(screen, bar_color, bar_fill, border_radius=8)
    time_text = small_font.render(
        f"{max(int(time_left), 0)}s", True, _HUD_TEXT)
    screen.blit(time_text, (bar_bg.right - time_text.get_width(),
                            time_box.top + 10))
    y = time_box.bottom + 16

    controls_y = panel_rect.bottom - 90
    controls_label = label_font.render("CONTROLS", True, _HUD_DIM)
    screen.blit(controls_label, (inner_x, controls_y))
    controls_text = small_font.render(
        "Arrows / WASD to move", True, _HUD_TEXT)
    screen.blit(controls_text, (inner_x, controls_y + 26))


def game_play(
        screen: pygame.Surface,
        cofiguration: confing,
        direction_key: dict[str, pygame.Event]) -> tuple[str, int]:
    """Run one full game session and return ("win"/"lose", final_score)."""
    origin = MAZE_ORIGIN
    window_width, window_height = screen.get_size()
    level_maze, size = make_level(
        configuration=cofiguration,
        window_width=window_width,
        window_height=window_height,
    )
    fram_clock = pygame.time.Clock()
    width = cofiguration.levels["width"]
    hight = cofiguration.levels["height"]
    score = 0
    edible_timer = 0.0
    lives = cofiguration.lives
    time_left = float(cofiguration.level_max_time)

    level_maze.get_pos(origin, size)
    center_cell = level_maze.center_cell()
    direction = "right"
    if (center_cell.left is None or center_cell.right is None or
            center_cell.top is None or center_cell.bottom is None):
        raise RuntimeError("center cell position was not computed")
    x = (center_cell.left + center_cell.right) // 2
    y = (center_cell.top + center_cell.bottom) // 2
    pacman = PacMan(pos=(x, y), screen=screen, cell_size=size, lives=3)

    corners = [
        (0, 0),
        (level_maze.width - 1, 0),
        (0, level_maze.height - 1),
        (level_maze.width - 1, level_maze.height - 1),
    ]
    ghosts = [
        Ghost(corners[0], corners[0], (255, 0, 0), chase_then_flee),
        Ghost(corners[1], corners[1], (255, 165, 0), next_step_towards),
        Ghost(corners[2], corners[2], (255, 105, 180), seek_pacgum_near_player),
        Ghost(corners[3], corners[3], (0, 200, 255), random_walk),
    ]
    collision_radius = max(size / 2, 12.0)

    while True:
        dt = fram_clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        draw_background(screen=screen, image_path=BACKGROUND_IMAGE)
        level_maze.draw(screen, size, origin)

        keyboard = pygame.key.get_pressed()
        if keyboard[direction_key["top"]]:
            direction = "top"
        elif keyboard[direction_key["down"]]:
            direction = "bottom"
        elif keyboard[direction_key["right"]]:
            direction = "right"
        elif keyboard[direction_key["left"]]:
            direction = "left"
        pacman.move(
            grid_hight=hight,
            grid_width=width,
            grid_list=level_maze.grid,
            direction=direction,
            destance=2,
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
            if edible_timer <= 0:
                for ghost in ghosts:
                    if ghost.state == Ghoststate.Edible:
                        ghost.state = Ghoststate.Chasing

        player_cell = where_i_am(
            point=pacman.pos, cell_size=size, origin=origin, maze=level_maze)
        for ghost in ghosts:
            ghost.update(level_maze, player_cell, dt, size, origin)

        life_lost, points_gained = check_ghost_collisions(
            ghosts, pacman, cofiguration.points_per_ghost, collision_radius)
        score += points_gained

        time_left -= dt
        if time_left <= 0 or life_lost:
            if life_lost:
                lives -= 1
            pacman.pos = (x, y)
            time_left = float(cofiguration.level_max_time)
            for ghost in ghosts:
                ghost.grid_pos = ghost.corner
                ghost.target_pos = ghost.corner
                ghost.pixel_pos = None
                ghost.state = Ghoststate.Chasing
            if lives <= 0:
                return "lose", score

        if level_maze.remaining_pacgums() == 0:
            return "win", score

        for ghost in ghosts:
            ghost.draw(screen, size, origin)

        draw_hud(
            screen, score, lives, current_level, time_left,
            level_max_time=float(cofiguration.level_max_time))

        pygame.display.update()