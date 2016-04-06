#!env python
"""
                        . . .                         
                         \|/                          
                       `--+--'                        
                         /|\                          
                        ' | '                         
                          |                           
                          |                           
                      ,--'#`--.                       
                      |#######|                       
                   _.-'#######`-._                    
                ,-'###############`-.                 
              ,'#####################`,               
             /#########################\              
            |###########################|             
           |#############################|            
           |#############################|            
           |#############################|            
           |#############################|            
            |###########################|             
             \#########################/              
              `.#####################,'               
                `._###############_,'                 
                   `--..#####..--'      

"""
import random

from pyglet.window import key
import pyglet


BOARD_WIDTH = 25
BOARD_HEIGHT = 10
BOARD_PIXEL_SCALE = 50

DEBUG = False


# ########################################################################### #


def get_random_position():
    """ Return a random position

    Returns:
        i (int): Horizontal index
        j (int): Vertical index
    """
    return (
        random.randrange(0, BOARD_WIDTH),
        random.randrange(0, BOARD_HEIGHT),
    )


def index_to_pixels(i, j):
    """ Take the index (lower left corner) and return pixel locations

    Args:
        i (int): Horizontal index
        j (int): Vertical index

    Returns:
        float: lower left x pixel
        float: lower left y pixel
        float: width
        float: height
    """
    x = int(i) * BOARD_PIXEL_SCALE
    y = int(j) * BOARD_PIXEL_SCALE
    dx = dy = BOARD_PIXEL_SCALE
    return x, y, dx, dy     


def all_positions():
    """ Iterator of all valid board positions

    Returns
        int: horizontal index
        int: vertical index

    """
    for i in range(0, BOARD_WIDTH):
        for j in range(0, BOARD_HEIGHT):
            yield i, j


def get_all_surrounding_positions(position):
    """ For a given position get all surrounding positions

    Returns:
        (int, int): lower left
        (int, int): left
        (int, int): upper left
        (int, int): up
        (int, int): upper right
        (int, int): right
        (int, int): lower right
        (int, int): down
    """
    i, j = position
    return (
        (i-1, j-1),  # lower left
        (i-1, j),    # left
        (i-1, j+1),  # upper left
        (i, j+1),    # up
        (i+1, j+1),  # upper right
        (i+1, j),    # right
        (i+1, j-1),  # lower right
        (i, j-1),    # down
    )


def get_plus_surrounding_positions(position):
    """ For a given position get up/down/left/right positions

    Returns:
        (int, int): left
        (int, int): up
        (int, int): right
        (int, int): down
    """
    i, j = position
    return (
        (i-1, j),  # left
        (i, j+1),  # up
        (i+1, j),  # right
        (i, j-1),  # down
    )


def create_bombs(num_bombs=10):
    """ Create bombs in random positions

    Args:
        num_bombs (int): number of bombs to create. 
            Truncated between 1 and BOARD_WIDTH * BOARD_HEIGHT - 1

    """
    max_bombs = BOARD_WIDTH * BOARD_HEIGHT - 1
    num_bombs = int(max(min(num_bombs, max_bombs), 0))

    bombs = set()
    while True:
        pos = get_random_position()
        bombs.add(pos)
        if len(bombs) >= num_bombs:
            break

    return bombs


