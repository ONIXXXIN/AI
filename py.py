import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "FREE bombardini guzini"


class Player(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__(r"C:\Users\vladt\OneDrive\Pictures\Снимки экрана\Снимок экрана 2025-12-10 145641.png", 1)   # ← здесь твой файл спрайта
        self.center_x = x
        self.center_y = y


class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.BLACK)

        # === Создаём игрока ===
        self.player = Player(400, 300)  # центр экрана

        # Если хочешь — можно положить в SpriteList
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        # Рисуем спрайта
        self.player_list.draw()

    def on_update(self, delta_time):
        # Обновление SpriteList (физика, анимации и т.д.)
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        # Пример такого управления:
        if key == arcade.key.W:
            self.player.change_y = 3
        if key == arcade.key.S:
            self.player.change_y = -3
        if key == arcade.key.A:
            self.player.change_x = -3
        if key == arcade.key.D:
            self.player.change_x = 3

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass


def main():
    Game()
    arcade.run()


if __name__ == "__main__":
    main()
