import time
import pyglet
import math

from pyglet.window import key

from asteroids import resources
from asteroids.physicalobject import PhysicalObject
from asteroids.asteroid import Asteroid
from asteroids.bullet import Bullet


def clip(x, a, b):
    """ clips the value x to be between a and b
    """
    if x < a:
        return a
    elif x >= b:
        return b
    return x


class Player(PhysicalObject):
    """ Player object """

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=resources.player_image, *args, **kwargs)
        
        self.thrust = 300.0
        self.rotate_speed = 250.0
        self.max_velocity = 700

        self.bullet_speed = 700.0
        self.reload_time_seconds = 0.2
                
        self.ready_to_fire = True
        
        self.key_handler = key.KeyStateHandler()

        self.engine_sprite = pyglet.sprite.Sprite(
            img=resources.engine_image, *args, **kwargs)
        self.engine_sprite.visible = False
        
    def update(self, dt, key_handler):
        super(Player, self).update(dt)

        if key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt

        if key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt

        if key_handler[key.UP]:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.thrust * dt
            force_y = math.sin(angle_radians) * self.thrust * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
            
            self.engine_sprite.rotation = self.rotation
            self.engine_sprite.x = self.x
            self.engine_sprite.y = self.y
            self.engine_sprite.visible = True

        else:
            self.engine_sprite.visible = False

        if key_handler[key.SPACE] and self.ready_to_fire:
            self.fire()
            if self.reload_time_seconds > 0:
                self.ready_to_fire = False
                pyglet.clock.schedule_once(
                    self.reload, self.reload_time_seconds)

        mv = self.max_velocity
        self.velocity_x = clip(self.velocity_x, -mv,mv)
        self.velocity_y = clip(self.velocity_y, -mv,mv)        
        
    def delete(self):
        self.engine_sprite.delete()
        super(Player, self).delete()
      
    def fire(self):
        # resources.bullet_sound.play()
        
        angle_radians = -math.radians(self.rotation)

        ship_radius = self.image.width/2
        bullet_x = self.x + math.cos(angle_radians) * ship_radius
        bullet_y = self.y + math.sin(angle_radians) * ship_radius
        new_bullet = Bullet(bullet_x, bullet_y, batch=self.batch)

        vx = self.velocity_x
        vy = self.velocity_y
        s = self.bullet_speed
        new_bullet.velocity_x = vx + s * math.cos(angle_radians)
        new_bullet.velocity_y = vy + s * math.sin(angle_radians)

        self.new_objects.append(new_bullet)

    def reload(self, dt):
        self.ready_to_fire = True

    def collides_with(self, other_object):
        if isinstance(other_object, Bullet):
            return False
        return super().collides_with(other_object)

    def handle_collision_with(self, other_object):
        """ handle a collision """
        if not isinstance(other_object, Bullet):
            self.dead = not (other_object.__class__ == self.__class__)
