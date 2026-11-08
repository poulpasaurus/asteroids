import pygame
from circleshape import CircleShape
from shot import Shot
from constants import *

class Player(CircleShape):
    def __init__(self, x: float, y: float, radius: float = PLAYER_RADIUS) -> None:
        super().__init__(x, y, radius)
        self.hitbox_radius = radius * PLAYER_HITBOX_PERCENTAGE
        self.rotation = 180.0
        self.shot_cooldown = 0.0
        self.lives = PLAYER_LIVES
        self.invincibility_cooldown = 0.0 # after getting hit
        self.immobilized_cooldown = 0.0 #after getting hit
        # keep momentum
        self.previous_velocities: list[pygame.Vector2] = []
        self.old_velocity: pygame.Vector2 = pygame.Vector2(0, 0)
    
    def ship(self) -> list[pygame.Vector2]:
        """
        draw the player ship
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        # little back wings
        d = b - 0.25 * (a - b)
        e = c - 0.25 * (a - c)
        return [a, b, d, b, c, e]

    # override
    def draw(self, screen: pygame.Surface) -> None:
        if self.immobilized_cooldown < 0:
            pygame.draw.polygon(screen, "white", self.ship(), width=LINE_WIDTH)
        else: #blinking when respawning
            pass

        if SHOW_HITBOXES:
            pygame.draw.circle(screen, "red", self.position, self.hitbox_radius, LINE_WIDTH)

    def rotate (self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, 1)
        # .rotate() returns a new vector, it doesn't modify the original
        rotated_vector = unit_vector.rotate(self.rotation)
        self.velocity = rotated_vector * dt * PLAYER_SPEED
        self.position += self.velocity
    
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()

        self.immobilized_cooldown -= dt
        if self.immobilized_cooldown > 0:
            return

        self.old_velocity -= self.old_velocity * dt
        self.position += self.old_velocity

        if keys[pygame.K_z]:
            self.old_velocity = self.velocity
            self.move(dt)
        
        if keys[pygame.K_q]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        self.shot_cooldown -= dt
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.off_screen_wrap()
        self.invincibility_cooldown -= dt

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

    def hit_asteroid(self) -> None:
        self.lives -= 1
        self.invincibility_cooldown = PLAYER_INVINCIBILITY_WINDOW
        self.immobilized_cooldown = PLAYER_IMMOBILIZED_WINDOW
        # respawn in the middle of the screen
        self.rotation = 180.0
        self.velocity = pygame.Vector2(0, 0)
        self.old_velocity = pygame.Vector2(0, 0)
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
