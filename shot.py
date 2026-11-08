import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH, SHOW_HITBOXES

class Shot(CircleShape):
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)

    #override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "blue", self.position, self.radius, LINE_WIDTH)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, "red", self.position, self.hitbox_radius, LINE_WIDTH)

    #override
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        # shot exiting the screen get deleted
        self.off_screen_kill()
