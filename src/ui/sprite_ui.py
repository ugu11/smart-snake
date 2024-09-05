import pygame

class SpriteUI:
    def __init__(self, x, y, width, height, icon):
        self.width = width
        self.height = height
        self.icon = icon
        self.ball = pygame.image.load(self.icon)
        self.ball = pygame.transform.scale(self.ball, (self.width, self.height))
        self.ballrect = self.ball.get_rect(topleft=(x, y))

    def draw(self, new_x, new_y, screen):
        self.ballrect.update(new_x * self.width, new_y * self.height, self.width, self.height)
        screen.blit(self.ball, self.ballrect)


    