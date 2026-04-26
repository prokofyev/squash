# game.py
import pygame
import config
from paddle import Paddle
from ball import Ball
from ai import AIController

class SquashGame:
    def __init__(self):
        pygame.init()
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
        self.sub_font = pygame.font.SysFont("arial", 28)

        self.state = 'MENU'  # MENU, PLAYING, PAUSED, GAMEOVER
        self.mode = '2P'     # '1P' или '2P'
        self._setup_game()

    def _setup_game(self):
        paddle_y = config.SCREEN_HEIGHT - config.PADDLE_Y_OFFSET
        self.p1 = Paddle(config.SCREEN_WIDTH // 4, paddle_y, config.P1_COLOR)
        self.p2 = Paddle(config.SCREEN_WIDTH * 3 // 4, paddle_y, config.P2_COLOR)
        self.ball = Ball()
        self.ai = AIController(self.p2)
        self.score1 = 0
        self.score2 = 0
        self.next_hit = 1
        self.game_over = False
        self.winner_text = ""
        self.winner_color = config.WHITE

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.state = 'QUIT'
                return

            if event.type == pygame.KEYDOWN:
                if self.state == 'MENU':
                    if event.key == pygame.K_1:
                        self.mode = '1P'
                        self.state = 'PLAYING'
                    elif event.key == pygame.K_2:
                        self.mode = '2P'
                        self.state = 'PLAYING'
                    elif event.key == config.QUIT_KEY:  # <-- Выход по ESC из меню
                        self.state = 'QUIT'
                elif self.state == 'PLAYING':
                    if event.key == config.QUIT_KEY:
                        self.state = 'PAUSED'
                elif self.state == 'PAUSED':
                    if event.key == config.QUIT_KEY:
                        self.state = 'PLAYING'
                    elif event.key == config.RESTART_KEY:
                        self.state = 'MENU'
                elif self.state == 'GAMEOVER':
                    if event.key == config.RESTART_KEY:
                        self.state = 'MENU'

        keys = pygame.key.get_pressed()
        if self.state == 'PLAYING':
            self.p1.move(keys, config.P1_LEFT, config.P1_RIGHT)
            if self.mode == '2P':
                self.p2.move(keys, config.P2_LEFT, config.P2_RIGHT)

    def _update(self):
        if self.state != 'PLAYING':
            return

        if self.mode == '1P':
            self.ai.update(self.ball)

        self.ball.move()
        self.ball.bounce_walls()
        self._check_paddle_collision()
        self._check_scoring()

    def _check_paddle_collision(self):
        if self.ball.dy < 0:
            return
        for paddle, player_id in [(self.p1, 1), (self.p2, 2)]:
            if self.ball.rect.colliderect(paddle.rect):
                if self.next_hit == player_id:
                    self.ball.dy *= -1
                    self._apply_spin(paddle)
                    self.next_hit = 3 - player_id
                    self.ball.rect.bottom = paddle.rect.top
                    break

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
            self.state = 'GAMEOVER'
        elif self.score2 >= config.WIN_SCORE:
            self.game_over = True
            self.winner_text = "Красный победил!"
            self.winner_color = config.P2_COLOR
            self.state = 'GAMEOVER'

    def _draw(self):
        self.screen.fill(config.BLACK)

        if self.state in ('PLAYING', 'PAUSED', 'GAMEOVER'):
            # Активная ракетка рисуется сверху, чтобы не мешать прицеливанию
            if self.next_hit == 1:
                self.p2.draw(self.screen)
                self.p1.draw(self.screen)
            else:
                self.p1.draw(self.screen)
                self.p2.draw(self.screen)

            self.ball.draw(self.screen)
            self._draw_ui()

        if self.state == 'MENU':
            self._draw_menu()
        elif self.state in ('PAUSED', 'GAMEOVER'):
            self._draw_overlay()

        pygame.display.flip()

    def _draw_ui(self):
        score_surf = self.font.render(f"{self.score1} : {self.score2}", True, config.WHITE)
        self.screen.blit(score_surf, (config.SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 30))

        indicator_color = config.P1_COLOR if self.next_hit == 1 else config.P2_COLOR
        pygame.draw.rect(self.screen, indicator_color, (0, 0, config.SCREEN_WIDTH, config.PADDLE_HEIGHT))

    def _draw_menu(self):
        title = self.font.render("SQUASH", True, config.WHITE)
        self.screen.blit(title, (config.SCREEN_WIDTH//2 - title.get_width()//2, 150))

        opt1 = self.sub_font.render("[1] Один игрок (против компьютера)", True, config.GRAY)
        opt2 = self.sub_font.render("[2] Два игрока", True, config.GRAY)
        opt_esc = self.sub_font.render("[ESC] Выйти из игры", True, config.GRAY)

        self.screen.blit(opt1, (config.SCREEN_WIDTH//2 - opt1.get_width()//2, 260))
        self.screen.blit(opt2, (config.SCREEN_WIDTH//2 - opt2.get_width()//2, 310))
        self.screen.blit(opt_esc, (config.SCREEN_WIDTH//2 - opt_esc.get_width()//2, 370))

    def _draw_overlay(self):
        surf = pygame.Surface((config.SCREEN_WIDTH, config.SCREEN_HEIGHT), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 140))
        self.screen.blit(surf, (0, 0))

        if self.state == 'GAMEOVER':
            win_surf = self.font.render(self.winner_text, True, self.winner_color)
            self.screen.blit(win_surf, (config.SCREEN_WIDTH//2 - win_surf.get_width()//2, config.SCREEN_HEIGHT//2 - 60))

            txt = self.sub_font.render("ПРОБЕЛ - в главное меню", True, config.GRAY)
            self.screen.blit(txt, (config.SCREEN_WIDTH//2 - txt.get_width()//2, config.SCREEN_HEIGHT//2 + 10))
        else:
            txt = self.font.render("ПАУЗА", True, config.WHITE)
            self.screen.blit(txt, (config.SCREEN_WIDTH//2 - txt.get_width()//2, config.SCREEN_HEIGHT//2 - 40))

            r1 = self.sub_font.render("ESC - продолжить", True, config.GRAY)
            r2 = self.sub_font.render("ПРОБЕЛ - в главное меню", True, config.GRAY)
            self.screen.blit(r1, (config.SCREEN_WIDTH//2 - r1.get_width()//2, config.SCREEN_HEIGHT//2 + 20))
            self.screen.blit(r2, (config.SCREEN_WIDTH//2 - r2.get_width()//2, config.SCREEN_HEIGHT//2 + 60))

    def run(self):
        while self.state != 'QUIT':
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(config.FPS)
        pygame.quit()
