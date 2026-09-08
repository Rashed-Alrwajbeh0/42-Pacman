from typing import Optional

import pygame
from mazegenerator import MazeGenerator
from cell import Cell, Gum, Pac_Gum, Super_Pac_Gum
from random import randint


class Maze:
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

        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in corners:
            self.grid[x][y].content_id = Cell.SUPER_PACGUM
        x_choise = [0, self.width - 1]
        y_choise = [0, self.height - 1]
        # number_of_gums += 1
        while (number_of_gums > 4):
            x = randint(0, self.width - 1)
            y = randint(0, self.height - 1)

            while (self.grid[x][y].is_pattern):
                if (x == self.width - 1):
                    break
                elif (y == self.height - 1):
                    break
                elif (x == 0 and y not in y_choise):
                    break
                elif (y == 0 and x not in x_choise):
                    break
                if (x in x_choise or y in y_choise):
                    x = randint(0, self.width - 1)
                    y = randint(0, self.height - 1)
                else:
                    if (not self.grid[x][y].is_pattern):
                        break
                    else:
                        x = randint(0, self.width - 1)
                        y = randint(0, self.height - 1)
            if ((x, y) not in corners):
                self.grid[x][y].content_id = Cell.PACGUM
                number_of_gums -= 1

    def center_cell(self) -> Cell:
        return self.grid[self.width // 2][self.height // 2]

    def remaining_pacgums(self) -> int:
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.content_id in (Cell.PACGUM, Cell.SUPER_PACGUM):
                    count += 1
        return count

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return walkable neighbor cells (no wall blocking) from (x, y)"""
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
        """Consume the content at (x, y) and return it (0 if empty)"""
        cell = self.grid[y][x]
        content = cell.content
        cell.content = None
        return content

    def cell_size_for(self, area_width: int, area_height: int) -> int:
        size = min(area_width // self.width, area_height // self.height)
        return max(size, 1)

    def get_pos(
            self,
            origin: tuple[int, int],
            cell_size: int) -> None:
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
        ox, oy = origin
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size
                if cell.content_id == Cell.PACGUM:
                    cell.content = Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=(px + cell_size // 2, py + cell_size // 2),
                        points=50,
                        size=5
                    )
                elif cell.content_id == Cell.SUPER_PACGUM:
                    cell.content = Super_Pac_Gum(
                        image="Pictures/gums/gum.png",
                        center_pos=(px + cell_size // 2, py + cell_size // 2),
                        points=50,
                        size=15
                    )

    def draw(self, screen: pygame.Surface, cell_size: int,
             origin: tuple[int, int] = (0, 0)) -> list[list[Cell]]:
        ox, oy = origin
        wall_color = (255, 255, 51)

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

                if cell.content_id == Cell.PACGUM and cell.content is not None:
                    cell.content.draw(screen)
                elif (cell.content_id == Cell.SUPER_PACGUM
                        and cell.content is not None):
                    cell.content.draw(screen)
        return self.grid
