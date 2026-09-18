from __future__ import annotations
from typing import Any, Optional
import pygame


class Cell:
    EMPTY = 0
    PACGUM = 1
    SUPER_PACGUM = 2

    def __init__(
            self,
            walls: int,
            content: Optional[Gum] = None,
            content_id: int = EMPTY) -> None:
        self.north: bool = bool(walls & 1)
        self.east: bool = bool(walls & 2)
        self.south: bool = bool(walls & 4)
        self.west: bool = bool(walls & 8)
        self.is_pattern: bool = (walls == 15)
        self.content_id: int = content_id
        self.content: Optional[Gum] = content
        self.left: Optional[int] = None
        self.right: Optional[int] = None
        self.top: Optional[int] = None
        self.bottom: Optional[int] = None


class Gum:
    def __init__(
            self,
            image: str,
            center_pos: tuple[int, int],
            points: int,
            size: int) -> None:
        self.image = image
        self.center_pos = center_pos
        self.points = points
        self.is_eaten = False
        self.show = True
        self.size = size
        self.gum = pygame.image.load(image).convert()
        self.resized_gum = pygame.transform.smoothscale(
            self.gum, (self.size, self.size)).convert()
        self.gum_rect = self.resized_gum.get_rect(center=self.center_pos)

    def draw(self, screen: pygame.Surface) -> Any:
        pass

    def collision(self, point: tuple[int, int]) -> bool:
        px, py = point
        gum_x_left = self.gum_rect.left
        gum_x_right = self.gum_rect.right
        gum_y_top = self.gum_rect.top
        gum_y_bottom = self.gum_rect.bottom
        return (px <= gum_x_right and
                px >= gum_x_left and
                py >= gum_y_top and
                py <= gum_y_bottom)


class Pac_Gum(Gum):
    def __init__(
            self,
            image: str,
            center_pos: tuple[int, int],
            points: int,
            size: int) -> None:
        super().__init__(
            image=image,
            center_pos=center_pos,
            points=points,
            size=size)

    def effect(self, resault: int) -> int:
        self.show = False
        return resault + self.points

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255, 255, 255),
                border_radius=100)


class Super_Pac_Gum(Gum):
    def __init__(
            self,
            image: str,
            center_pos: tuple[int, int],
            points: int,
            size: int) -> None:
        super().__init__(
            image=image,
            center_pos=center_pos,
            points=points,
            size=size)

    def effect(self, resault: int) -> int:
        self.show = False
        return resault + self.points

    def draw(self, screen: pygame.Surface) -> None:
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255, 255, 255),
                border_radius=100)


def where_i_am(
        point: tuple[int, int],
        cell_size: int,
        grid_width: int,
        grid_hight: int,
        grid_list: list[list[Cell]],
        direction: str
        ) -> Cell:

    Px, Py = point

    Px -= 450
    Py -= 50
    answer_x = Px // cell_size
    answer_y = Py // cell_size
    return grid_list[answer_y][answer_x]


