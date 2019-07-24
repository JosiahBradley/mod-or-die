from abc import ABC, abstractmethod
from typing import List, Dict
import os
import arcade


class Conf:
    def __init__(self):
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 960
        self.TILE_RADIUS = 64

        # Resources
        self.FILE_ROOT = os.path.dirname(__file__)
        self.SPRITE_RESOURCES = os.path.abspath(self.FILE_ROOT + "/../resources/arcade/character_sprites/")
        self.AUDIO_RESOURCES = os.path.abspath(self.FILE_ROOT + "/../resources/audio/")
        self.TILE_RESOURCES = os.path.abspath(self.FILE_ROOT + "/../resources/arcade/tiles/")

        # How many pixels to keep as a minimum margin between the character
        # and the edge of the screen.
        self.LEFT_VIEWPORT_MARGIN = 300
        self.RIGHT_VIEWPORT_MARGIN = 300
        self.BOTTOM_VIEWPORT_MARGIN = 150
        self.TOP_VIEWPORT_MARGIN = 100

        self.PLAYER_START_X, self.PLAYER_START_Y = (200, 200)


class Player(arcade.Sprite, ABC):
    pass


class MetaLevel(type(arcade.Window), type(ABC)):
    pass


class BaseLevel(arcade.Window, metaclass=MetaLevel):
    """
    Base Level to implement other levels

    Provides functions for drawing the ground and base functions to override.
    """

    def __init__(self, title: str="LEVEL", gravity: float=1.0, speed: float=20.0, map: Dict[int, Dict]=None):
        self.conf = Conf()
        super().__init__(self.conf.SCREEN_WIDTH, self.conf.SCREEN_HEIGHT, title)

        self.assets = {
            "statics": None,
            "objects": None,
            "block": None,
            "enemy": None,
            "player": None,
        }

        self.player = None

        self.is_game_over = False
        self.jump_sound = None

        # Our physics engine
        self.map = map
        self.gravity = gravity
        self.speed = speed
        self.jump_speed = speed * 2
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        for k in self.assets.keys():
            self.assets[k] = arcade.SpriteList()

        self.player = Player()
        self.player.center_x, self.player.center_y = (self.conf.PLAYER_START_X, self.conf.PLAYER_START_Y)
        self.player.texture = self.a_tex("character0")

        self.jump_sound = self.audio("jump1")

        self.assets["player"].append(self.player)

        if self.map:
            self._init_map()
        else:
            self.draw_map()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.assets["block"],
                                                             self.gravity)

    @abstractmethod
    def draw_map(self):
        wall = self.tile_sprite("grassLeft")
        wall.center_x = 0
        wall.center_y = self.conf.TILE_RADIUS
        self.assets["block"].append(wall)
        for x in range(2 * self.conf.TILE_RADIUS, 100 * 2 * self.conf.TILE_RADIUS, 2 * self.conf.TILE_RADIUS):
            wall = self.tile_sprite("grassMid")
            wall.center_x = x
            wall.center_y = self.conf.TILE_RADIUS
            self.assets["block"].append(wall)
        wall = self.tile_sprite("grassRight")
        wall.center_x = 100 * 2 * self.conf.TILE_RADIUS
        wall.center_y = self.conf.TILE_RADIUS
        self.assets["block"].append(wall)

    @staticmethod
    def sprite(path, name):
        return arcade.Sprite(path + '/' + name + ".png")

    def audio(self, name):
        return arcade.load_sound(self.conf.AUDIO_RESOURCES + '/' + name + ".wav")

    def a_sprite(self, name):
        return self.sprite(self.conf.SPRITE_RESOURCES, name)

    def a_tex(self, name):
        return arcade.load_texture(self.conf.SPRITE_RESOURCES + '/' + name + ".png")

    def tile_sprite(self, name):
        return self.sprite(self.conf.TILE_RESOURCES, name)

    @abstractmethod
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        for k in self.assets.keys():
            self.assets[k].draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            self.view_left + .8 * self.get_size()[0],
            self.view_bottom + .95 * self.get_size()[1],
            arcade.csscolor.WHITE, 18
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = self.jump_speed
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -self.speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = self.speed

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    @abstractmethod
    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        self.assets["player"].update()
        self.assets["player"].update_animation()

        # --- Manage Scrolling ---

        # Prevent walking off the left side
        if self.player.left <= 0:
            self.player.change_x = 0
            self.player.center_x = self.conf.TILE_RADIUS

        # Kill player if they fall into a pit
        if self.player.bottom < 0:
            self.game_over()

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + self.conf.LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + self.conf.SCREEN_WIDTH - self.conf.RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + self.conf.SCREEN_HEIGHT - self.conf.TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + self.conf.BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                self.conf.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                self.conf.SCREEN_HEIGHT + self.view_bottom)

    def game_over(self):
        # self.physics_engine = None
        self.audio("gameover2")
        self.setup()

    @abstractmethod
    def win(self):
        self.is_game_over = True
        for k in self.assets.keys():
            self.assets[k] = arcade.SpriteList()
