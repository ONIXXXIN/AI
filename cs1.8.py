# simple_fps_ursina.py
# pip install ursina

from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import random

app = Ursina()

window.title = "Simple CS-like FPS (Ursina prototype)"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# -----------------------
# Настройки
# -----------------------
PLAYER_SPEED = 6
BULLET_RANGE = 100
FIRE_RATE = 0.18   # сек между выстрелами
ENEMY_COUNT = 6

# -----------------------
# Сцена / свет / пол
# -----------------------
ground = Entity(model='plane', scale=100, texture='white_cube', texture_scale=(50,50), collider='box')
ground.texture = 'grass'
ground.y = 0

DirectionalLight(y=2, rotation=(45, -45, 45), color=color.white)
AmbientLight(color=color.rgb(60,60,60))

# простые стены (кубы)
walls = []
def make_wall(pos, scale=(2,2,2), color=color.gray):
    e = Entity(model='cube', color=color, scale=scale, position=pos, collider='box')
    walls.append(e)
    return e

# рамка и несколько блоков
make_wall((0,1,-30),(80,4,2))
make_wall((0,1,30),(80,4,2))
make_wall((-40,1,0),(2,4,60))
make_wall((40,1,0),(2,4,60))
make_wall((0,1,0),(10,4,2))
make_wall((12,1,8),(6,4,2))
make_wall((-14,1,-8),(6,4,2))

# -----------------------
# Игрок
# -----------------------
player = FirstPersonController()
player.cursor.visible = False  # мы нарисуем свой прицел
player.speed = PLAYER_SPEED
player.gravity = 1
player.jump_height = 1.2

# простая камера-пушечка (визуал)
weapon = Entity(model='cube', parent=camera, position=(0.6,-0.5,1.2), scale=(0.2,0.2,1.2), color=color.dark_gray)
muzzle_flash = None

# HUD прицел
crosshair = Entity(parent=camera, model='quad', color=color.white, scale=0.008, position=(0, 0, 1.1))
crosshair.rotation_z = 45

# -----------------------
# Враги
# -----------------------
class Enemy(Entity):
    def __init__(self, pos=(0,0,0)):
        super().__init__(
            model='cube',
            color=color.color(0.95,0.4,0.6),
            scale=(1,1.8,1),
            position=pos,
            collider='box'
        )
        self.max_hp = 3
        self.hp = self.max_hp
        self.speed = 2.0
        self.last_hit = 0.0

    def update(self):
        # пропустить если мёртв
        if self.hp <= 0:
            return
        # простая ИИ: идти к игроку, избегая сильных столкновений
        dir_vec = (player.position - self.position)
        dir_vec.y = 0
        dist = dir_vec.length()
        if dist > 1.8:
            dir_vec = dir_vec.normalized()
            self.position += dir_vec * self.speed * time.dt
            # простая проверка на стены (откат)
            hits = [w for w in walls if self.intersects(w).hit]
            if hits:
                self.position -= dir_vec * self.speed * time.dt

    def take_damage(self, amount):
        self.hp -= amount
        self.last_hit = time.time()
        # краткий визуальный отклик
        self.animate_color(color.red, duration=0.12)
        if self.hp <= 0:
            # смерть: эффект
            explosion = Entity(model='sphere', scale=0.2, position=self.position, color=color.orange)
            explosion.animate_scale(2, duration=0.25, curve=curve.out_expo)
            destroy(self, delay=0.05)
            destroy(explosion, delay=0.4)

enemies = []

def spawn_enemies(n):
    for _ in range(n):
        # случайная позиция внутри рамки
        x = random.uniform(-30, 30)
        z = random.uniform(-20, 20)
        e = Enemy(pos=(x,1,z))
        enemies.append(e)

spawn_enemies(ENEMY_COUNT)

# -----------------------
# Оружие / стрельба (луч)
# -----------------------
last_fire = 0.0
ammo = 999

def shoot():
    global last_fire
    global muzzle_flash
    now = time.time()
    if now - last_fire < FIRE_RATE:
        return
    last_fire = now

    # визуальный "выстрел" - небольшая вспышка у дула
    if muzzle_flash:
        destroy(muzzle_flash)
    muzzle_flash = Entity(parent=camera, model='quad', color=color.yellow, scale=(0.08,0.08), position=(0.7,-0.45,0.9))
    destroy(muzzle_flash, delay=0.05)

    # raycast из камеры в направлении камеры.forward
    origin = camera.world_position
    direction = camera.forward
    hit_info = raycast(origin, direction, distance=BULLET_RANGE, ignore=[player, weapon])
    if hit_info.hit:
        # если попали в врага — найти ближайшего Entity в hit_info.entity
        ent = hit_info.entity
        if isinstance(ent, Enemy):
            ent.take_damage(1)
        else:
            # попали в стену/землю — можно сделать след пули
            p = Entity(model='cube', color=color.black, scale=0.05, position=hit_info.world_point)
            destroy(p, delay=2.0)

# -----------------------
# Обновление (глобальное)
# -----------------------
def update():
    # удаление врагов из списка когда уничтожены
    for e in list(enemies):
        if not e.enabled or e.hp <= 0:
            try:
                enemies.remove(e)
            except:
                pass

    # если все враги убиты — респавним
    if len(enemies) == 0:
        invoke(spawn_enemies, ENEMY_COUNT, delay=1)

# -----------------------
# Контролы мыши/клавиш
# -----------------------
def input(key):
    # ЛКМ — стрелять
    if key == 'left mouse down':
        shoot()
    # R — перезарядка (сбросить запас)
    if key == 'r':
        pass
    # ESC — выход из игры
    if key == 'escape':
        application.quit()

# -----------------------
# HUD (простая панель)
# -----------------------
def draw_ui():
    # очки здоровья (пока для примера суммируем hp врагов)
    hp_text = f"Enemies: {len([e for e in enemies if e.hp>0])}"
    draw_text(hp_text, 0.02 * window.width, 0.95 * window.height, color.white, 16, font='Vera')

# интегрируем draw_ui с Ursina
window.borderless = False
def input_wrapper(key):
    input(key)
window.input = input_wrapper

# подключаем рисование UI
def late_update():
    draw_ui()
# Ursina использует update() для логики и render автоматически;
# draw_ui мы вызываем из ui через schedule или просто rely on above draw_text each frame
# Вместо сложной интеграции просто оставим draw_text в update через invoke every frame:
def fixed_update():
    pass

app.run()
