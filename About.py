import arcade

# Размеры окна
SCREEN_TITLE = "My Arcade Game"
WIDTH_CUBE = 80
HEIGHT_CUBE = 80
ROW = 10
COLUMN = 10
SCREEN_WIDTH = WIDTH_CUBE * COLUMN
SCREEN_HEIGHT = HEIGHT_CUBE * ROW
class S1mple(arcade.Sprite):
    def __init__(self):
        super().__init__("img_1.png",0.15)
        self.center_x = 380
        self.center_y = 300

class Potujno(arcade.Sprite):
    def __init__(self):
        super().__init__("img.png", 0.25)
        self.center_x = 380
        self.center_y = 300
class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.Bplant = S1mple()
        self.Vorobushek = Potujno()



    def setup(self):
        """Вызывается один раз при старте или перезапуске"""
        pass

    def on_draw(self):
        """Отрисовка"""
        arcade.start_render()
        self.Bplant.draw()
        self.Vorobushek.draw()
        for y in range(10):
            for x in range(10):
                arcade.draw_rectangle_outline(50,50,WIDTH_CUBE,HEIGHT_CUBE,arcade.color.TIFFANY_BLUE,2)

    def on_update(self, delta_time):
        """Логика игры (60 раз в секунду)"""
        pass

    def on_key_press(self, key, modifiers):
        """Нажатие клавиш"""
        if key == arcade.key.D:
            self.Bplant.center_x += 25
        if key == arcade.key.A:
            self.Bplant.center_x -= 25
        if key == arcade.key.W:
            self.Bplant.center_y += 25
        if key == arcade.key.S:
            self.Bplant.center_y -= 25

    def on_key_release(self, key, modifiers):
        """Отпускание клавиш"""
        pass


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
