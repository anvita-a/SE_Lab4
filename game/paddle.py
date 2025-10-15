import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height, is_ai=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_ai = is_ai

        # Slightly increase AI speed to make it competitive
        self.speed = 8 if not is_ai else 8.5

        # AI tuning parameters
        self.reaction_timer = 0
        self.reaction_interval = random.randint(1, 3)   # reacts much faster now
        self.error_margin = random.randint(5, 15)       # tighter tracking

    def move(self, dy, screen_height):
        """Move the paddle while keeping it within bounds"""
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        """Return the paddle rectangle for drawing and collision"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        """AI follows the ball with near-perfect but human-like precision"""
        if not self.is_ai:
            return

        # Quick reaction cycle — almost every frame
        if self.reaction_timer > 0:
            self.reaction_timer -= 1
            return
        else:
            self.reaction_timer = random.randint(1, 3)

        paddle_center = self.y + self.height / 2
        ball_center = ball.y + ball.height / 2

        # Move toward ball center, slightly overshoot sometimes
        if abs(ball_center - paddle_center) > self.error_margin:
            if ball_center < paddle_center:
                self.move(-self.speed, screen_height)
            elif ball_center > paddle_center:
                self.move(self.speed, screen_height)

        # Add tiny random offset (makes AI human)
        if random.random() < 0.05:
            self.y += random.choice([-2, -1, 0, 1, 2])

        # Clamp within screen bounds
        self.y = max(0, min(self.y, screen_height - self.height))