def update_game_square(click_pos, _searched_pos=None):
    """ Logic for clicking on a square

    Args: 
        click_pos (tuple): position index of a click
        _searched_pos (None): used in recursion not to
            create infinite loops
    """
    global objects 
    if _searched_pos is None:
        _searched_pos = set()
    _searched_pos.add(click_pos)

    hidden_pos = objects['hidden']['positions']
    bomb_pos = objects['hidden']['positions']
    bomb_cnts = objects['bomb_cnts']

    if click_pos in hidden_pos:
        # you clicked on a hidden square, high-five bro!
        hidden_pos.remove(click_pos)

    if click_pos in bomb_pos:
        # awww, snap! you're going to lose!
        return

    plus_positions = get_plus_surrounding_positions(click_pos)
    all_positions = get_all_surrounding_positions(click_pos)

    if bomb_cnts[click_pos] == 0: 
        # yay, you clicked on an spot with no bombs around       
        for pos_near in all_positions:
            # search all the positions around you and simulate 
            # clicking on those (because they DEFINITELY don't contain bombs)

            already_searched = pos_near in _searched_pos
            if already_searched:
                continue            

            within_board = pos_near in bomb_cnts
            if within_board:
                # if position around you is within the board
                # then do the same update process

                # this causes the function to be recursive or to call itself
                # we're safe from infinite loops because the function will 
                # won't be called if we've already search this square and 
                # will return if the pos_near has bombs around it
                update_game_square(pos_near, _searched_pos=_searched_pos)


# ########################################################################### #


def draw_grid():
    """ Draw the grid lines of the board
    """
    pyglet.gl.glColor4f(0.23, 0.23, 0.93, 1.0)
    rows = int(BOARD_HEIGHT)
    columns = int(BOARD_WIDTH)

    #Horizontal lines
    for i in range(rows):
        pyglet.graphics.draw(
            2, pyglet.gl.GL_LINES, 
            ('v2i', 
                (
                    0, 
                    i * BOARD_PIXEL_SCALE, 
                    BOARD_PIXEL_SCALE * BOARD_WIDTH, 
                    i * BOARD_PIXEL_SCALE
                )
            )
        )

    #Vertical lines
    for j in range(columns):
        pyglet.graphics.draw(
            2, pyglet.gl.GL_LINES, 
            ('v2i', 
                (
                    j * BOARD_PIXEL_SCALE, 
                    0, 
                    j * BOARD_PIXEL_SCALE, 
                    BOARD_HEIGHT * BOARD_PIXEL_SCALE,
                )
            )
        )


def draw_board_square(position, color_rgba=(0, 0, 0, 0)):
    """ draw a board_square filled with a particular thing

    Args:
        position (tuple): (i, j) = (horizontal index, vertical index)
        color_rgba (tuple): (red, green, blue, alpha)

    Returns:
        None: draws a rectangle on the screen
    """
    i, j = position
    x, y, dx, dy = index_to_pixels(i, j)
    corners = [
        x, y,       # lower left
        x, y+dy,    # upper left
        x+dx, y+dy, # upper right
        x+dx, y,    # lower right
    ]
    pyglet.gl.glColor4f(*color_rgba)
    pyglet.graphics.draw(4, pyglet.gl.GL_QUADS, ('v2f', corners))


def draw_text_board_square(position, text, color_rgba=(0.5, 0.23, 0.23, 1.0)):
    """ Draw text within a particular square
    """
    i, j = position
    x, y, dx, dy = index_to_pixels(i, j)

    xc = x + dx * 0.5
    yc = y + dy * 0.5

    pyglet.gl.glColor4f(*color_rgba)
    pyglet.text.Label(
        str(text),
        font_name='Times New Roman',
        font_size=20,
        x=xc, 
        y=yc,
        anchor_x='center', 
        anchor_y='center',
    ).draw()


# ########################################################################### #


