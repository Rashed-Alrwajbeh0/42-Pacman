"""In-game HUD: two glowing side panels (Score/Lives, Level/Time)
flanking the maze."""

import pygame

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
    """
    Draws a filled rounded rectangle panel on the
    screen with an optional border.

    Args:
        screen (pygame.Surface):
            The target Pygame surface to draw onto.
        rect (pygame.Rect):
            The rectangular dimensions and position of the panel.
        color (tuple[int, int, int]):
            The RGB fill color of the panel.
        border_color (tuple[int, int, int] | None):
            The RGB color for the border, or None if no border is needed.
        radius (int):
            The corner radius for the rounding effect (default 18).

    Returns:
        None
    """
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
        maze_pixel_w: int
) -> None:
    """
    Draws the Heads-Up Display (HUD) elements (Score,
    Lives, Level, and Time Remaining) around the game maze on the screen.

    Args:
        screen (pygame.Surface):
            The target Pygame surface to render the HUD onto.
        score (int):
            The current player score.
        lives (int):
            The remaining lives of the player.
        level (int):
            The current active game level.
        time_left (float):
            The remaining time left for the current level.
        maze_origin (tuple[int, int]):
            The (x, y) starting coordinates of the maze.
        maze_pixel_w (int):
            The total pixel width of the maze.

    Returns:
        None
    """
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
        _rounded_panel(
            screen, rect, _HUD_BG_LIGHT, border_color=_HUD_ACCENT, radius=12)
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
    draw_box(
        right_x, start_y + box_h + gap, "Time", str(max(int(time_left), 0)))
