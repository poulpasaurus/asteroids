import pygame
import random

from shot import Shot, Rocket
from constants import *


class Weapon():
    def __init__(self, cooldown:float | list[float]):
        self.cooldown = cooldown

    def shot(self, x:float, y:float, rotated_vect:pygame.Vector2) -> None:
        #must override
        pass

    def get_cooldown(self):
        return self.cooldown


class Blaster(Weapon):
    def __init__(self):
        super().__init__(WEAPON_BLASTER_COOLDOWN)

    def shot(self, x:float, y:float, rotated_vect:pygame.Vector2) -> None:
        shot = Shot(x, y, WEAPON_BLASTER_RADIUS)
        shot.velocity = rotated_vect * WEAPON_BLASTER_SHOT_SPEED


class RocketLauncher(Weapon):
    def __init__(self):
        super().__init__(WEAPON_ROCKET_COOLDOWN)

    def shot(self, x:float, y:float, rotated_vect:pygame.Vector2) -> None:
        rocket = Rocket(x, y, WEAPON_ROCKET_RADIUS)
        rocket.velocity = rotated_vect * WEAPON_ROCKET_SHOT_SPEED


class Burst(Weapon):
    def __init__(self):
        cooldown = [0.01 for _ in range(WEAPON_BURST_NB_BULLETS)]
        cooldown.append(WEAPON_BURST_COOLDOWN)
        
        super().__init__(cooldown)
        self.idx = 0

    def shot(self, x:float, y:float, rotated_vect:pygame.Vector2) -> None:
        shot = Shot(x, y, WEAPON_BURST_RADIUS)
        random_rotated_vect = rotated_vect.rotate(random.uniform(-5, 5))
        shot.velocity = random_rotated_vect * WEAPON_BURST_SHOT_SPEED

    # override
    def get_cooldown(self):
        if self.idx > WEAPON_BURST_NB_BULLETS:
            self.idx = 0
        current_cooldown = self.cooldown[self.idx]
        self.idx += 1
        return current_cooldown