class PacMan:
    def __init__(
            self,
            pos: tuple[int, int],
            screen: pygame.Surface,
            cell_size: int,
            lives: int) -> None:
        self.pos = pos
        self.__idx = 0
        self.lives = lives
        self.__center_pos = pos
        self.screen = screen
        self.__move: list[pygame.Surface] = []
        for i in range(1, 50):
            image = pygame.image.load(
                f"Pictures/Pacman/move_png/{i}.png").convert()
            resized_image = pygame.transform.smoothscale(image, (75, 42))
            self.__move.append(resized_image)
        self.__radius = 0
        self.direction = "right"

    def __desplay(self, pos: tuple[int, int], rotation: int) -> None:
        if self.__idx == 49:
            self.__idx = 0
        image = self.__move[self.__idx]
        rotated_image = pygame.transform.rotate(
            image, rotation)
        self.__idx += 1
        rect = rotated_image.get_rect(center=pos)
        self.screen.blit(rotated_image, rect.topleft)

    def __set_radius(self, cell_size: int) -> None:
        self.__radius = 10

    def __go_right(self, destance: int) -> None:
        x, y = self.pos
        self.pos = (x + destance, y)

    def __go_left(self, destance: int) -> None:
        x, y = self.pos
        self.pos = (x - destance, y)

    def __go_top(self, destance: int) -> None:
        x, y = self.pos
        self.pos = (x, y - destance)

    def __go_bottom(self, destance: int) -> None:
        x, y = self.pos
        self.pos = (x, y + destance)

    def __wrong_direction(self, destance: int, current_cell: Cell) -> None:
        if self.direction == "right":
            if not current_cell.east:
                self.__go_right(destance=destance)
                self.direction = "right"
        elif self.direction == "left":
            if not current_cell.west:
                self.__go_left(destance=destance)
                self.direction = "left"
        elif self.direction == "top":
            if not current_cell.north:
                self.__go_top(destance=destance)
                self.direction = "top"
        elif self.direction == "bottom":
            if not current_cell.south:
                self.__go_bottom(destance=destance)
                self.direction = "bottom"

    def is_pacmac_inside_cell(self, cell: Cell) -> bool:
        x, y = self.pos
        if (cell.bottom is None or cell.top is None or
                cell.right is None or cell.left is None):
            return False
        if (cell.bottom >= y + self.__radius + 4 and
                cell.top <= y - self.__radius - 4 and
                cell.right >= x + self.__radius + 5 and
                cell.left <= x - self.__radius - 5):
            return True
        return False

    def put_pacman_in_cell(self, destance: int) -> None:
        if self.direction == "right":
            self.__go_right(destance=destance)
            self.direction = "right"
        if self.direction == "left":
            self.__go_left(destance=destance)
            self.direction = "left"
        if self.direction == "top":
            self.__go_top(destance=destance)
            self.direction = "top"
        if self.direction == "bottom":
            self.__go_bottom(destance=destance)
            self.direction = "bottom"

    def __move_(
            self,
            grid_list: list[list[Cell]],
            direction: str,
            destance: int,
            grid_hight: int,
            grid_width: int,
            size: int) -> None:

        self.__set_radius(size)
        current_cell = where_i_am(
            point=self.pos,
            cell_size=size,
            grid_width=grid_width,
            grid_hight=grid_hight,
            grid_list=grid_list,
            direction=direction)
        if not self.is_pacmac_inside_cell(cell=current_cell):
            self.put_pacman_in_cell(destance=destance)
            return
        if direction == "right":
            if not current_cell.east:
                self.__go_right(destance=destance)
                self.direction = "right"

            else:
                self.__wrong_direction(
                    destance=destance,
                    current_cell=current_cell)
        elif direction == "left":
            if not current_cell.west:
                self.__go_left(destance=destance)
                self.direction = "left"
            else:
                self.__wrong_direction(
                    destance=destance,
                    current_cell=current_cell)
        elif direction == "top":
            if not current_cell.north:
                self.__go_top(destance=destance)
                self.direction = "top"
            else:
                self.__wrong_direction(
                    destance=destance,
                    current_cell=current_cell)
        elif direction == "bottom":
            if not current_cell.south:
                self.__go_bottom(destance=destance)
                self.direction = "bottom"
            else:
                self.__wrong_direction(
                    destance=destance,
                    current_cell=current_cell)

    def move(
            self,
            grid_list: list[list[Cell]],
            direction: str,
            destance: int,
            grid_hight: int,
            grid_width: int,
            size: int) -> None:
        while destance > 0:
            self.__move_(
                grid_list=grid_list,
                direction=direction,
                destance=1,
                grid_hight=grid_hight,
                grid_width=grid_width,
                size=size)
            destance -= 1
        rotation_map = {
            "right": 0,
            "left": 180,
            "top": 90,
            "bottom": 270
        }
        self.__desplay(
            pos=self.pos, rotation=rotation_map.get(self.direction, 0))

    def reset_atfer_eaten(self, cheat: int = 0) -> None:
        if not cheat:
            self.lives -= 1
            if self.lives == 0:
                raise ValueError("Finish Lives")
            self.pos = self.__center_pos
