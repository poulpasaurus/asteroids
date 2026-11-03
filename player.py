import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float = PLAYER_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.rotation = 0.0
        self.shot_cooldown = 0.0

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    # override
    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle(), width=LINE_WIDTH)

    def rotate (self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        # unit_vector.rotate() returns a new vector – it doesn't modify the original
        rotated_vector = unit_vector.rotate(self.rotation)
        # the rotation works by changing using the polar form (length r and angle a) so x = r * cos(a), y = r * sin(a)
        # so rotating by θ is : 
        #   x' = r*cos(a+θ) = r·cos α·cos θ − r·sin α·sin θ = x·cos θ − y·sin c
        #   y' = r*sin(a+θ) = r·sin α·cos θ + r·cos α·sin θ = x·sin θ + y·cos θ
        rotated_speed_vector = rotated_vector * dt * PLAYER_SPEED
        self.position += rotated_speed_vector

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        
        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        self.shot_cooldown -= dt
        if keys[pygame.K_SPACE]:
            self.shoot()

    def shoot(self) ->None:
        # if we waited long enough, we can shoot
        if self.shot_cooldown > 0:
            return
        self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        unit_vect = pygame.Vector2(0, 1)
        rotated_vect = unit_vect.rotate(self.rotation)
        rotated_speed_vect = rotated_vect * PLAYER_SHOOT_SPEED
        shot.velocity = rotated_speed_vect
