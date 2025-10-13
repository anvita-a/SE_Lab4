import pygame
import random

class Paddle:
    def __init__(self, x, y, width, height, is_ai=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 7
        self.is_ai = is_ai
        self.reaction_delay = random.randint(0, 5)  # frames to delay AI reaction

    def move(self, dy, screen_height):
        self.y += dy
        self.y = max(0, min(self.y, screen_height - self.height))

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def auto_track(self, ball, screen_height):
        if not self.is_ai:
            return

        # Random chance to delay reaction
        if random.randint(0, 5) < self.reaction_delay:
            return  # skip movement this frame

        # Calculate target center
        paddle_center = self.y + self.height / 2
        ball_center = ball.y + ball.height / 2

        # Move only part of the distance to be beatable
        if ball_center < paddle_center:
            self.move(-self.speed, screen_height)
        elif ball_center > paddle_center:
            self.move(self.speed, screen_height)

        # Add small random overshoot/undershoot
        self.y += random.choice([-1, 0, 1])
        # Clamp to screen
        self.y = max(0, min(self.y, screen_height - self.height))
