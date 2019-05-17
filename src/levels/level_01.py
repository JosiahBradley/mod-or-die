import BaseLevel


class L1(BaseLevel):
    def draw_map(self):
        super().draw_map()
        self.water_list = arcade.SpriteList()
        for x in range(-10 * TILE_RADIUS, 35 * TILE_RADIUS, 2 * TILE_RADIUS):
            wall = arcade.Sprite(TILE_RESOURCES + "/waterTop_low.png")
            wall.center_y = 0
            wall.center_x = x
            wall.start_x = x
            wall.waves = scale_generator(x=0, offset=0, step=0.02)
            self.water_list.append(wall)
            for y in range(2 * TILE_RADIUS, 6 * TILE_RADIUS, 2 * TILE_RADIUS):
                wall = arcade.Sprite(TILE_RESOURCES + "/water.png")
                wall.center_y = -y
                wall.center_x = x
                wall.start_x = x
                wall.waves = scale_generator(x=0, offset=0, step=0.02)
                self.water_list.append(wall)

    def update(self, delta_time):
        super().update(delta_time=delta_time)
        for water in self.water_list:
            water.center_x = water.start_x + next(water.waves) * TILE_RADIUS
            water.center_y += 0.1
        self.water_list.update()

        if self.player.top < self.water_list.__getitem__(0).top:
            self.game_over()

    def on_draw(self):
        super().on_draw()
        self.water_list.draw()


if __name__ == "__main__":
    def main():
        """ Main method """
        window = L0(speed=5.0, title="LEVEL 0 TEST")
        window.setup()
        arcade.run()

    main()