import random

import pyglet

from asteroids import resources
from asteroids.physicalobject import PhysicalObject
from asteroids.asteroid import Asteroid
from asteroids.utils import distance


def asteroids(no_asteroids, player_position=None, random_sizes=False, batch=None):
    """ Spawns asteroids in random locations """
    asteroids = []

    for i in range(no_asteroids):
        # Find a random position for the new asteroid,
        # that isn't too close to the player.
        x, y = (random.randint(0, 800), random.randint(0, 600))
        if player_position is not None:
            while distance((x, y), player_position) < 100:
                x, y = (random.randint(0, 800), random.randint(0, 600))

        new_asteroid = Asteroid(x=x, y=y, batch=batch)
        new_asteroid.rotation = random.randint(0, 360)
        new_asteroid.velocity_x = random.random()*40
        new_asteroid.velocity_y = random.random()*40

        if random_sizes:
            new_asteroid.scale = 1.0 / 2**random.randint(0,2)

        asteroids.append(new_asteroid)

    return asteroids


def player_lives(no_lives, batch=None):
    """ Creates icons that shows the number of lives left """
    player_lives = []

    for i in range(no_lives):
        new_sprite = pyglet.sprite.Sprite(
            img=resources.player_image,
            x=785 - i * 20, 
            y=585,
            batch=batch,
        )
        new_sprite.scale = 0.5
        new_sprite.rotation = 230
        player_lives.append(new_sprite)

    return player_lives
