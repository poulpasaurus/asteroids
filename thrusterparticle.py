import pygame
import random
import math

from particle import Particle
from constants import *

class ThrusterParticle(Particle):
    """particles used when the ship is moving"""

    def __init__(self, x: float, y: float, ship_rotation: float = 0) -> None:
        speed = random.randint(math.floor((PLAYER_SPEED / 2)), math.floor(PLAYER_SPEED * 3/2))
        unit_vector = pygame.Vector2(0, 1)
        flame_orientation = ship_rotation + 180 + random.randint(-30, 30)
        self.velocity: pygame.Vector2 = unit_vector.rotate(flame_orientation) * speed
        
        radius = random.randint(THRUSTER_PARTICLE_MIN_RADIUS, THRUSTER_PARTICLE_MAX_RADIUS)
        duration = random.uniform(THRUSTER_PARTICLE_MIN_DURATION, THRUSTER_PARTICLE_MAX_DURATION)
        rotation: int = random.randint(-60, 60)
        turn_speed = random.randint(THRUSTER_PARTICLE_MIN_TURN_SPEED, THRUSTER_PARTICLE_MAX_TURN_SPEED)
        color = random.choice(THRUSTER_PARTICLE_COLORS)
        super().__init__(x, y, radius, duration, color, rotation, turn_speed)

    # override
    def update(self, dt: float) -> None:
        super().update(dt)
        self.position += self.velocity * dt
        self.velocity -= self.velocity * THRUSTER_PARTICLE_SPEED_DECREASE_RATE * dt

    # override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, self.color, self.equ_triangle(), width=LINE_WIDTH)
