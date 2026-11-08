import pygame
from constants import *

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius
        self.hitbox_radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        # must override
        pass

    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other: "CircleShape") -> bool:
        dist = self.position.distance_to(other.position)
        return dist <= (self.hitbox_radius + other.hitbox_radius)

    def off_screen_wrap(self, wrap_margin=None) -> None:
        """
        Wrap an object around the screen instead of letting it drift into the void
        Used by the player and asteroids
        """
        # to keep the current asteroid spawning mechanic
        if wrap_margin is None:
            wrap_margin = self.radius

        # wrap around the screen
        if self.position.x < (-wrap_margin):
            self.position.x = (SCREEN_WIDTH + self.radius)
        if self.position.x > (wrap_margin + SCREEN_WIDTH):
            self.position.x = -self.radius

        if self.position.y < (-wrap_margin):
            self.position.y = (SCREEN_HEIGHT + self.radius)
        if self.position.y > (wrap_margin + SCREEN_HEIGHT):
            self.position.y = (-self.radius)

    def off_screen_kill(self) -> None:
        """
        Kill an object off-screen instead of letting it drift into the void
        Used by the shots
        """
        if (self.position.x < (-self.radius)) or (self.position.x > (self.radius + SCREEN_WIDTH)) or (self.position.y < (-self.radius)) or (self.position.y > (self.radius + SCREEN_HEIGHT)):
            self.kill()
