import arcade
from .BaseLevel import BaseLevel
from ..tools.funcs import scale_generator


class L1(BaseLevel):
    def __init__(self, speed, title):
        super().__init__(speed=speed, title=title)
        self.water_list = None
        self.exit = None

    def draw_map(self):
        super().draw_map()
        self.assets["water"] = arcade.SpriteList()
        for x in range(-10 * self.conf.TILE_RADIUS, 250 * self.conf.TILE_RADIUS, 2 * self.conf.TILE_RADIUS):
            wall = self.tile_sprite("waterTop_low")
            wall.center_y = 0
            wall.center_x = x
            wall.start_x = x
            wall.waves = scale_generator(x=0, offset=0, step=0.02)
            self.assets["water"].append(wall)
            for y in range(2 * self.conf.TILE_RADIUS, 6 * self.conf.TILE_RADIUS, 2 * self.conf.TILE_RADIUS):
                wall = self.tile_sprite('water')
                wall.center_y = -y
                wall.center_x = x
                wall.start_x = x
                wall.waves = scale_generator(x=0, offset=0, step=0.02)
                self.assets["water"].append(wall)
        door = self.tile_sprite('signExit')
        door.center_x = 100 * self.conf.TILE_RADIUS
        # door.center_x = 10 * self.conf.TILE_RADIUS
        door.center_y = 185
        self.assets["statics"].append(door)
        self.exit = door

    def update(self, delta_time):
        super().update(delta_time=delta_time)
        if self.is_game_over:
            return

        for water in self.assets["water"]:
            water.center_x = water.start_x + next(water.waves) * self.conf.TILE_RADIUS
            water.center_y += 0.18

        if self.player.top < self.assets["water"].__getitem__(0).top:
            self.game_over()

        if self.player.center_x > self.exit.center_x:
            self.win()

    def on_draw(self):
        super().on_draw()
        if self.is_game_over:
            arcade.draw_text(
                "YOU WIN",
                self.view_left + self.get_size()[0] * .5,
                self.view_bottom + self.get_size()[1] * .5,
                arcade.csscolor.ORANGE_RED, 32
            )

    def win(self):
        super().win()
        self.audio("gameover1")
        self.score = 1000


def main():
    """ Main method """
    window = L1(speed=5.0, title="LEVEL 1: RUN")
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
