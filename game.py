import pygame
import config
from paddle import Paddle
from ball import Ball

class SquashGame:
    def __init__(self):
        pygame.init()
        
        # Настройка экрана: полный или оконный режим
        flags = pygame.FULLSCREEN if config.FULLSCREEN else 0
        if config.FULLSCREEN:
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode((info.current_w, info.current_h), flags)
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT = info.current_w, info.current_h
        else:
            self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            config.SCREEN_WIDTH = config.WINDOW_WIDTH
            config.SCREEN_HEIGHT = config.WINDOW_HEIGHT

        pygame.display.set_caption("Squash")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 44, bold=True)
        self._setup()

    def _setup(self):
        paddle_y = config.SCREEN_HEIGHT - config.PADDLE_Y_OFFSET
        self.p1 = Paddle(config.SCREEN_WIDTH // 4, paddle_y, config.P1_COLOR)
        self.p2 = Paddle(config.SCREEN_WIDTH * 3 // 4, paddle_y, config.P2_COLOR)
        self.ball = Ball()
        self.score1 = 0
        self.score2 = 0
        self.next_hit = 1
        self.is_running = True
        self.game_over = False
        self.winner_text = ""
        self.winner_color = config.WHITE

    def _handle_events(self):
        keys = pygame.key.get_pressed()
        self.p1.move(keys, config.P1_LEFT, config.P1_RIGHT)
        self.p2.move(keys, config.P2_LEFT, config.P2_RIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN and event.key == config.RESTART_KEY and self.game_over:
                self._setup()
            if event.type == pygame.KEYDOWN and event.key == config.QUIT_KEY:
                self.is_running = False

    def _update(self):
        if self.game_over:
            return

        self.ball.move()
        self.ball.bounce_walls()
        self._check_paddle_collision()
        self._check_scoring()

    def _check_paddle_collision(self):
        # Если мяч летит вверх, ракетки не обрабатываются
        if self.ball.dy < 0:
            return

        for paddle, player_id in [(self.p1, 1), (self.p2, 2)]:
            if self.ball.rect.colliderect(paddle.rect):
                if self.next_hit == player_id:
                    self.ball.dy *= -1
                    self._apply_spin(paddle)
                    self.next_hit = 3 - player_id  # Передаём очередь
                    self.ball.rect.bottom = paddle.rect.top  # Корректировка позиции
                    break  # Один контакт за кадр

    def _apply_spin(self, paddle):
        hit_pos = (self.ball.rect.centerx - paddle.rect.centerx) / (paddle.rect.width / 2)
        self.ball.dx = hit_pos * config.BALL_SPEED_X

    def _check_scoring(self):
        if self.ball.rect.top > config.SCREEN_HEIGHT:
            if self.next_hit == 1:
                self.score2 += 1
                self.next_hit = 2
            else:
                self.score1 += 1
                self.next_hit = 1

            self._check_win()
            if not self.game_over:
                self.ball.reset()

    def _check_win(self):
        if self.score1 >= config.WIN_SCORE:
            self.game_over = True
            self.winner_text = "Синий победил!"
            self.winner_color = config.P1_COLOR
        elif self.score2 >= config.WIN_SCORE:
            self.game_over = True
            self.winner_text = "Красный победил!"
            self.winner_color = config.P2_COLOR

    def _draw(self):
        self.screen.fill(config.BLACK)
        if self.next_hit == 2:
            self.p1.draw(self.screen)
            self.p2.draw(self.screen)
        else:
            self.p2.draw(self.screen)
            self.p1.draw(self.screen)
        self.ball.draw(self.screen)
        self._draw_ui()
        pygame.display.flip()

    def _draw_ui(self):
        # Счёт по центру
        score_surf = self.font.render(f"{self.score1} : {self.score2}", True, config.WHITE)
        self.screen.blit(score_surf, (config.SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 30))

        # ЦВЕТНОЙ ИНДИКАТОР ХОДА (вместо текста)
        indicator_color = config.P1_COLOR if self.next_hit == 1 else config.P2_COLOR
        pygame.draw.rect(self.screen, indicator_color, (0, 0, config.SCREEN_WIDTH, config.PADDLE_HEIGHT))

        if self.game_over:
            win_surf = self.font.render(self.winner_text, True, self.winner_color)
            self.screen.blit(win_surf, (config.SCREEN_WIDTH // 2 - win_surf.get_width() // 2, config.SCREEN_HEIGHT // 2 - 30))
            
            restart_font = pygame.font.SysFont("arial", 26)
            restart_surf = restart_font.render("Нажмите пробел для новой игры или ESC для выхода", True, config.GRAY)
            self.screen.blit(restart_surf, (config.SCREEN_WIDTH // 2 - restart_surf.get_width() // 2, config.SCREEN_HEIGHT // 2 + 20))

    def run(self):
        while self.is_running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(config.FPS)
        pygame.quit()
