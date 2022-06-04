import os

import pyglet
from pyglet.window import key, FPSDisplay

from asteroids import resources, load, utils
from asteroids.player import Player
from asteroids.resources import resources_path
from asteroids.bullet import Bullet


class AsteroidGameStates:
    MAIN_MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
    TOP_SCORES = 4
    SELECT_LEVEL = 5


class AsteroidsWindow(pyglet.window.Window):
    
    def __init__(self, *args, **kwargs):
        super(AsteroidsWindow, self).__init__(800, 600, *args, **kwargs)

        self.game_state = AsteroidGameStates.MAIN_MENU

        self.level = 1
        self.score = 0

        self.fps_display = FPSDisplay(self)
        self.show_fps = False

        self.main_menu_batch = pyglet.graphics.Batch()
        self.main_menu, self.main_menu_asteroids = \
            self.create_main_menu(self.main_menu_batch)

        self.top_score_batch = pyglet.graphics.Batch()
        self.top_scores = self.load_top_scores(resources.top_scores_filepath
            )
        self.top_score_menu = \
            self.create_top_score_menu(self.top_score_batch, self.top_scores)

        self.game_batch = pyglet.graphics.Batch()
        game_objects = self.create_game_objects(self.game_batch)
        self.game_objects, self.player_ship, self.asteroids = game_objects

        self.game_label_batch = pyglet.graphics.Batch()
        self.player_lives, \
            self.score_label, \
            self.level_label = self.create_game_labels(self.game_label_batch)

        self.pause_menu_batch = pyglet.graphics.Batch()
        self.pause_menu = self.create_pause_menu(self.pause_menu_batch)

        self.game_over_batch = pyglet.graphics.Batch()
        # This is the default text that is displayed when the game is over
        self.player_name = ['_', '_', '_']
        self.player_name_input_index = 0

        game_over = self.create_game_over_labels(self.game_over_batch)
        self.game_over_score_label, self.game_over_name_label = game_over

        self.key_handler = key.KeyStateHandler()
        self.push_handlers(self.key_handler)

        # This is the last line in __init__ because all the game elements
        # need to be loaded before update is called
        pyglet.clock.schedule_interval(self.update, 1.0 / 120.0)

    def load_top_scores(self, filename):
        if not os.path.isfile(filename):
            os.system("touch "+filename)
        
        f = open(filename, 'r')
        top_scores = []
        for line in f.readlines():
            info = line.split()
            top_scores.append({
                'name': info[0], 
                'level': int(info[1]), 
                'score': int(info[2])
            })

        key = lambda score: score['score']
        return sorted(top_scores, key=key, reverse=True)

    def create_top_score_menu(
            self, top_score_batch, top_scores, create_title=True):
        if create_title:
            top_score_label = \
                utils.create_title_label('Top scores', top_score_batch)

        top_score_texts = []
        for ts in top_scores[:5]:
            score_text = '{} {} {}'.format(
                ts['name'], ts['level'], ts['score'])
            top_score_texts.append(score_text)

        top_score_texts.append('Main menu')

        return utils.create_menu_labels(top_score_texts, top_score_batch)

    def create_main_menu(self, main_menu_batch):
        asteroids_game_label = utils.create_title_label(
            'Asteroids', main_menu_batch)
        menu_asteroids = load.asteroids(
            25, random_sizes=True, batch=main_menu_batch)        

        menu_label_texts = ['New game', 'Top scores', 'Exit']

        return (
            utils.create_menu_labels(menu_label_texts, main_menu_batch), 
            menu_asteroids,
        )

    def create_pause_menu(self, pause_menu_batch):
        paused_game_label = \
            utils.create_title_label('Paused', pause_menu_batch)

        menu_label_texts = ['Resume game', 'Main menu', 'Exit']

        return utils.create_menu_labels(menu_label_texts, pause_menu_batch)

    def create_game_over_labels(self, game_over_batch):
        game_over_label = utils.create_title_label(
            'Game over', game_over_batch)

        l0 = utils.create_menu_label(
            self.score_label.text,
            game_over_batch,
            selected=True
        )
        l1 = utils.create_menu_label(
            '{} {} {}'.format(
                self.player_name[0],
                self.player_name[1],
                self.player_name[2],
            ),
            game_over_batch, 
            selected=True,
            y=320,
        )
        return l0, l1 

    def spawn_new_player_ship(self, game_batch):
        new_ship = Player(x=400, y=300, batch=game_batch)
        new_ship.rotation = 270
        return new_ship

    def create_game_objects(self, game_batch):
        player_ship = self.spawn_new_player_ship(game_batch)

        asteroids = load.asteroids(2 + self.level, player_ship.position, batch=game_batch)

        game_objects = [player_ship] + asteroids

        return game_objects, player_ship, asteroids


    def reset_player_lives (self, game_label_batch):
        return load.player_lives(10, batch=game_label_batch)

    def create_game_labels(self, game_label_batch):
        player_lives = self.reset_player_lives(game_label_batch)


        score_label = pyglet.text.Label(
            text='Score: %d' % self.score,
            x=10, y=575,
            font_name='Syncopate',
            batch=game_label_batch,
        )

        level_label = pyglet.text.Label(
            text='Level %d' % self.level,
            x=300, y=575,
            anchor_x='center',
            font_name='Syncopate',
            batch=game_label_batch,
        )
                                        
        return player_lives, score_label, level_label

    def on_draw(self):
        self.clear()

        if self.game_state == AsteroidGameStates.MAIN_MENU:
            self.main_menu_batch.draw()
        
        elif self.game_state == AsteroidGameStates.PLAYING:
            self.game_batch.draw()
            self.game_label_batch.draw()
            
        elif self.game_state == AsteroidGameStates.PAUSED:
            self.game_batch.draw()
            self.pause_menu_batch.draw()
        
        elif self.game_state == AsteroidGameStates.GAME_OVER:
            self.game_batch.draw()
            self.game_over_batch.draw()
        
        elif self.game_state == AsteroidGameStates.TOP_SCORES:
            self.top_score_batch.draw()

        if self.show_fps:
            self.fps_display.draw()

    def update(self, dt):
        if self.game_state == AsteroidGameStates.MAIN_MENU:
            for obj in self.main_menu_asteroids:
                obj.update(dt)

        elif self.game_state == AsteroidGameStates.PLAYING:
            # throw the key states to the player_ship and update it
            self.player_ship.update(dt, self.key_handler)

            # Check collisions
            for i in range(len(self.game_objects)):
                for j in range(i+1, len(self.game_objects)):
                    obj_i = self.game_objects[i]
                    obj_j = self.game_objects[j]

                    if not obj_i.dead and not obj_j.dead:
                        if obj_i.collides_with(obj_j):
                            obj_i.handle_collision_with(obj_j)
                            obj_j.handle_collision_with(obj_i)

            # update other game objects 
            # and add new objects if they have been spawned
            to_add = []
            for obj in self.game_objects:
                if not obj == self.player_ship:
                    obj.update(dt)

                if obj in self.asteroids:
                    self.asteroids.extend(obj.new_objects)

                to_add.extend(obj.new_objects)
                obj.new_objects = []

            # Remove dead objects from the scene
            for to_remove in [obj for obj in self.game_objects if obj.dead]:
                is_bullet = isinstance(to_remove, Bullet)
                if not to_remove == self.player_ship and not is_bullet:
                    self.score += 1 / to_remove.scale

                to_remove.delete()
                self.game_objects.remove(to_remove)
                if to_remove in self.asteroids:
                    self.asteroids.remove(to_remove)

            # Update score label
            self.score_label.text = 'Score: %d' % self.score

            # Add the new objects to the scene now
            self.game_objects.extend(to_add)

            # You are dead, but you still have some lives left
            if not self.player_ship in self.game_objects and len(self.player_lives) > 1:
                self.player_lives[-1].delete()
                self.player_ship = self.spawn_new_player_ship(self.game_batch)
                self.game_objects.append(self.player_ship)
                self.player_lives.remove(self.player_lives[-1])

            # HAHAHA You suck, you couldn't even kill some lame asteroids
            # Horrible astronaut pilot skills
            elif not self.player_ship in self.game_objects and len(self.player_lives) == 1:
                self.game_state = AsteroidGameStates.GAME_OVER
                self.game_over_score_label.text = self.score_label.text

            # Level complete!
            if not len(self.asteroids) and self.game_state == AsteroidGameStates.PLAYING:
                self.level += 1
                self.level_label.text = 'Level %d' % self.level
                self.asteroids = load.asteroids(
                        2 + self.level, 
                        self.player_ship.position, 
                        batch=self.game_batch,
                    )
                self.game_objects.extend(self.asteroids)
                    
                self.player_lives = self.reset_player_lives(self.game_batch)
                
    def on_key_press(self, symbol, modifiers):
        """ Handles key presses in/for menus and toggling fps display """
        if symbol == key.F and not self.game_state == AsteroidGameStates.GAME_OVER:
            self.show_fps = not self.show_fps

        if self.game_state == AsteroidGameStates.MAIN_MENU or \
                self.game_state == AsteroidGameStates.PAUSED or \
                self.game_state == AsteroidGameStates.TOP_SCORES:
            menu = None
            menu_name = None

            if self.game_state == AsteroidGameStates.MAIN_MENU:
                menu = self.main_menu
                menu_name = 'main'
            elif self.game_state == AsteroidGameStates.PAUSED:
                menu = self.pause_menu
                menu_name = 'pause'
            elif self.game_state == AsteroidGameStates.TOP_SCORES:
                menu = self.top_score_menu
                menu_name = 'top score'

            if symbol == key.DOWN:
                self.move_menu_select(menu, 1)
            elif symbol == key.UP:
                self.move_menu_select(menu, -1)
            elif symbol == key.ENTER:
                self.handle_menu_press(
                    self.selected_menu_text(menu), menu_name)

        if symbol == key.ESCAPE and self.game_state == AsteroidGameStates.PLAYING:
            self.game_state = AsteroidGameStates.PAUSED

        elif symbol == key.ESCAPE and self.game_state == AsteroidGameStates.PAUSED:
            self.game_state = AsteroidGameStates.PLAYING

        if symbol == key.ENTER and self.game_state == AsteroidGameStates.GAME_OVER:
            self.game_state = AsteroidGameStates.MAIN_MENU
            # reset game objects
            self.score = 0
            self.level = 1
            self.game_batch = pyglet.graphics.Batch()
            self.game_objects, \
                self.player_ship, \
                self.asteroids = self.create_game_objects(self.game_batch)
            self.game_label_batch = pyglet.graphics.Batch()
            self.player_lives, \
                self.score_label, \
                self.level_label = self.create_game_labels(self.game_label_batch)

        elif self.game_state == AsteroidGameStates.GAME_OVER:
            self.player_name[self.player_name_input_index] = \
                key.symbol_string(symbol)[0]
            self.player_name_input_index += 1
            self.player_name_input_index %= 3
            self.game_over_name_label.text = \
                '%s %s %s' % (
                    self.player_name[0],
                    self.player_name[1],
                    self.player_name[2],
                )

    def move_menu_select(self, menu, index):
        """ moves the selected menu item by index amount of items """
        prev_selected_index = 0
        for i in range(len(menu)):
            if menu[i].color[3] == 255:
                prev_selected_index = i

        menu[prev_selected_index].color = (255, 255, 255, 76)
        menu[(prev_selected_index+index)%len(menu)].color = \
            (255, 255, 255, 255)

    def selected_menu_text(self, menu):
        """ Get's the selected menu item's text """

        selected_index = 0
        for i in range(len(menu)):
            if menu[i].color[3] == 255:
                selected_index = i

        return menu[selected_index].text

    def handle_menu_press(self, selected_text, menu_name):
        """ Handles selection in menus """

        if menu_name == 'main':
            if selected_text == 'Exit':
                pyglet.app.exit()

            elif selected_text == 'Select Level':
                self.game_state = AsteroidGameStates.PLAYING

            elif selected_text == 'New game':
                self.game_state = AsteroidGameStates.PLAYING

            elif selected_text == 'Top scores':
                self.game_state = AsteroidGameStates.TOP_SCORES 

        elif menu_name == 'pause':
            if selected_text == 'Resume game':
                self.game_state = AsteroidGameStates.PLAYING

            elif selected_text == 'Main menu':
                self.game_state = AsteroidGameStates.MAIN_MENU
                # reset game objects
                self.score = 0
                self.level = 1
                self.game_batch = pyglet.graphics.Batch()
                self.game_objects, \
                    self.player_ship, \
                    self.asteroids = self.create_game_objects(self.game_batch)
                self.game_label_batch = pyglet.graphics.Batch()

                self.player_lives, self.score_label, self.level_label = \
                    self.create_game_labels(self.game_label_batch)

            elif selected_text == 'Exit':
                pyglet.app.exit()

        elif menu_name == 'top score':

            if selected_text == 'Main menu':
                self.game_state = AsteroidGameStates.MAIN_MENU
