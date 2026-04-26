import pygame
import config
import random

class Ball:
    def __init__(self):
        self.radius = config.BALL_RADIUS
        self.color = config.WHITE
        self.rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        self.dx = 0
        self.dy = 0
        self.reset()

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def bounce_walls(self):
        if self.rect.left <= 0 or self.rect.right >= config.SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= config.PADDLE_HEIGHT:
            self.dy *= -1
            self.rect.top = config.PADDLE_HEIGHT  # Предотвращает "залипание" на потолке

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius)

    def reset(self):
        """Спавн в верхней части экрана с направлением вниз."""
        self.rect.centerx = config.SCREEN_WIDTH // 2
        self.rect.centery = 50
        self.dx = random.choice([-1, 1]) * config.BALL_SPEED_X
        self.dy = config.BALL_SPEED_Y  # Положительный = движение вниз
