import arcade
from src.tools.funcs import rand_range, scale_generator
import math
from random import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1280
SCREEN_TITLE = "Spiral animation using sprite scaling"


class Spiral(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.sprite_list = None

        arcade.set_background_color(arcade.csscolor.AQUAMARINE)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Create the Sprite lists
        self.sprite_list = arcade.SpriteList()

        r = 60
        for x in rand_range(0, 100 * math.pi, scale=math.pi / 5):
            star = arcade.Sprite("../../resources/arcade/gold_1.png")
            star.center_x = SCREEN_WIDTH / 2 + r * math.cos(x)
            star.center_y = SCREEN_HEIGHT / 2 + r * math.sin(x)
            star.seed = scale_generator(x=random() * math.pi, offset=.5, step=.01)
            star.scale = next(star.seed)
            self.sprite_list.append(star)
            r += 3

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.sprite_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            pass  # change colors, rotate spiral

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        pass  # stop animation

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)

        for star in self.sprite_list:
            star.scale = next(star.seed) - 1
            star.center_x, star.center_y = arcade.draw_commands.rotate_point(
                star.center_x,
                star.center_y,
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                .1
            )

        self.sprite_list.update()


def main():
    """ Main method """
    window = Spiral()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
