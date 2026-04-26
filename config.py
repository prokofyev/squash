import pygame

# Экран и производительность
FPS = 60
FULLSCREEN = True
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Цвета
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
P1_COLOR = (50, 120, 255)   # Синий
P2_COLOR = (255, 60, 60)    # Красный

# Ракетка
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 30
PADDLE_SPEED = 15
PADDLE_Y_OFFSET = 60

# Мяч
BALL_RADIUS = 16 
BALL_SPEED_X = 10
BALL_SPEED_Y = 10

# Правила
WIN_SCORE = 5

# Управление
P1_LEFT = pygame.K_LEFT
P1_RIGHT = pygame.K_RIGHT
P2_LEFT = pygame.K_a
P2_RIGHT = pygame.K_d
RESTART_KEY = pygame.K_SPACE
QUIT_KEY = pygame.K_ESCAPE
