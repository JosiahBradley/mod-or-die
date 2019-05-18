from abc import ABC, abstractmethod
from typing import List, Dict
import os
from importlib.resources import read_binary
# os.environ['LD_LIBRARY_PATH'] = os.path.abspath(os.getcwd())
# from ctypes import cdll
# cdll.LoadLibrary("libavutil.so")
# cdll.LoadLibrary("libswresample.so")
# cdll.LoadLibrary("libswresample.so")
# cdll.LoadLibrary("libavcodec.so.56")
import arcade


class Conf():
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


        self.object_list = None
        self.block_list = None
        self.enemy_list = None
        self.player_list = None

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
        self.object_list = arcade.SpriteList()
        self.block_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        self.player = Player()
        self.player.center_x, self.player.center_y = (self.conf.PLAYER_START_X, self.conf.PLAYER_START_Y)
        self.player.texture = arcade.load_texture(self.conf.SPRITE_RESOURCES + "/character0.png")

        self.jump_sound = arcade.load_sound(self.conf.AUDIO_RESOURCES + "/jump1.wav")

        self.player_list.append(self.player)

        if self.map:
            self._init_map()
        else:
            self.draw_map()

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.block_list,
                                                             self.gravity)

    @abstractmethod
    def draw_map(self):
        wall = arcade.Sprite(self.conf.TILE_RESOURCES + "/grassLeft.png")
        wall.center_x = 0
        wall.center_y = self.conf.TILE_RADIUS
        self.block_list.append(wall)
        for x in range(2 * self.conf.TILE_RADIUS, 10 * 2 * self.conf.TILE_RADIUS, 2 * self.conf.TILE_RADIUS):
            wall = arcade.Sprite(self.conf.TILE_RESOURCES + "/grassMid.png")
            wall.center_x = x
            wall.center_y = self.conf.TILE_RADIUS
            self.block_list.append(wall)
        wall = arcade.Sprite(self.conf.TILE_RESOURCES + "/grassRight.png")
        wall.center_x = 10 * 2 * self.conf.TILE_RADIUS
        wall.center_y = self.conf.TILE_RADIUS
        self.block_list.append(wall)

    @abstractmethod
    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.block_list.draw()
        self.object_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

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

        self.player_list.update()
        self.player_list.update_animation()

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
        arcade.play_sound(arcade.load_sound(self.conf.AUDIO_RESOURCES + "/gameover2.wav"))
        self.setup()
