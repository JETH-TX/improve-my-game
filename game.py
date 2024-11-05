import pygame
import random
import sys
from config import HEIGHT, FPS, WHITE, WIDTH, BLACK
from player import Player
from obstacle import Obstacle

pygame.font.init()
font = pygame.font.SysFont(None, 48)

class Game:
    def _init(self):  # Corregido de _init a _init_
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Speedrunner")

        self.clock = pygame.time.Clock()
        self.player = Player(100, HEIGHT - 50)
        self.obstacles = []
        self.background_image = pygame.image.load("assets/background.png").convert()
        self.background_scroll = 0
        self.background_speed = 2
        self.lives = 3
        self.health = 100
        self.max_health = 100
        self.collision_damage = 20
        self.score = 0

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.update()
            self.draw()

            pygame.display.flip()

        pygame.quit()

    def update(self):
        self.player.update()

        self.background_scroll -= self.background_speed
        if self.background_scroll <= -self.background_image.get_width():
            self.background_scroll = 0

        if random.randint(0, 100) < 1:
            obstacle_x = WIDTH
            obstacle_y = HEIGHT - 50
            self.obstacles.append(Obstacle(obstacle_x, obstacle_y))

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if obstacle.rect.x + obstacle.rect.width > 0
        ]

        player_rect = self.player.get_rect()
        for obstacle in self.obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.health -= self.collision_damage  # Reducir salud
                self.obstacles.remove(obstacle)  # Elimina obstáculo después de colisión
            if self.health <= 0:
                self.lives -= 1  # Reduce una vida
                self.health = self.max_health  # Restablece la salud

                if self.lives <= 0:
                    self.draw_text("¡Perdiste!", font, BLACK, self.screen, WIDTH // 2, HEIGHT // 2)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    pygame.quit()
                    sys.exit()

            elif obstacle.rect.x == 0:
                self.score += 1  # Incrementar el puntaje cuando el obstáculo ha pasado

    def draw(self):
        self.screen.blit(self.background_image, (self.background_scroll, 0))
        self.screen.blit(
            self.background_image,
            (self.background_scroll + self.background_image.get_width(), 0),
        )

        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        # Mostrar texto de Vidas, Salud y Puntaje
        self.draw_text(f"Vidas: {self.lives}", font, BLACK, self.screen, 100, 30)
        self.draw_text(f"Puntaje: {self.score}", font, BLACK, self.screen, 350, 30)
        self.draw_text(f"Salud: {self.health}/{self.max_health}", font, BLACK, self.screen, 125, 60)

        # Barra de salud
        pygame.draw.rect(self.screen, BLACK, (125, 75, 200, 20))  # Fondo de la barra de salud
        pygame.draw.rect(self.screen, (255, 0, 0), (125, 75, (200 * self.health) // self.max_health, 20))  # Barra de salud

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, True, color)
        textrect = textobj.get_rect()
        textrect.center = (x, y)
        surface.blit(textobj, textrect)