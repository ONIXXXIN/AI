# simple_cs_style.py
# pip install arcade
import arcade
import math
import random
from typing import Tuple

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Simple CS-like Shooter (singleplayer educational)"

PLAYER_SPEED = 300         # пикселей/сек
BULLET_SPEED = 800
BULLET_LIFETIME = 1.2      # секунды
ENEMY_SPEED = 120
ENEMY_SPAWN_INTERVAL = 3.0 # секунд

# --- Утилиты ---
def vec_from_to(a: Tuple[float,float], b: Tuple[float,float]) -> Tuple[float,float]:
    dx = b[0] - a[0]
    dy = b[1] - a[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return 0.0, 0.0
    return dx / dist, dy / dist

# --- Игровые объекты ---
class Bullet(arcade.SpriteSolidColor):
    def __init__(self, width, height, color, pos, velocity):
        super().__init__(width, height, color)
        self.center_x, self.center_y = pos
        self.change_x, self.change_y = velocity
        self.spawn_time = 0.0  # будет установлено при добавлении в мир

class SimpleEnemy(arcade.SpriteSolidColor):
    def __init__(self, size, color, pos):
        super().__init__(size, size, color)
        self.center_x, self.center_y = pos
        self.health = 1

class Player(arcade.SpriteSolidColor):
    def __init__(self, w=28, h=28, color=arcade.color.BLUE, pos=(100,100)):
        super().__init__(w, h, color)
        self.center_x, self.center_y = pos
        self.speed = PLAYER_SPEED
        self.health = 5
        # движение по осям
        self.move_x = 0
        self.move_y = 0

# --- Окно игры (OOP) ---
class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        # Списки спрайтов
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # Игрок
        self.player = Player()
        self.player_list.append(self.player)

        # Прицел (положение мыши)
        self.aim_x = SCREEN_WIDTH // 2
        self.aim_y = SCREEN_HEIGHT // 2

        # Таймеры
        self.total_time = 0.0
        self.time_since_enemy = 0.0

        # UI / счёт
        self.score = 0

        # Настройка карты (простые стены)
        self._create_walls()

    def _create_walls(self):
        # Простейшая карта: рамка + несколько внутренних блоков
        thickness = 32
        # рамка
        wall_color = arcade.color.DARK_BROWN
        walls = [
            (SCREEN_WIDTH/2, thickness/2, SCREEN_WIDTH, thickness),                # bottom
            (SCREEN_WIDTH/2, SCREEN_HEIGHT - thickness/2, SCREEN_WIDTH, thickness),# top
            (thickness/2, SCREEN_HEIGHT/2, thickness, SCREEN_HEIGHT),             # left
            (SCREEN_WIDTH - thickness/2, SCREEN_HEIGHT/2, thickness, SCREEN_HEIGHT) # right
        ]
        # внутренняя преграда
        walls += [
            (SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 300, 40),
            (SCREEN_WIDTH/2 - 200, SCREEN_HEIGHT/2 + 120, 200, 40),
            (SCREEN_WIDTH/2 + 200, SCREEN_HEIGHT/2 - 120, 200, 40)
        ]
        for (cx, cy, w, h) in walls:
            spr = arcade.SpriteSolidColor(int(w), int(h), wall_color)
            spr.center_x = cx
            spr.center_y = cy
            self.wall_list.append(spr)

    # -----------------------
    # Рисование
    # -----------------------
    def on_draw(self):
        arcade.start_render()
        # рисуем мир
        self.wall_list.draw()
        self.enemy_list.draw()
        self.player_list.draw()
        self.bullet_list.draw()

        # прицел
        arcade.draw_circle_outline(self.aim_x, self.aim_y, 12, arcade.color.WHITE, 2)
        arcade.draw_circle_outline(self.aim_x, self.aim_y, 4, arcade.color.WHITE, 2)

        # HUD
        arcade.draw_text(f"HP: {self.player.health}", 16, SCREEN_HEIGHT - 28, arcade.color.WHITE, 18)
        arcade.draw_text(f"Score: {self.score}", 140, SCREEN_HEIGHT - 28, arcade.color.WHITE, 18)
        arcade.draw_text(f"Time: {int(self.total_time)}s", 280, SCREEN_HEIGHT - 28, arcade.color.WHITE, 18)

    # -----------------------
    # Обновление логики
    # -----------------------
    def on_update(self, delta_time: float):
        # таймеры
        self.total_time += delta_time
        self.time_since_enemy += delta_time

        # спавн врагов периодически
        if self.time_since_enemy >= ENEMY_SPAWN_INTERVAL:
            self._spawn_enemy()
            self.time_since_enemy = 0.0

        # Движение игрока (нормализуем диагонали)
        dx = self.player.move_x
        dy = self.player.move_y
        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            nx, ny = dx / length, dy / length
            self.player.center_x += nx * self.player.speed * delta_time
            self.player.center_y += ny * self.player.speed * delta_time

            # коллизия с стенами — простой откат
            walls_hit = arcade.check_for_collision_with_list(self.player, self.wall_list)
            if walls_hit:
                # простейшая реакция: сдвинуть назад на пройденный шаг
                self.player.center_x -= nx * self.player.speed * delta_time
                self.player.center_y -= ny * self.player.speed * delta_time

        # Обновляем пули
        for bullet in list(self.bullet_list):
            # перемещение
            bullet.center_x += bullet.change_x * delta_time
            bullet.center_y += bullet.change_y * delta_time

            # время жизни
            if self.total_time - bullet.spawn_time > BULLET_LIFETIME:
                bullet.remove_from_sprite_lists()
                continue

            # проверка по стенам
            hit_walls = arcade.check_for_collision_with_list(bullet, self.wall_list)
            if hit_walls:
                bullet.remove_from_sprite_lists()
                continue

            # проверка по врагам
            hit_enemies = arcade.check_for_collision_with_list(bullet, self.enemy_list)
            if hit_enemies:
                for e in hit_enemies:
                    e.health -= 1
                    if e.health <= 0:
                        e.remove_from_sprite_lists()
                        self.score += 100
                bullet.remove_from_sprite_lists()
                continue

        # Враги: простая ИИ — двигаться к игроку
        for enemy in list(self.enemy_list):
            vec = vec_from_to((enemy.center_x, enemy.center_y), (self.player.center_x, self.player.center_y))
            enemy.center_x += vec[0] * ENEMY_SPEED * delta_time
            enemy.center_y += vec[1] * ENEMY_SPEED * delta_time

            # коллизии врагов со стенами: откат
            if arcade.check_for_collision_with_list(enemy, self.wall_list):
                enemy.center_x -= vec[0] * ENEMY_SPEED * delta_time
                enemy.center_y -= vec[1] * ENEMY_SPEED * delta_time

            # соприкосновение с игроком — наносим урон и отталкиваем
            if arcade.check_for_collision(enemy, self.player):
                self.player.health -= 1
                # отталкиваем врага немного назад, чтобы не застрять
                enemy.center_x -= vec[0] * 20
                enemy.center_y -= vec[1] * 20
                if self.player.health <= 0:
                    self._on_player_dead()

    def _on_player_dead(self):
        # простой рестарт: очищаем врагов и буллеты, восстановлен игрока
        self.enemy_list.clear()
        self.bullet_list.clear()
        self.player.center_x, self.player.center_y = 120, 120
        self.player.health = 5
        self.score = 0
        self.total_time = 0.0
        self.time_since_enemy = 0.0

    def _spawn_enemy(self):
        # спавним врага у случайной стены (вне центра)
        margin = 80
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            x = random.uniform(margin, SCREEN_WIDTH - margin)
            y = SCREEN_HEIGHT - 50
        elif side == "bottom":
            x = random.uniform(margin, SCREEN_WIDTH - margin)
            y = 50
        elif side == "left":
            x = 50
            y = random.uniform(margin, SCREEN_HEIGHT - margin)
        else:
            x = SCREEN_WIDTH - 50
            y = random.uniform(margin, SCREEN_HEIGHT - margin)

        e = SimpleEnemy(26, arcade.color.RED, (x, y))
        self.enemy_list.append(e)

    # -----------------------
    # Ввод: клавиши
    # -----------------------
    def on_key_press(self, key, modifiers):
        # WASD или стрелки
        if key == arcade.key.W or key == arcade.key.UP:
            self.player.move_y = 1
        elif key == arcade.key.S or key == arcade.key.DOWN:
            self.player.move_y = -1
        if key == arcade.key.A or key == arcade.key.LEFT:
            self.player.move_x = -1
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            self.player.move_x = 1

        # пример: R — рестарт
        if key == arcade.key.R:
            self._on_player_dead()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W or key == arcade.key.UP:
            if self.player.move_y == 1:
                self.player.move_y = 0
        elif key == arcade.key.S or key == arcade.key.DOWN:
            if self.player.move_y == -1:
                self.player.move_y = 0
        if key == arcade.key.A or key == arcade.key.LEFT:
            if self.player.move_x == -1:
                self.player.move_x = 0
        elif key == arcade.key.D or key == arcade.key.RIGHT:
            if self.player.move_x == 1:
                self.player.move_x = 0

    # -----------------------
    # Мышь
    # -----------------------
    def on_mouse_motion(self, x, y, dx, dy):
        self.aim_x = x
        self.aim_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        # левая кнопка — стрелять
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.shoot_bullet((x, y))

    def on_mouse_release(self, x, y, button, modifiers):
        pass

    def shoot_bullet(self, target_pos):
        # создаём пулю от позиции игрока в сторону прицела
        px, py = self.player.center_x, self.player.center_y
        dir_x, dir_y = vec_from_to((px, py), target_pos)
        vx = dir_x * BULLET_SPEED
        vy = dir_y * BULLET_SPEED
        b = Bullet(6, 6, arcade.color.YELLOW_ORANGE, (px + dir_x*20, py + dir_y*20), (vx, vy))
        b.spawn_time = self.total_time
        self.bullet_list.append(b)

# ------------------------------
# Запуск
# ------------------------------
def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
