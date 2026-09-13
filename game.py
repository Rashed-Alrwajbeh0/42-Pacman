import sys

import pygame

from cell import PacMan, Super_Pac_Gum
from conf import confing
from ghost import (
    chase_then_flee, next_step_towards, ghost_speed_for_level, random_walk, seek_pacgum_near_player,
)
from ghost_entity import Ghost, Ghoststate
from maze import Maze

current_level = 0
HUD_HEIGHT = 60
MARGIN = 20
EDIBLE_DURATION = 8.0
HUD_PANEL_WIDTH = 450
MAZE_ORIGIN = (HUD_PANEL_WIDTH, 50)

BACKGROUND_IMAGE = "Pictures/Backgrounds/7.png"
WALL_COLOR = (0, 209, 255)


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
        maze.put_pacgums_in_cells(cell_size=cell_size, origin=MAZE_ORIGIN, conf=configuration)
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
        maze_origin: tuple[int, int],
        maze_pixel_w: int,
        level_max_time: float = 90.0,
        panel_width: int = HUD_PANEL_WIDTH,
) -> None:
    ox, oy = maze_origin
    box_w = 180
    box_h = 70
    gap = 35
    gap_from_maze = 40
    vertical_offset = 60

    label_font = pygame.font.SysFont(None, 24)
    value_font = pygame.font.SysFont(None, 40, bold=True)

    def draw_box(x: int, y: int, label: str, value: str) -> None:
        rect = pygame.Rect(x, y, box_w, box_h)
        _rounded_panel(screen, rect, _HUD_BG_LIGHT, border_color=_HUD_ACCENT, radius=12)
        label_surf = label_font.render(label.upper(), True, _HUD_DIM)
        screen.blit(label_surf, (rect.left + 12, rect.top + 8))
        value_surf = value_font.render(value, True, _HUD_TEXT)
        screen.blit(value_surf, (rect.left + 12, rect.top + 30))

    start_y = oy + vertical_offset   

    left_x = ox - gap_from_maze - box_w
    draw_box(left_x, start_y, "Score", f"{score:,}")
    draw_box(left_x, start_y + box_h + gap, "Lives", str(lives))

    right_x = ox + maze_pixel_w + gap_from_maze
    draw_box(right_x, start_y, "Level", str(level))
    draw_box(right_x, start_y + box_h + gap, "Time", str(max(int(time_left), 0)))


def game_init(screen, cofiguration):
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
        Ghost(corners[0], corners[0], (255, 0, 0), chase_then_flee, speed=ghost_speed),
        Ghost(corners[1], corners[1], (255, 165, 0), next_step_towards, speed=ghost_speed),
        Ghost(corners[2], corners[2], (255, 105, 180), seek_pacgum_near_player, speed=ghost_speed),
        Ghost(corners[3], corners[3], (0, 200, 255), random_walk, speed=ghost_speed),
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
    """Run one full game session and return ("win"/"lose", final_score)."""
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
    while True:
        dt = fram_clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
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
                         Stop_timer) = game_init(screen=screen, cofiguration=cofiguration)
                        continue
                    if event.key == pygame.K_F3:
                        pacman.lives += 1
                    if event.key == pygame.K_F4:
                        Increased_speed = not Increased_speed
                    if event.key == pygame.K_F5:
                        Ghost_freeze = not Ghost_freeze
                    if event.key == pygame.K_F6:
                        Stop_timer = not Stop_timer

        draw_background(screen=screen, image_path=BACKGROUND_IMAGE, alpha=100)
        level_maze.draw(screen, size, origin)
        if current_level == 11:
            return

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
            if edible_timer <= 0 and ghost.state in (Ghoststate.Edible, Ghoststate.Waiting):
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
            ghosts, pacman, cofiguration.points_per_ghost, collision_radius, Invincibility)
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
            if not cheat and not Invincibility:
                for ghost in ghosts:
                    ghost.grid_pos = ghost.corner
                    ghost.target_pos = ghost.corner
                    ghost.pixel_pos = None
                    ghost.state = Ghoststate.Chasing


        if level_maze.remaining_pacgums() == 0:
            return "win", score

        for ghost in ghosts:
            ghost.draw(screen, size, origin)

        draw_hud(
            screen, score, pacman.lives, current_level,
            maze_origin=origin,
            time_left=time_left,
            maze_pixel_w=level_maze.width * size,
            level_max_time=float(cofiguration.level_max_time))
        pygame.display.update()