def game_on_draw():
    """ Called when drawing the board
    """
    global window, objects

    print('game_on_draw')

    window.clear()

    hidden_pos = objects['hidden']['positions']
    hidden_color = objects['hidden']['color']
    bomb_pos = objects['bombs']['positions']
    bomb_color = objects['bombs']['color']
    bomb_cnts = objects['bomb_cnts']
    flagged_as_bomb = objects['flagged_as_bomb']['positions']
    flagged_color = objects['flagged_as_bomb']['color']

    user_wins = len(hidden_pos - bomb_pos) == 0
    game_over = user_wins

    for pos in all_positions():
        num_bombs = bomb_cnts[pos]

        if pos in hidden_pos:
            if pos in flagged_as_bomb:
                draw_board_square(pos, flagged_color)
            else:
                draw_board_square(pos, hidden_color)

        elif pos in bomb_pos:
            draw_board_square(pos, bomb_color)
            game_over = True

        elif num_bombs > 0:
            draw_board_square(pos, (0.0, 0.2, 0.2, 0.0))                
            color_rgba = (1.0, 0.2, 0.2, 0.0)
            draw_text_board_square(pos, num_bombs, color_rgba=color_rgba)

    if DEBUG:
        for pos in all_positions():
            if pos in bomb_pos:
                draw_board_square(pos, (1.0, 0.2, 0.2, 50.0))
            draw_text_board_square(
                pos, bomb_cnts[pos], (0.0, 1.0, 0.0, 0.0))

    print('')

    draw_grid()

    if game_over:
        for pos in bomb_pos:
            draw_board_square(pos, bomb_color)

        if user_wins:
            print('CONGRATS, YOU WON!')        

        if not DEBUG:
            end_game()


def game_on_mouse_press(x, y, button, modifiers):
    """ Called when the mouse is clicked within the window
    """
    global objects 

    print('game_on_mouse_press')  

    bomb_pos = objects['bombs']['positions']
    hidden_pos = objects['hidden']['positions']
    flagged_as_bomb = objects['flagged_as_bomb']['positions']

    i = int(x / BOARD_PIXEL_SCALE)
    j = int(y /BOARD_PIXEL_SCALE)
    click_pos = (i, j)
    print('click {} with position={} modifiers={}'.format(
        button, click_pos, modifiers))    

    if button == pyglet.window.mouse.LEFT:
        if modifiers == pyglet.window.key.MOD_SHIFT:
            if click_pos in hidden_pos:
                remove_flag = click_pos in flagged_as_bomb
                print('flag_position={}'.format(not remove_flag))
                if remove_flag:
                    flagged_as_bomb.remove(click_pos)
                else:
                    flagged_as_bomb.add(click_pos)
        else:
            if click_pos not in flagged_as_bomb:        
                print('not flagged')    
                update_game_square(click_pos)


# ########################################################################### #


def start_game(num_bombs=15):
    """ Start game by initializing objects and adding handlers
    """
    global objects

    print('start_game')
    
    bomb_pos = set(create_bombs(num_bombs=num_bombs))
    bomb_cnts = {}
    for pos in all_positions():
        num_bombs = 0
        for pos_near in get_all_surrounding_positions(pos):
            if pos_near in bomb_pos:
                num_bombs += 1
        bomb_cnts[pos] = num_bombs

    objects = {
        'bombs': {
            'positions': bomb_pos,
            'color': (1.0, 0.01, 0.01, 0),
        },
        'hidden': {
            'positions': set(all_positions()),    
            'color': (0.25, 0.25, 0.25, 0),
        },
        'flagged_as_bomb': {
            'positions': set(),
            'color': (0.8, 0.0, 0.8, 0),
        },
        'bomb_cnts': bomb_cnts,
    }

    window.push_handlers(
        on_mouse_press=game_on_mouse_press,
        on_draw=game_on_draw,
    )


def end_game():
    """ End game by removing handlers """
    global window 

    print('')
    print('GAME OVER'.center(30))
    
    window.remove_handler('on_mouse_press', game_on_mouse_press)
    window.remove_handler('on_draw', game_on_draw)


# ########################################################################### #


# cursor = window.get_system_mouse_cursor(win.CURSOR_HAND)
# window.set_mouse_cursor(cursor)

if __name__ == "__main__":

    objects = {}
    window = pyglet.window.Window(
        BOARD_WIDTH * BOARD_PIXEL_SCALE,
        BOARD_HEIGHT * BOARD_PIXEL_SCALE,
        caption='Mine Sweeper',
    )

    start_game(num_bombs=25)
    pyglet.app.run()
