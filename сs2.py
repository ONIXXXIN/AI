from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# -------------------------------
# Карта "похожа на Dust2 / Mirage"
# -------------------------------

level = [
    "####################",
    "#..................#",
    "#..####....####....#",
    "#..................#",
    "#..####....####....#",
    "#..................#",
    "####################",
]

# Стена
for z, row in enumerate(level):
    for x, block in enumerate(row):
        if block == "#":
            Entity(
                model="cube",
                color=color.gray,
                collider="box",
                scale=(1, 2, 1),
                position=(x, 1, z)
            )

# -------------------------------
# Игрок
# -------------------------------
player = FirstPersonController(
    position=(2, 2, 2),
    speed=5
)

# -------------------------------
# Оружие (модель от третьего лица)
# -------------------------------
gun = Entity(
    parent=camera.ui,
    model="cube",
    scale=(0.3, 0.2, 1),
    position=(0.4, -0.3, 1),
    color=color.black
)

# -------------------------------
# Стрельба
# -------------------------------
bullets = []

def input(key):
    if key == "left mouse down":
        shoot()

def shoot():
    bullet = Entity(
        model="sphere",
        color=color.yellow,
        scale=0.1,
        position=player.position + player.forward * 1.5
    )
    bullets.append(bullet)

def update():
    for b in bullets:
        b.position += b.forward * 0.7
        hit_info = b.intersects()
        if hit_info.hit:
            destroy(b)
            bullets.remove(b)

# -------------------------------
# Свет и небо
# -------------------------------
DirectionalLight()
Sky()

app.run()
