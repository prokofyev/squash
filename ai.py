import config

class AIController:
    def __init__(self, paddle):
        self.paddle = paddle
        self.deadzone = 10        # Зона покоя, чтобы не дёргался
        self.speed_factor = 0.75  # Множитель скорости для баланса

    def update(self, ball):
        """Двигает ракетку ИИ, отслеживая мяч."""
        # Реагируем только когда мяч летит вниз
        if ball.dy < 0:
            return

        diff = ball.rect.centerx - self.paddle.rect.centerx
        if abs(diff) > self.deadzone:
            direction = 1 if diff > 0 else -1
            self.paddle.rect.x += direction * config.PADDLE_SPEED * self.speed_factor
        
        self.paddle._clamp()
