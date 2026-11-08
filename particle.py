import pygame
import random
from constants import *

class Particle(pygame.sprite.Sprite):
    """Particles expiring after duration"""
    containers: tuple[pygame.sprite.Group, ...]
    
    def __init__(self, x: float, y: float, radius: float, duration:float, color: pygame.Color | str | list[int], rotation:float = 0, turn_speed:int = 0) -> None:
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()
        self.random_length: list[float] = [
            random.uniform(ASTEROID_MIN_POINT_PERCENTAGE, ASTEROID_MAX_POINT_PERCENTAGE) for _ in range(ASTEROID_POINTS)
        ]
        
        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.rotation = rotation
        self.radius = radius
        self.duration = duration
        self.turn_speed = turn_speed
        self.color = color

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        self.rotate(dt)
        
        self.duration -= dt
        if self.duration <= 0:
            self.kill()

    def equ_triangle(self) -> list[pygame.Vector2]:
        unit_vect = pygame.Vector2(0, 1)
        forward = unit_vect.rotate(self.rotation) * self.radius
        a = self.position + forward
        b = self.position + forward.rotate(120)
        c = self.position + forward.rotate(-120)
        return [a, b, c]

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

    def rotate(self, dt: float) -> None:
        self.rotation += self.turn_speed * dt