import random
import pygame

from particle import Particle
from constants import *

class ShotParticle(Particle):
    """particles used for the trail of a shot"""
    def __init__(self, x:float, y:float,):
        radius = random.randint(SHOT_PARTICLE_MIN_RADIUS, SHOT_PARTICLE_MAX_RADIUS)
        duration = random.uniform(SHOT_PARTICLE_MIN_DURATION, SHOT_PARTICLE_MAX_DURATION)
        rotation = random.randint(-60, 60)
        turn_speed = random.randint(SHOT_PARTICLE_MIN_TURN_SPEED, SHOT_PARTICLE_MAX_TURN_SPEED)
        color = random.choice(SHOT_COLORS)
        super().__init__(x, y, radius, duration, color, rotation, turn_speed)

    # override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, self.color, self.equ_triangle(), width=LINE_WIDTH)
