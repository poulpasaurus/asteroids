import pygame
import random
from logger import log_event
from circleshape import CircleShape
from asteroidparticle import AsteroidExplosionParticle
from constants import *


class Asteroid(CircleShape):
    def __init__(self, x: float, y: float, kind: int) -> None:
        self.kind = kind
        self.color = random.choice(ASTEROID_COLORS)
        # used to draw a jagged sphere
        self.random_length: list[float] = [
            random.uniform(ASTEROID_MIN_POINT_PERCENTAGE, ASTEROID_MAX_POINT_PERCENTAGE) for _ in range(ASTEROID_POINTS)
        ]
        radius = self.kind * ASTEROID_MIN_RADIUS
        super().__init__(x, y, radius)
        self.hitbox_radius = radius * ASTEROID_MIN_POINT_PERCENTAGE

    #override
    def draw(self, screen: pygame.Surface) -> None:
        line_width = LINE_WIDTH # only outline 
        # line_width = 0 # filled in asteroids, 0 is the default for polygon, we give it explicitly    
        pygame.draw.polygon(screen, self.color, self.rock(), width=line_width)

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, "red", self.position, self.hitbox_radius, LINE_WIDTH)

    #override
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.off_screen_wrap(ASTEROID_MAX_RADIUS)

    def split(self) -> None:
        self.kill()
        for _ in range(self.kind * random.randint(3,5)):
            AsteroidExplosionParticle(self.position.x, self.position.y)
        if self.kind <= 1:
            # smallest asteroid, disappear without splitting
            return

        log_event("asteroid_split")
        ast1 = Asteroid(self.position.x, self.position.y, (self.kind - 1))
        ast2 = Asteroid(self.position.x, self.position.y, (self.kind - 1))
        
        angle = random.uniform(20, 50)
        ast1.velocity = self.velocity.rotate(angle) * 1.2
        ast2.velocity = self.velocity.rotate(-angle) * 1.2

    def rock(self) -> list[pygame.Vector2]:
        """draw an irregular circle"""
        angle = 360 / ASTEROID_POINTS
        points = []
        for i in range(ASTEROID_POINTS):
            unit_vector = pygame.Vector2(0, 1)
            rotated_vector = unit_vector.rotate(i * angle)
            forward_vector = rotated_vector * self.radius * self.random_length[i]
            position = self.position + forward_vector
            points.append(position)
        return points
