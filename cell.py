from abc import ABC
import pygame


class Cell:
    EMPTY = 0
    PACGUM = 1
    SUPER_PACGUM = 2

    def __init__(self, walls: int, content: list[Gum] = [], content_id: int = EMPTY) -> None:
        self.north: bool = bool(walls & 1)
        self.east: bool = bool(walls & 2)
        self.south: bool = bool(walls & 4)
        self.west: bool = bool(walls & 8)
        self.is_pattern: bool = (walls == 15)
        self.content_id: int = content_id
        self.content: list[Gum] = content
        self.left: int | None = None
        self.right: int | None = None
        self.top: int | None = None
        self.bottom: int | None = None

    
class Gum(ABC):
    def __init__(self, image, center_pos, points, size):
        self.image = image
        self.center_pos = center_pos
        self.points = points
        self.is_eaten = False
        self.size = size
        self.gum = pygame.image.load(image).convert()
        self.resized_gum = pygame.transform.smoothscale(
            self.gum, (self.size, self.size)).convert()
        self.gum_rect = self.resized_gum.get_rect(center=self.center_pos)

    def effect(self, resault):
        pass

    def draw(self):
        pass

    def collision(self, point):
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
    def __init__(self, image, center_pos, points, size):
        super().__init__(
            image=image,
            center_pos=center_pos,
            points=points,
            size=size)

    def effect(self, resault):
        return resault + self.points

    def draw(self, screen):
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255, 255, 255),
                border_radius=100)


class Super_Pac_Gum(Gum):
    def __init__(self, image, center_pos, points, size):
        super().__init__(
            image=image,
            center_pos=center_pos,
            points=points,
            size=size)

    def effect(self, resault):
        return resault + self.points

    def draw(self, screen):
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255, 255, 255),
                border_radius=100)
