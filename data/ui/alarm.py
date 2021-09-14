import pygame
import math
from data.ui.base import Base

class Alarm(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hand_position = pygame.Vector2(self.position.x, self.position.y - self.size.y)
        self.start_drag = False
        self.text = "0.00 minutes left"
        self.font = pygame.font.SysFont("Calibri", 34)
        self.rendered_text = self.font.render(self.text, True, pygame.Color("Red"))
        self.timer = 0
        self.minutes = 3600

    @property
    def collide(self):
        mouse_pos = pygame.mouse.get_pos()
        distance = math.hypot(mouse_pos[0] - self.position.x, mouse_pos[1] - self.position.y)
        if distance <= self.size.x + 50:
            return True
        return False

    @property
    def left_click(self):
        return pygame.mouse.get_pressed()[0] and self.collide

    def update(self, delta_time):
        if self.start_drag:
            mouse_pos = pygame.mouse.get_pos()
            radians = math.atan2(mouse_pos[1] - self.position.y, mouse_pos[0] - self.position.x) + (1/2*math.pi)
            radians = radians if radians > 0 else radians + 2*math.pi
            self.timer = radians / (2*math.pi) * self.minutes
            direction = pygame.Vector2(mouse_pos[0] - self.position.x, mouse_pos[1] - self.position.y).normalize()  # TODO normalize crashes at 0
            self.hand_position = pygame.Vector2(direction.x * self.size[1] + self.position.x, direction.y * self.size[1] + self.position.y)

        if self.timer > 0:
            self.timer = max(0.0, self.timer - delta_time)
            self.rendered_text = self.font.render(f"{self.timer/60:.2f} minutes left", True, pygame.Color("Red"))
            radians = self.timer / self.minutes * (2*math.pi)
            x = math.cos(radians - 1/2*math.pi) * self.size[1] + self.position.x
            y = math.sin(radians - 1/2*math.pi) * self.size[1] + self.position.y
            self.hand_position = pygame.Vector2(x, y)

    def handle_events(self, event):
        if event.type in [pygame.MOUSEBUTTONDOWN]:
            if self.left_click:
                self.start_drag = True
        elif event.type in [pygame.MOUSEBUTTONUP]:
            self.start_drag = False

    def draw(self, surface):
        pygame.draw.circle(surface, pygame.Color("lightblue").lerp((0,0,0), 0.2), self.position, self.size[1])
        pygame.draw.circle(surface, pygame.Color("lightblue").lerp((100,100,100), 0.2), self.position, self.size[1] - 10)
        pygame.draw.circle(surface, pygame.Color("lightblue").lerp((255,255,255), 0.3), self.position, self.size[1] - 20)
        pygame.draw.circle(surface, pygame.Color("red").lerp((100, 200, 100), .3), self.hand_position, 30)
        pygame.draw.circle(surface, pygame.Color("lightblue").lerp((0,0,0, 0), 0.2), self.rect.center, self.size[1] - 60)
        pygame.draw.circle(surface, pygame.Color("lightblue").lerp((255, 255, 255), 0.75), (self.position.x - 60, self.position.y - 130), 15)
        surface.blit(self.rendered_text, (self.position.x - self.rendered_text.get_width()/2, self.position.y - self.rendered_text.get_height()/2))





