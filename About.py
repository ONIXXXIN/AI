import arcade

# Размеры окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Здесь будут переменные игры
        # пример:
        # self.player = None

    def setup(self):
        """Вызывается один раз при старте или перезапуске"""
        pass

    def on_draw(self):
        """Отрисовка"""
        arcade.start_render()
        # Рисовать здесь
        pass

    def on_update(self, delta_time):
        """Логика игры (60 раз в секунду)"""
        pass

    def on_key_press(self, key, modifiers):
        """Нажатие клавиш"""
        pass

    def on_key_release(self, key, modifiers):
        """Отпускание клавиш"""
        pass


def main():
    game = Game()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
