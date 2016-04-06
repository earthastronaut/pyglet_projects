import pyglet

from asteroids import resources
from asteroids.physicalobject import PhysicalObject


class Bullet(PhysicalObject):
    """ Bullets fired by the player """

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)
        pyglet.clock.schedule_once(self.die, 0.75)
        
    def die(self, dt):
        self.dead = True
