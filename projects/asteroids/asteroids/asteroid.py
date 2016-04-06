import random

import pyglet

from asteroids import resources
from asteroids.physicalobject import PhysicalObject


class Asteroid(PhysicalObject):    
    
    def __init__(self, *args, **kwargs):
        image = resources.asteroid_images[
            random.randint(0, len(resources.asteroid_images)-1)]
        super(Asteroid, self).__init__(image, *args, **kwargs)
        self.rotate_speed = random.random() * 100.0 - 50
        
    def handle_collision_with(self, other_object):
        super(Asteroid, self).handle_collision_with(other_object)

        if self.dead and self.scale > 0.25:
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):
                new_asteroid = Asteroid(x=self.x, y=self.y, batch=self.batch)
                new_asteroid.rotation = random.randint(0, 360)
                
                vx = random.random() * 70 + self.velocity_x
                vy = random.random() * 70 + self.velocity_y
                
                new_asteroid.velocity_x = vx 
                new_asteroid.velocity_y = vy 
                new_asteroid.scale = self.scale * 0.5

                self.new_objects.append(new_asteroid)
    
    def update(self, dt):
        super(Asteroid, self).update(dt)
        self.rotation += self.rotate_speed * dt
