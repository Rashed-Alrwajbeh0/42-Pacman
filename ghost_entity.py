from enum import Enum, auto
from typing import Callable
import pygame
import ghost as ghost_logic
from maze import Maze

position = tuple[int, int]


class Ghoststate(Enum):
    """Possible behavioral states of a ghost"""
    Chasing = auto()
    Edible = auto()
    Eaten = auto()


class Ghost:
    """Represents a single ghost entity with position, state and behavior.

    A Ghost couples pure pathfinding logic (from ghost.py) with rendering
    state needed by pygame. Each ghost can have a different `behavior`
    function, allowing distinct AI personalities without duplicating code.

    Attributes:
        position: Current (x, y) grid position of the ghost.
        corner: The ghost's home corner, used as its respawn point.
        color: RGB tuple used when drawing the ghost.
        behavior: Callable(maze, ghost_pos, player_pos) -> next_position,
            defining this ghost's chase/flee strategy.
        state: Current GhostState (CHASING, EDIBLE, or EATEN).
        respawn_timer: Seconds remaining before an eaten ghost respawns.
    """
    respawn_delay: float = 5.0

    def __init__(
              self,
              position: position,
              corner: position,
              color: tuple[int, int, int],
              behavior: Callable[[Maze, position, position], position],
              ) -> None:
               """Initialize a ghost at its starting corner.
               Args:
               position: Initial (x, y) grid position.
               coner: Home corner position used for respawning.
               color: RGB color tuple for rendering.
               behavior: Movement strategy function for this ghost.
               """
               self.position = position
               self.conner = corner
               self.color = color
               self.behavior = behavior
               self.state = Ghoststate.Chasing
               self.respawn_timer = 0.0
               self.move_interval: float = 0.3
               self.move_timer: float = 0.0

    def become_eddible(self) -> None:
        """Switch the ghost to edible state (player ate a super-pacgum)"""
        if self.state != Ghoststate.Eaten:
             self.state = Ghoststate.Edible

    def get_eaten(self) -> None:
        """Switch the ghost to eaten state and start its respawn timer"""
        self.state = Ghoststate.Eaten
        self.respawn_timer = self.respawn_delay

    def update(
              self,
              maze: Maze,
              player_pos: position,
              dt: float,
    ) -> None:
         """Update the ghost's position and state for one game tick"""
         if self.state == Ghoststate.Eaten:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.position = self.corner
                self.state = Ghoststate.Chasing
            return
         
         self.move_timer += dt
         if self.move_timer < self.move_interval:
              return
         self.move_timer = 0.0
               
         if self.state == Ghoststate.Chasing:
            self.position = self.behavior(maze, self.position, player_pos)
         elif self.state == Ghoststate.Edible:
                    self.position = ghost_logic.flee_towards_farthest_neighbor(
                        maze, self.position, player_pos)
                         

    def draw(
              self,
              screen: pygame.Surface,
              cell_size: int,
              origin: position,
        ) -> None :
         """Draw the ghost on screen at its current position.
        Args:
            screen: The pygame surface to draw on.
            cell_size: Size in pixels of one maze cell.
            origin: (x, y) pixel offset of the maze's top-left corner.
        """
         ox, oy = origin
         x, y =self.position
         center = (
              ox + x * cell_size + cell_size //2,
              oy + y * cell_size + cell_size //2,
         )
         color = (100, 100, 255)if self.state == Ghoststate.Edible else self.color
         pygame.draw.circle(screen, color, center, max(cell_size // 2 -2, 1))
         