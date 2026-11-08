import pygame
import random
import math

from particle import Particle
from constants import *

class AsteroidExplosionParticle(Particle):
    """particles used when an asteroid is destroyed"""

    def __init__(self, x: float, y: float) -> None:
        speed = random.randint(math.floor((PLAYER_SPEED / 2)), math.floor(PLAYER_SPEED * 3/2))
        unit_vector = pygame.Vector2(0, 1)
        rotation = random.randint(0, 360)
        self.velocity: pygame.Vector2 = unit_vector.rotate(rotation) * speed
        
        radius = random.randint(ASTEROID_PARTICLE_MIN_RADIUS, ASTEROID_PARTICLE_MAX_RADIUS)
        duration = random.uniform(THRUSTER_PARTICLE_MIN_DURATION, THRUSTER_PARTICLE_MAX_DURATION)
        more_colors = []
        more_colors.extend(ASTEROID_COLORS)
        more_colors.extend(THRUSTER_PARTICLE_COLORS)
        color = random.choice(more_colors)
        super().__init__(x, y, radius, duration, color)

    # override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, self.color, self.rock(), width=LINE_WIDTH)

    # override
    def update(self, dt:float) -> None:
        super().update(dt)
        self.position += self.velocity * dt
