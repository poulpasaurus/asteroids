import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    # print(f"Screen width: {SCREEN_WIDTH}")
    # print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    dt = 0.0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    # add ALL FUTURE intances of players to all groups it should belong to
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    
    x = SCREEN_WIDTH / 2
    y = SCREEN_HEIGHT / 2
    player = Player(x, y)
    asteroid_field = AsteroidField()

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill("black")

        # update every updatable
        updatable.update(dt)
        # draw every drawable sprite instead of doing it one by one
        # /!\ 
        # Group.draw(screen) does not call your draw method
        # It expects each sprite to have .image and .rect attributes and blits those 
        # My shapes don't have them, because they're drawn with pygame.draw.polygon 
        # So I need to loop over the group and call each object's own draw()
        for obj in drawable:
            obj.draw(screen)

        # detecting collisions
        for astr in asteroids:
            if player.collides_with(astr):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

            for shot in shots:
                if astr.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    astr.split()
                    break
                
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
