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

    


class Gum(ABC):
    def __init__(self, image, center_pos, points):
        self.image = image
        self.center_pos = center_pos
        self.points = points
        self.is_eaten = False

    def effect(self, resault):
        pass

    def draw(self):
        pass

class Pac_Gum(Gum):
    def __init__(self, image, center_pos, points):
        super().__init__(image, center_pos, points)
        self.gum = pygame.image.load(image).convert()
        self.resized_gum = pygame.transform.scale(self.gum, (5, 5)).convert()
        self.gum_rect = self.resized_gum.get_rect(center=self.center_pos)

    def effect(self, resault):
        return resault + self.points

    def draw(self, screen):
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255,255,255),
                border_radius=100)


class Super_Pac_Gum(Gum):
    def __init__(self, image, center_pos, points):
        super().__init__(image, center_pos, points)
        self.gum = pygame.image.load(image).convert()
        self.resized_gum = pygame.transform.smoothscale(self.gum, (15, 15)).convert()
        self.gum_rect = self.resized_gum.get_rect(center=self.center_pos)

    def effect(self, resault):
        return resault + self.points

    def draw(self, screen):
        if not self.is_eaten:
            pygame.draw.rect(
                surface=screen,
                rect=self.gum_rect,
                color=(255,255,255),
                border_radius=100)
