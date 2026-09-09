from random import randint
from typing import Optional

import pygame
from mazegenerator import MazeGenerator

from cell import Cell, Gum, Pac_Gum, Super_Pac_Gum


class Maze:
    """A Pac-Man compatible maze built from an external generator.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        grid: 2D grid of Cell objects, indexed as grid[y][x] (row, col).
    """

    def __init__(
            self, width: int, height: int,
            number_of_gums: int, seed: int = 0,
            perfect: bool = False) -> None:
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
        """Place the 4 super-pacgums in the corners and scatter pacgums.

        Args:
            number_of_gums: Number of regular pacgums to place, in
                addition to the four fixed super-pacgums.
        """
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in corners:
            self.grid[y][x].content_id = Cell.SUPER_PACGUM

        placed = 0
        attempts = 0
        max_attempts = max(number_of_gums * 50, 200)

        while placed < number_of_gums and attempts < max_attempts:
            attempts += 1
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)
            if (x, y) in corners:
                continue
            cell = self.grid[y][x]
            if cell.is_pattern or cell.content_id != Cell.EMPTY:
                continue
            cell.content_id = Cell.PACGUM
            placed += 1

    def center_cell(self) -> Cell:
        """Return the cell at the logical center of the maze."""
        return self.grid[self.height // 2][self.width // 2]

    def remaining_pacgums(self) -> int:
        """Count how many pacgums/super-pacgums are still uneaten."""
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.content_id in (Cell.PACGUM, Cell.SUPER_PACGUM):
                    count += 1
        return count

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return walkable neighbor cells (no wall blocking) from (x, y)."""
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
        """Consume the content at (x, y) and return it (None if empty)."""
        cell = self.grid[y][x]
        content = cell.content
        cell.content = None
        return content

    def cell_size_for(self, area_width: int, area_height: int) -> int:
        """Return the largest square cell size that fits this maze in
        the given pixel area."""
        size = min(area_width // self.width, area_height // self.height)
        return max(size, 1)

    def get_pos(
            self,
            origin: tuple[int, int],
            cell_size: int) -> None:
        """Compute and store each cell's pixel bounding box."""
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
            origin: tuple[int, int]) -> None:
        """Instantiate Gum sprite objects for every gum cell."""
        ox, oy = origin
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size
                center = (px + cell_size // 2, py + cell_size // 2)
                if cell.content_id == Cell.PACGUM:
                    cell.content = Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=center,
                        points=50,
                        size=max(cell_size // 6, 3),
                    )
                elif cell.content_id == Cell.SUPER_PACGUM:
                    cell.content = Super_Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=center,
                        points=50,
                        size=max(cell_size // 2, 6),
                    )

    def draw(self, screen: pygame.Surface, cell_size: int,
             origin: tuple[int, int] = (0, 0),
             wall_color: tuple[int, int, int] = (0, 209, 255),
             wall_thickness: int = 3) -> list[list[Cell]]:
        """Draw walls and gums, refreshing each cell's pixel bounds.

        Args:
            screen: Surface to draw on.
            cell_size: Size in pixels of one maze cell.
            origin: (x, y) pixel offset of the maze's top-left corner.
            wall_color: RGB color used for the maze walls. Defaults to an
                electric cyan (change this, or pass your own, to reskin
                the maze).
            wall_thickness: Line thickness in pixels for the walls.
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

                if cell.north:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py), (px + cell_size, py), wall_thickness)
                if cell.south:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py + cell_size),
                        (px + cell_size, py + cell_size), wall_thickness)
                if cell.west:
                    pygame.draw.line(
                        screen, wall_color,
                        (px, py), (px, py + cell_size), wall_thickness)
                if cell.east:
                    pygame.draw.line(
                        screen, wall_color,
                        (px + cell_size, py),
                        (px + cell_size, py + cell_size), wall_thickness)

                if cell.content is not None and cell.content_id in (
                        Cell.PACGUM, Cell.SUPER_PACGUM):
                    cell.content.draw(screen)
        return self.grid