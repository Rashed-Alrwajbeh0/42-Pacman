from cell import Cell, Gum, Pac_Gum, Super_Pac_Gum
from mazegenerator import MazeGenerator
from random import randint, seed
from typing import Optional
from config import confing
import pygame


class Maze:
    """
    A class representing the game maze grid, managing walls,
    paths, items (gums/super gums), and rendering logic using Pygame.

    Attributes:
        width (int): The width of the maze in grid units.
        height (int): The height of the maze in grid units.
        entry (tuple[int, int]): The starting coordinate point of the maze.
        exit (tuple[int, int]): The ending coordinate point of the maze.
        shortest_path (list): The calculated shortest path through the maze.
        grid (list[list[Cell]]): A 2D grid matrix containing Cell instances.
    """
    def __init__(
            self, width: int, height: int,
            number_of_gums: int, seed: int = 0,
            perfect: bool = False) -> None:
        """Initializes the Maze generator, constructs the grid,
        and places items."""
        self.width = width
        self.height = height

        try:
            generator = MazeGenerator(
                size=(width, height), perfect=perfect, seed=seed
            )
        except Exception as exc:
            raise RuntimeError(f"Maze generation failed: {exc}") from exc

        raw = generator.maze
        self.entry: tuple[int, int] = generator.maze_entry
        self.exit: tuple[int, int] = generator.maze_exit
        self.shortest_path = generator.shortest_path

        self.grid: list[list[Cell]] = [
            [Cell(raw[y][x]) for x in range(width)]
            for y in range(height)
        ]
        self._place_content(number_of_gums)

    def _place_content(self, number_of_gums: int) -> None:
        """Randomly places regular and super Pac-Gums into valid grid cells."""
        seed(None)
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in corners:
            self.grid[y][x].content_id = Cell.SUPER_PACGUM

        if number_of_gums > 607:
            number_of_gums = 607
        placed = 0
        attempts = 0
        max_attempts = max(number_of_gums * 50, 200)
        while placed < number_of_gums and attempts < max_attempts:
            attempts += 1
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if (not self.grid[y][x].is_pattern and
                (x, y) not in corners and
                    not self.grid[y][x].content_id):
                self.grid[y][x].content_id = Cell.PACGUM
                placed += 1

    def center_cell(self) -> Cell:
        """
        Returns the center cell of the maze grid.

        Returns:
            Cell: The Cell object located at the center of the grid.
        """
        return self.grid[self.height // 2][self.width // 2]

    def remaining_pacgums(self) -> int:
        """
        Counts how many regular and super Pac-Gums are
        left uncollected in the maze.

        Returns:
            int: The total count of remaining gums.
        """
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.content_id in (Cell.PACGUM, Cell.SUPER_PACGUM):
                    count += 1
        return count

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """
        Return walkable neighbor cells (no wall blocking) from (x, y).

        Args:
            x (int): The x-coordinate of the current cell.
            y (int): The y-coordinate of the current cell.

        Returns:
            list[tuple[int, int]]: A list of coordinate tuples for accessible
            neighbor cells.
        """
        cell = self.grid[y][x]
        result: list[tuple[int, int]] = []
        if not cell.north and y > 0:
            result.append((x, y - 1))
        if not cell.south and y < self.height - 1:
            result.append((x, y + 1))
        if not cell.east and x < self.width - 1:
            result.append((x + 1, y))
        if not cell.west and x > 0:
            result.append((x - 1, y))
        return result

    def eat_at(self, x: int, y: int) -> Optional[Gum]:
        """
        Consume the content at (x, y) and return it (None if empty).

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            Optional[Gum]:-
                The consumed Gum object, or None if the cell was empty.
        """
        cell = self.grid[y][x]
        content = cell.content
        cell.content = None
        return content

    def cell_size_for(self, area_width: int, area_height: int) -> int:
        """
        Calculates the optimal cell size to fit the maze
        within a specified area.

        Args:
            area_width (int): The available pixel width.
            area_height (int): The available pixel height.

        Returns:
            int: The pixel size for each cell.
        """
        size = min(area_width // self.width, area_height // self.height)
        return max(size, 1)

    def get_pos(
            self,
            origin: tuple[int, int],
            cell_size: int) -> None:
        """
        Computes and updates the pixel bounding box coordinates
        for every cell in the maze.

        Args:
            origin (tuple[int, int]):-
                The (x, y) origin offset for the maze rendering.
            cell_size (int):-
                The pixel size of each individual cell.

        Returns:
            None
        """
        ox, oy = origin
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size
                cell.left = px
                cell.top = py
                cell.right = px + cell_size
                cell.bottom = py + cell_size

    def put_pacgums_in_cells(
            self,
            cell_size: int,
            origin: tuple[int, int],
            conf: confing) -> None:
        """
        Instantiates and assigns Pac_Gum and Super_Pac_Gum
        objects to their respective grid cells.

        Args:
            cell_size (int): The pixel size of each cell.
            origin (tuple[int, int]): The (x, y) starting coordinate offset.
            conf (confing): Configuration object providing item score points.

        Returns:
            None
        """
        ox, oy = origin
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size
                if cell.content_id == Cell.PACGUM:
                    cell.content = Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=(px + cell_size // 2, py + cell_size // 2),
                        points=conf.points_per_pacgum,
                        size=5
                    )
                elif cell.content_id == Cell.SUPER_PACGUM:
                    cell.content = Super_Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=(px + cell_size // 2, py + cell_size // 2),
                        points=conf.points_per_super_pacgum,
                        size=15
                    )

    def draw(self, screen: pygame.Surface, cell_size: int,
             origin: tuple[int, int] = (0, 0),
             wall_color: tuple[int, int, int] = (255, 255, 51),
             pattern_color: tuple[int, int, int] = (0,
                                                    209,
                                                    255)) -> list[list[Cell]]:
        """
        Renders the maze walls, background patterns,
        and active food items onto the screen.

        Args:
            screen (pygame.Surface): The target Pygame surface to draw onto.
            cell_size (int): The pixel size of each cell.
            origin (tuple[int, int]):
                The (x, y) rendering offset origin (default (0, 0)).
            wall_color (tuple[int, int, int]):
                The RGB color for maze walls (default yellow).
            pattern_color (tuple[int, int, int]):
                The RGB color for pattern blocks (default cyan).

        Returns:
            list[list[Cell]]: The 2D grid matrix of cells.
        """
        ox, oy = origin

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size
                cell.left = px
                cell.top = py
                cell.right = px + cell_size
                cell.bottom = py + cell_size

                if cell.is_pattern:
                    pygame.draw.rect(
                        screen, pattern_color,
                        pygame.Rect(px, py, cell_size, cell_size))

                if cell.north:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py), (px + cell_size, py), 2)
                if cell.south:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size), 2)
                if cell.west:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py), (px, py + cell_size), 2)
                if cell.east:
                    pygame.draw.line(
                        screen, wall_color,
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size), 2)

                if (cell.content_id == Cell.PACGUM and
                        cell.content is not None):
                    cell.content.draw(screen)
                elif (cell.content_id == Cell.SUPER_PACGUM and
                      cell.content is not None):
                    cell.content.draw(screen)
        return self.grid
