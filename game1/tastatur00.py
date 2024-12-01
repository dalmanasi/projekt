import os
import pygame
import random
import time

class Settings:
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 800
    FPS = 60
    FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    IMAGE_PATH = os.path.join(FILE_PATH, "images")

class Player:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.start_x = (Settings.WINDOW_WIDTH - self.width) // 2
        self.start_y = Settings.WINDOW_HEIGHT - self.height
        self.x = self.start_x
        self.y = self.start_y
        self.speed = 4

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

        self.x = max(0, min(Settings.WINDOW_WIDTH - self.width, self.x))
        self.y = max(0, min(Settings.WINDOW_HEIGHT - self.height, self.y))

    def reset_position(self):
        self.x = self.start_x
        self.y = self.start_y

class MovingObstacle:
    def __init__(self, image_path, x, y, speed_x, speed_y, size):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, size)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.x < -self.width:
            self.x = Settings.WINDOW_WIDTH
        elif self.x > Settings.WINDOW_WIDTH:
            self.x = -self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def check_collision(self, player):
        return self.x < player.x + player.width and self.x + self.width > player.x and self.y < player.y + player.height and self.y + self.height > player.y

def draw_dark_overlay(screen):
    overlay = pygame.Surface((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

def display_score(screen, score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def main():
    os.environ["SDL_VIDEO_WINDOW_POS"] = "10, 50"
    pygame.init()

    screen = pygame.display.set_mode((Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))
    pygame.display.set_caption("Spiel ohne Hindernisse")
    clock = pygame.time.Clock()

    obstacles = [
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), 250, 50, 1, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), -350, 50, 1, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), 550, 50, 1, 0, (60, 50)),    
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car2.png"), 600, 220, -2, 0, (90, 80)),  
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.png"), 200, 250, -2, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), 400, 480, 2, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.png"), 830, 125, -4, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.png"), 350, 112, -4, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.png"), 450, 170, -3, 0, (60, 50)),  
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.png"), 700, 670, -3, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car1.png"), 450, 670, -3, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car3.png"), 200, 550, -2, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car2.png"), 600, 530, -2, 0, (90, 80)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), -350, 600, 2, 0, (60, 50)),
        MovingObstacle(os.path.join(Settings.IMAGE_PATH, "car4.png"), 300, 600, 2, 0, (60, 50)),
    ]

    background_image = pygame.image.load(os.path.join(Settings.IMAGE_PATH, "background.png")).convert()
    background_image = pygame.transform.scale(background_image, (Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT))

    player = Player(os.path.join(Settings.IMAGE_PATH, "frogger.png"))

    paused = False
    running = True
    esc_last_pressed = 0
    score = 0
    level = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_ESCAPE:
                    now = time.time()
                    if now - esc_last_pressed < 0.5:
                        running = False
                    esc_last_pressed = now

        screen.blit(background_image, (0, 0))

        if not paused:
            keys = pygame.key.get_pressed()
            player.move(keys)
            player.draw(screen)

            if player.y <= 0:
                player.reset_position()
                score += 10
                print("Neue Runde!")
                player.speed += 1

                # Level erhöhen und Hindernisgeschwindigkeiten anpassen
                level += 1
                for obstacle in obstacles:
                    obstacle.speed_x *= 1.1

            for obstacle in obstacles:
                obstacle.move()
                obstacle.draw(screen)

                if obstacle.check_collision(player):
                    print("Kollision!")
                    player.reset_position()

            display_score(screen, score)

        else:
            draw_dark_overlay(screen)

        pygame.display.flip()
        clock.tick(Settings.FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
