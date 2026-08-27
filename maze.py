import pygame
from mazegenerator import MazeGenerator
from cell import Cell, Pac_Gum, Super_Pac_Gum
from random import randint


class Maze:
    def __init__(self, width: int, height: int,
                 number_of_gums: int, seed: int = 0, perfect: bool = False) -> None:
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

    def _place_content(self, number_of_gums) -> None:
        corners = [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1),
        ]
        for x, y in corners:
            self.grid[y][x].content_id = Cell.SUPER_PACGUM
        px = [i for i in range(self.height)]
        py = [i for i in range(self.width)]

        x_choise = [0, self.width - 1]
        y_choise = [0, self.height -1]
        number_of_gums += 1
        while(number_of_gums):
            x = randint(1, self.width - 1)
            y = randint(1, self.height - 1)
            while(self.grid[x][y].is_pattern or
                  x in x_choise or
                  y in y_choise):
                x = randint(1, self.width - 1)
                y = randint(1, self.height - 1)
            self.grid[x][y].content_id = Cell.PACGUM
            number_of_gums-=1
 
    def center_cell(self) -> tuple[int, int]:
        return self.width // 2, self.height // 2

    def remaining_pacgums(self) -> int:
        count = 0
        for row in self.grid:
            for cell in row:
                if cell.content_id in (Cell.PACGUM, Cell.SUPER_PACGUM):
                    count += 1
        return count

    def cell_size_for(self, area_width: int, area_height: int) -> int:
        size = min(area_width // self.width, area_height // self.height)
        return max(size, 1)

    def draw(self, screen: pygame.Surface, cell_size: int,
             origin: tuple[int, int] = (0, 0)) -> None:
        ox, oy = origin
        wall_color = (33, 33, 222)
        pacgum_color = (255, 255, 255)

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                px, py = ox + x * cell_size, oy + y * cell_size

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

                center = (px + cell_size // 2, py + cell_size // 2)
                if cell.content_id == Cell.PACGUM:
                    
                    cell.content = Pac_Gum(image="Pictures/gums/gum.png",center_pos=(px+cell_size//2, py+cell_size//2), points=50)
                    # pygame.draw.circle(screen, pacgum_color, center, 2)
                    cell.content.draw(screen)
                elif cell.content_id == Cell.SUPER_PACGUM:
                    cell.content = Super_Pac_Gum(image="Pictures/gums/gum.png",center_pos=(px+cell_size//2, py+cell_size//2), points=50)
                    # pygame.draw.circle(screen, pacgum_color, center, 6)
                    cell.content.draw(screen)
        return self.grid
