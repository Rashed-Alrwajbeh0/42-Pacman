from enum import Enum, auto
from typing import Callable, Optional

import pygame

import ghost as ghost_logic
from maze import Maze

Position = tuple[int, int]

_EDIBLE_COLOR = (33, 33, 222)
_EDIBLE_FLASH_COLOR = (255, 255, 255)
_EYE_COLOR = (255, 255, 255)
_PUPIL_COLOR = (30, 30, 180)


class Ghoststate(Enum):
    """Possible behavioral states of a ghost."""
    Chasing = auto()
    Edible = auto()
    Eaten = auto()


class Ghost:
    """Represents a single ghost entity with position, state and behavior.

    A Ghost couples pure pathfinding logic (from ghost.py) with rendering
    state needed by pygame. Each ghost can have a different `behavior`
    function, allowing distinct AI personalities without duplicating code.

    Movement is pixel-based: the ghost tracks its current grid cell
    (`grid_pos`), a target grid cell (`target_pos`) and its actual pixel
    position (`pixel_pos`). Each update it moves `speed * dt` pixels
    toward the center of the target cell (so movement speed is
    independent of the frame rate); once it arrives, a new target is
    chosen via `behavior`. This mirrors how the player (PacMan) moves,
    so ghosts glide smoothly instead of teleporting cell-to-cell.

    Attributes:
        grid_pos: Current (x, y) grid position of the ghost (logical cell).
        target_pos: The next grid cell the ghost is walking toward.
        pixel_pos: Current pixel position on screen, or None until first
            computed from `grid_pos`.
        speed: Movement speed in pixels per second.
        corner: The ghost's home corner, used as its respawn point.
        color: RGB tuple used when drawing the ghost's body.
        behavior: Callable(maze, ghost_pos, player_pos) -> next_position,
            defining this ghost's chase/flee strategy.
        state: Current Ghoststate (Chasing, Edible, or Eaten).
        respawn_timer: Seconds remaining before an eaten ghost respawns.
        facing: Last (dx, dy) grid direction moved in, each in
            {-1, 0, 1}. Used to orient the eyes.
    """
    respawn_delay: float = 5.0

    def __init__(
            self,
            position: Position,
            corner: Position,
            color: str | tuple[int, int, int],
            behavior: Callable[[Maze, Position, Position], Position],
            speed: float = 140.0,
            ) -> None:
        """Initialize a ghost at its starting corner.

        Args:
            position: Initial (x, y) grid position.
            corner: Home corner position used for respawning.
            color: RGB color tuple for rendering.
            behavior: Movement strategy function for this ghost.
            speed: Movement speed in pixels per second.
        """
        self.grid_pos = position
        self.target_pos = position
        self.pixel_pos: Optional[tuple[float, float]] = None
        self.speed = speed
        self.corner = corner
        self.color = color
        self.behavior = behavior
        self.state = Ghoststate.Chasing
        self.respawn_timer = 0.0
        self.facing: tuple[int, int] = (0, -1)

    def become_eddible(self) -> None:
        """Switch the ghost to edible state (player ate a super-pacgum)."""
        if self.state != Ghoststate.Eaten:
            self.state = Ghoststate.Edible

    def get_eaten(self) -> None:
        """Switch the ghost to eaten state and start its respawn timer."""
        self.state = Ghoststate.Eaten
        self.respawn_timer = self.respawn_delay

    @staticmethod
    def _cell_center(
            cell: Position,
            cell_size: int,
            origin: Position,
    ) -> tuple[float, float]:
        """Compute the pixel coordinates of a grid cell's center."""
        ox, oy = origin
        x, y = cell
        return (
            ox + x * cell_size + cell_size / 2,
            oy + y * cell_size + cell_size / 2,
        )

    def _pick_next_target(self, maze: Maze, player_pos: Position) -> None:
        """Ask the behavior/flee logic for the next cell, and update
        the facing direction used to orient the eyes when drawing."""
        previous = self.grid_pos
        if self.state == Ghoststate.Edible:
            self.target_pos = ghost_logic.flee_towards_farthest_neighbor(
                maze, self.grid_pos, player_pos)
        else:
            self.target_pos = self.behavior(
                maze, self.grid_pos, player_pos)

        dx = self.target_pos[0] - previous[0]
        dy = self.target_pos[1] - previous[1]
        if dx or dy:
            self.facing = ((dx > 0) - (dx < 0), (dy > 0) - (dy < 0))

    def update(
            self,
            maze: Maze,
            player_pos: Position,
            dt: float,
            cell_size: int,
            origin: Position,
    ) -> None:
        """Update the ghost's position and state for one game tick.

        Args:
            maze: The maze the ghost is moving through.
            player_pos: Current (x, y) grid position of the player.
            dt: Time elapsed since the last update, in seconds.
            cell_size: Size in pixels of one maze cell.
            origin: (x, y) pixel offset of the maze's top-left corner.
        """
        if self.state == Ghoststate.Eaten:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.grid_pos = self.corner
                self.target_pos = self.corner
                self.pixel_pos = self._cell_center(
                    self.corner, cell_size, origin)
                self.state = Ghoststate.Chasing
            return

        if self.pixel_pos is None:
            self.pixel_pos = self._cell_center(
                self.grid_pos, cell_size, origin)
            self.target_pos = self.grid_pos

        target_x, target_y = self._cell_center(
            self.target_pos, cell_size, origin)
        pixel_x, pixel_y = self.pixel_pos
        delta_x, delta_y = target_x - pixel_x, target_y - pixel_y

        # Frame-rate independent step: pixels/second * seconds elapsed.
        step = self.speed * dt

        if abs(delta_x) <= step and abs(delta_y) <= step:
            self.pixel_pos = (target_x, target_y)
            self.grid_pos = self.target_pos
            self._pick_next_target(maze, player_pos)
        else:
            step_x = step if delta_x > 0 else (-step if delta_x < 0 else 0)
            step_y = step if delta_y > 0 else (-step if delta_y < 0 else 0)
            self.pixel_pos = (pixel_x + step_x, pixel_y + step_y)

    def _draw_eyes(
            self,
            screen: pygame.Surface,
            center: tuple[float, float],
            radius: float,
            pupils: bool = True,
    ) -> None:
        """Draw two eyes at `center`, pupils looking towards `facing`."""
        cx, cy = center
        eye_radius = max(radius * 0.32, 3.0)
        eye_dx = radius * 0.4
        eye_dy = -radius * 0.12
        left_eye = (cx - eye_dx, cy + eye_dy)
        right_eye = (cx + eye_dx, cy + eye_dy)

        for eye in (left_eye, right_eye):
            pygame.draw.circle(
                screen, _EYE_COLOR,
                (round(eye[0]), round(eye[1])), round(eye_radius))

        if not pupils:
            return

        pupil_radius = max(eye_radius * 0.5, 1.0)
        pupil_shift = eye_radius * 0.45
        dir_x, dir_y = self.facing
        for eye in (left_eye, right_eye):
            pupil = (
                eye[0] + dir_x * pupil_shift,
                eye[1] + dir_y * pupil_shift,
            )
            pygame.draw.circle(
                screen, _PUPIL_COLOR,
                (round(pupil[0]), round(pupil[1])), round(pupil_radius))

    def _draw_body(
            self,
            screen: pygame.Surface,
            center: tuple[float, float],
            radius: float,
            color: str | tuple[int, int, int],
    ) -> None:
        """Draw the classic dome-plus-wavy-skirt ghost silhouette."""
        cx, cy = center

        # Dome (the polygon skirt below overlaps its lower half).
        pygame.draw.circle(
            screen, color, (round(cx), round(cy)), round(radius))

        # Wavy skirt across the lower half of the body.
        bumps = 4
        step = (2 * radius) / bumps
        points: list[tuple[float, float]] = [(cx - radius, cy)]
        for i in range(bumps + 1):
            x = cx - radius + i * step
            y = cy + radius if i % 2 == 0 else cy + radius * 0.55
            points.append((x, y))
        points.append((cx + radius, cy))
        pygame.draw.polygon(
            screen, color,
            [(round(x), round(y)) for x, y in points])

    def draw(
            self,
            screen: pygame.Surface,
            cell_size: int,
            origin: Position,
    ) -> None:
        """Draw the ghost on screen at its current pixel position.

        Args:
            screen: The pygame surface to draw on.
            cell_size: Size in pixels of one maze cell.
            origin: (x, y) pixel offset of the maze's top-left corner.
        """
        if self.pixel_pos is None:
            self.pixel_pos = self._cell_center(
                self.grid_pos, cell_size, origin)

        radius = max(cell_size / 2 - 2, 4.0)

        if self.state == Ghoststate.Eaten:
            # Classic look: only the eyes travel back home.
            self._draw_eyes(
                screen, self.pixel_pos, radius, pupils=False)
            return

        if self.state == Ghoststate.Edible:
            body_color = _EDIBLE_COLOR
            self._draw_body(screen, self.pixel_pos, radius, body_color)
            self._draw_eyes(
                screen, self.pixel_pos, radius, pupils=False)
            return

        self._draw_body(screen, self.pixel_pos, radius, self.color)
        self._draw_eyes(screen, self.pixel_pos, radius, pupils=True)