import pygame
from .paddle import Paddle
from .ball import Ball
import time

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height, paddle_sound=None, wall_sound=None, score_sound=None):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.paddle_sound = paddle_sound
        self.wall_sound = wall_sound
        self.score_sound = score_sound

        # Player paddle
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        # AI paddle (set is_ai=True)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height, is_ai=True)

        self.ball = Ball(width // 2, height // 2, 7, 7, width, height, paddle_sound, wall_sound)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)

        self.winning_score = 5

    # rest of update, handle_input, render, check_game_over remains unchanged

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)


    def update(self):
        # Move ball
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Score logic
        if self.ball.x <= 0:
            self.ai_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            if self.score_sound:
                self.score_sound.play()
            self.ball.reset()

        # AI tracking (now beatable)
        self.ai.auto_track(self.ball, self.height)


    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        self.check_game_over(screen)

    # check_game_over remains the same
    def check_game_over(self, screen):
        winner_text = ""
        if self.player_score >= self.winning_score:
            winner_text = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            winner_text = "AI Wins!"

        if winner_text:
            # Fill screen black
            screen.fill((0, 0, 0))
            # Show winner
            text_surface = self.game_over_font.render(winner_text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
            screen.blit(text_surface, text_rect)

            # Show replay options
            option_font = pygame.font.SysFont("Arial", 35)
            options_text = [
                "Press 3 for Best of 3",
                "Press 5 for Best of 5",
                "Press 7 for Best of 7",
                "Press ESC to Exit"
            ]
            for i, text in enumerate(options_text):
                option_surface = option_font.render(text, True, WHITE)
                option_rect = option_surface.get_rect(center=(self.width // 2, self.height // 2 + 40 + i*40))
                screen.blit(option_surface, option_rect)

            pygame.display.flip()

            # Wait for user input
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_3:
                            self.winning_score = 2  # Best of 3 → first to 2
                            waiting = False
                        elif event.key == pygame.K_5:
                            self.winning_score = 5
                            waiting = False
                        elif event.key == pygame.K_7:
                            self.winning_score = 4  # Best of 7 → first to 4
                            waiting = False
                        elif event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()

            # Reset game state for replay
            self.player_score = 0
            self.ai_score = 0
            self.ball.reset()
            self.player.y = self.height // 2 - self.paddle_height // 2
            self.ai.y = self.height // 2 - self.paddle_height // 2
