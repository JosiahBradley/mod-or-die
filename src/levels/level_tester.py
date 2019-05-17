"""
Platformer Game
"""
import arcade
import os

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Level Tester"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 1
TILE_RADIUS = 64
COIN_SCALING = 0.5

# Resources
FILE_ROOT = os.path.dirname(__file__)
SPRITE_RESOURCES = os.path.abspath(FILE_ROOT +  "/../../resources/arcade/character_sprites/")
AUDIO_RESOURCES = os.path.abspath(FILE_ROOT +  "/../../resources/audio/")
TILE_RESOURCES = os.path.abspath(FILE_ROOT +  "/../../resources/arcade/tiles/")

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class L1(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player = None
        self.jump_sound = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Load sounds
        # self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        # self.jump_sound = arcade.load_sound("sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player
        self.player = arcade.AnimatedWalkingSprite()
        self.player.stand_right_textures = []
        self.player.stand_right_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character0.png",
                                                                    scale=CHARACTER_SCALING))
        self.player.stand_left_textures = []
        self.player.stand_left_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character0.png",
                                                                   scale=CHARACTER_SCALING, mirrored=True))
    
        self.player.walk_right_textures = []
    
        self.player.walk_right_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw0.png",
                                                                   scale=CHARACTER_SCALING))
        self.player.walk_right_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw1.png",
                                                                   scale=CHARACTER_SCALING))
        self.player.walk_right_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw2.png",
                                                                   scale=CHARACTER_SCALING))
        self.player.walk_right_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw3.png",
                                                                   scale=CHARACTER_SCALING))
    
        self.player.walk_left_textures = []
    
        self.player.walk_left_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw0.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw1.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw2.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_left_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/characterw3.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))

        self.player.walk_up_textures = []

        self.player.walk_up_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character2.png",
                                                                scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_up_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character3.png",
                                                                scale=CHARACTER_SCALING))
        self.player.walk_up_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character2.png",
                                                                scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_up_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character3.png",
                                                                scale=CHARACTER_SCALING))

        self.player.walk_down_textures = []
        self.player.walk_down_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character13.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_down_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character16.png",
                                                                  scale=CHARACTER_SCALING))
        self.player.walk_down_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character13.png",
                                                                  scale=CHARACTER_SCALING, mirrored=True))
        self.player.walk_down_textures.append(arcade.load_texture(SPRITE_RESOURCES + "/character16.png",
                                                                  scale=CHARACTER_SCALING))

        self.player.texture_change_distance = 64
        
        self.player.center_x = 376
        self.player.center_y = 512
        self.player.scale = 1

        self.player_list.append(self.player)

        self.jump_sound = arcade.load_sound(AUDIO_RESOURCES + "/jump1.wav")

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
        wall = arcade.Sprite(TILE_RESOURCES + "/grassLeft.png", TILE_SCALING)
        wall.center_x = 0
        wall.center_y = TILE_RADIUS
        self.wall_list.append(wall)
        for x in range(2 * TILE_RADIUS, 10 * 2 * TILE_RADIUS, 2 * TILE_RADIUS * TILE_SCALING):
            wall = arcade.Sprite(TILE_RESOURCES + "/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = TILE_RADIUS
            self.wall_list.append(wall)
        wall = arcade.Sprite(TILE_RESOURCES + "/grassRight.png", TILE_SCALING)
        wall.center_x = 10 * 2 * TILE_RADIUS
        wall.center_y = TILE_RADIUS
        self.wall_list.append(wall)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()

        # Draw our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.WHITE, 18)

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        self.player_list.update()
        self.player_list.update_animation()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
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
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = L1()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
