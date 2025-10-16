import pygame
import time
from game.game_engine import GameEngine

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sounds

# Screen setup
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load sounds
SOUND_PADDLE = pygame.mixer.Sound("paddle_hit.wav")
SOUND_WALL = pygame.mixer.Sound("wall_bounce.wav")
SOUND_SCORE = pygame.mixer.Sound("score.wav")


def replay_menu(screen, width, height, font):
    waiting = True
    choice = None

    while waiting:
        screen.fill(BLACK)
        options = [
            "Press 3: Best of 3",
            "Press 5: Best of 5",
            "Press 7: Best of 7",
            "Press ESC: Exit"
        ]

        for i, text in enumerate(options):
            rendered = font.render(text, True, WHITE)
            screen.blit(rendered, (width//2 - rendered.get_width()//2, height//3 + i*50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_3:
                    choice = 3
                    waiting = False
                elif event.key == pygame.K_5:
                    choice = 5
                    waiting = False
                elif event.key == pygame.K_7:
                    choice = 7
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
    return choice


def main():
    engine = GameEngine(WIDTH, HEIGHT, SOUND_PADDLE, SOUND_WALL, SOUND_SCORE)
    running = True
    game_over_text = None
    font_large = pygame.font.SysFont("Arial", 50)

    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over_text:
            engine.handle_input()
            engine.update()
            game_over_text = engine.check_game_over()

        engine.render(SCREEN)

        if game_over_text:
            text = font_large.render(game_over_text, True, WHITE)
            SCREEN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.delay(1500)

            # Show replay menu
            new_winning_score = replay_menu(SCREEN, WIDTH, HEIGHT, engine.font)
            engine.winning_score = new_winning_score
            engine.reset_game()
            game_over_text = None

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
