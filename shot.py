import pygame

from circleshape import CircleShape
from shotparticle import ShotParticle
from constants import WEAPON_ROCKET_NB_SCHRAPNELS, SUB_ROCKET_SIZE_TO_ORIGINAL, LINE_WIDTH, SHOW_HITBOXES

class Shot(CircleShape):
    def __init__(self, x: float, y: float, radius:float) -> None:
        super().__init__(x, y, radius)

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
        self.trail()

    def trail(self) -> None:
        ShotParticle(self.position.x, self.position.y, self.radius)


class Rocket(Shot):
    def __init__(self, x:float, y:float, radius:float) -> None:
        super().__init__(x, y, radius)

    #override
    def update(self, dt: float) -> None:
        super().update(dt)
        # spawn shrapnels
        angle = 360 / WEAPON_ROCKET_NB_SCHRAPNELS
        for i in range(WEAPON_ROCKET_NB_SCHRAPNELS):
            shrapnel = Shot(self.position.x, self.position.y, self.radius * SUB_ROCKET_SIZE_TO_ORIGINAL)
            shrapnel.velocity = self.velocity.rotate(i * angle)
