import pygame
from cell import Cell


def where_i_am(
        point: tuple[int, int],
        cell_size: int,
        grid_width: int,
        grid_hight: int,
        grid_list,
        direction: str
        ) -> Cell:

    Px, Py = point

    Px -= 450
    Py -= 50

    
    answer_x = Px // cell_size
    answer_y = Py // cell_size
    return grid_list[answer_y][answer_x]


class PacMan:
    def __init__(self, pos, screen, cell_size):
        self.pos = pos
        self.__idx = 0
        self.screen = screen
        self.__move = []
        for i in range(1, 50):
            image = pygame.image.load(
                f"Pictures/Pacman/move_png/{i}.png").convert()
            resized_image = pygame.transform.smoothscale(image, (75, 42))
            self.__move.append(resized_image)
        self.__radius = 0
        self.direction = "right"

    def __desplay(self, pos, rotation):
        if self.__idx == 49:
            self.__idx = 0
        image = self.__move[self.__idx]
        rotated_image = pygame.transform.rotate(
            image, rotation)
        self.__idx += 1
        rect = rotated_image.get_rect(center=pos)
        self.screen.blit(rotated_image, rect.topleft)

    def __set_radius(self, cell_size):
        self.__radius = 10

    def __go_right(self, destance):
        x, y = self.pos
        self.pos = (x + destance, y)

    def __go_left(self, destance):
        x, y = self.pos
        self.pos = (x - destance, y)

    def __go_top(self, destance):
        x, y = self.pos
        self.pos = (x, y - destance)

    def __go_bottom(self, destance):
        x, y = self.pos
        self.pos = (x, y + destance)

    def __wrong_direction(self, destance, current_cell):
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


    def is_pacmac_inside_cell(self, cell: Cell):
        x, y = self.pos
        return (cell.bottom >= y + self.__radius + 4 and
                cell.top <= y - self.__radius - 4 and
                cell.right >= x + self.__radius + 5 and
                cell.left <= x - self.__radius - 5)

    def put_pacman_in_cell(self, destance):
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
            size: int):
        
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
            size: int):
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
        self.__desplay(pos=self.pos, rotation=rotation_map.get(self.direction, 0))
            