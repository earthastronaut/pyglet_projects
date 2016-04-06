import math 

import pyglet


def distance(p1=(0,0), p2=(0,0)):
    """ Returns the distance between two points """
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx**2 + dy**2)


def create_title_label(text, batch):
    return pyglet.text.Label(
        text=text,
        x=400, y=575,
        anchor_x='center',
        anchor_y='top',
        font_name='Syncopate',
        font_size=62,
        color=(255, 255, 255, 255),
        batch=batch,
    )


def create_menu_label(text, batch, selected=False, y=400):
    return pyglet.text.Label(
        text=text,
        x=400, y=y,
        anchor_x='center',
        anchor_y='bottom',
        font_name='Syncopate',
        font_size=42,
        color=(255, 255, 255, 255 if selected else 76),
        batch=batch,
    )


def create_menu_labels(
        texts, batch, first_selected=True, y_start=400, y_step=80):
    menu = []
    y = y_start
    for i in range(len(texts)):
        is_selected = i == 0
        menu_item = create_menu_label(texts[i], batch, is_selected, y=y)
        menu.append(menu_item)
        y -= y_step

    return menu
