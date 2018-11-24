import pygame
from pygame.rect import Rect

class Cube:
    def __init__(self, i, j, size, color = (0, 0, 0), state = 1):
        self.rect = Rect(i*size, j*size, size, size)
        self.X = i
        self.Y = j
        self.color = color
        self.chosen_color = None
        self.state = state
        self.update_chosen_color()

    def update_chosen_color(self):
        result = []
        for c in self.color:
            if c <= 205:
                result.append(c + 50)
            else:
                result.append(c)
        self.chosen_color = tuple(result)

    def draw(self, surface):
        if self.state == 1:
            pygame.draw.rect(surface, self.color, self.rect)
        elif self.state == 2:
            pygame.draw.rect(surface, self.chosen_color, self.rect, 5)
        elif self.state == 0:
            pygame.draw.rect(surface, (255, 255, 255), self.rect)