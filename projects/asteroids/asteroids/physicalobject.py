import pyglet

from asteroids.utils import distance


class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.dead = False
        self.new_objects = []

    def update(self, dt):
        """ update position """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

    def check_bounds(self):
        """ If this object is outside the screen move it to the
        other edge of the screen """

        min_x = -self.image.width / 2
        min_y = -self.image.height / 2

        max_x = 800 + self.image.width / 2
        max_y = 600 + self.image.height / 2

        if self.x < min_x:
            self.x = max_x
        elif self.x > max_x:
            self.x = min_x

        if self.y < min_y:
            self.y = max_y
        elif self.y > max_y:
            self.y = min_y

    def collides_with(self, other_object):
        """ Did another object collide with this one """
        collision_distance = self.image.width/2 + other_object.image.width/2
        actual_distance = distance(self.position, other_object.position)
        return (actual_distance <= collision_distance)

    def handle_collision_with(self, other_object):
        """ Handle the collision """
        self.dead = not (other_object.__class__ == self.__class__)
