import os

import pyglet


game_path = os.path.dirname(os.path.abspath(__file__))
resources_path = os.path.join(game_path, "resources/")

pyglet.resource.path.append(resources_path)
pyglet.resource.reindex()


def center_image(image):
    """ Sets an image's anchor point to its center """
    image.anchor_x = image.width/2.0
    image.anchor_y = image.height/2.0


def center_images(*images):
    """ Plural of the center_image function """
    for i in images:
        center_image(i)


player_image = pyglet.resource.image('player.png')
bullet_image = pyglet.resource.image('bullet.png')
bullet_sound = pyglet.media.load(
    os.path.join(resources_path,'phew.wav'), streaming=False)

top_scores_filepath = os.path.join(resources_path, 'top_scores.txt')

asteroid_images = [
    pyglet.resource.image('asteroid.png'),
    pyglet.resource.image('asteroid2.png'),
    pyglet.resource.image('asteroid3.png'),
    pyglet.resource.image('asteroid4.png')
]

engine_image = pyglet.resource.image('engine_flame.png')
engine_image.anchor_x = engine_image.width * 1.85
engine_image.anchor_y = engine_image.height / 2.0

center_images(player_image, bullet_image)
center_images(*asteroid_images)

# Fonts
pyglet.font.add_file(os.path.join(resources_path,'Syncopate-Regular.ttf'))
pyglet.font.add_file(os.path.join(resources_path,'Syncopate-Bold.ttf'))
