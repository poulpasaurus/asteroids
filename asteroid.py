import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, kind: int) -> None:
        self.kind = kind
        radius = self.kind * ASTEROID_MIN_RADIUS
        super().__init__(x, y, radius)

    #override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, "grey", self.position, self.radius, LINE_WIDTH)

    #overide
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.off_screen_wrap(ASTEROID_MAX_RADIUS)

    def split(self) -> None:
        self.kill()
        if self.kind <= 1:
            # smallest asteroid, disapear without splitting
            return

        log_event("asteroid_split")
        ast1 = Asteroid(self.position.x, self.position.y, (self.kind - 1))
        ast2 = Asteroid(self.position.x, self.position.y, (self.kind - 1))
        
        angle = random.uniform(20, 50)
        ast1.velocity = self.velocity.rotate(angle) * 1.2
        ast2.velocity = self.velocity.rotate(-angle) * 1.2
