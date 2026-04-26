import pygame
import config

class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, config.PADDLE_WIDTH, config.PADDLE_HEIGHT)
        self.color = color
        self.speed = config.PADDLE_SPEED

    def move(self, keys, left_key, right_key):
        if keys[left_key]:
            self.rect.x -= self.speed
        if keys[right_key]:
            self.rect.x += self.speed
        self._clamp()

    def _clamp(self):
        self.rect.x = max(0, min(self.rect.x, config.SCREEN_WIDTH - self.rect.width))

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
