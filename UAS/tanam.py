from ursina import *
import random

app = Ursina()

# Konfigurasi Window
window.title = "Greenhouse Tycoon 3D"
window.borderless = False
window.color = color.black
Sky(texture='sky_sunset')

# Variabel Game
score = 0
score_text = Text(text=f'Tanaman: {score}', position=(-0.85, 0.45), scale=2, color=color.yellow)

# ==========================================
# 1. LINGKUNGAN (Representasi 3D & Kedalaman)
# ==========================================
floor = Entity(model='plane', scale=40, texture='grass', texture_scale=(4,4), collider='box')

# Rangka Greenhouse (Poligon & Transformasi)
for i in range(-20, 21, 10):
    Entity(model='cube', scale=(0.5, 12, 0.5), position=(i, 6, 20), color=color.dark_gray)
    Entity(model='cube', scale=(0.5, 12, 0.5), position=(i, 6, -20), color=color.dark_gray)
    # Atap Lengkung (Rotasi & Skala)
    Entity(model='cube', scale=(40, 0.2, 0.5), position=(0, 12, i), color=color.light_gray)

# ==========================================
# 2. SISTEM TANAMAN INTERAKTIF
# ==========================================
class Pot(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            model='cube',
            scale=(2, 0.8, 2),
            position=position,
            color=color.brown,
            highlight_color=color.orange # Feedback saat mouse lewat
        )
        self.has_plant = False
        self.plant = None
        self.growth_speed = random.uniform(0.1, 0.3)

    def on_click(self):
        if not self.has_plant:
            # Buat tanaman baru (Translasi & Skala Awal)
            self.plant = Entity(
                model='sphere', 
                scale=0.1, 
                position=(self.x, 0.5, self.z), 
                color=color.green,
                parent=scene
            )
            self.has_plant = True
            global score
            score += 1
            score_text.text = f'Tanaman: {score}'
            audio_click = Audio('cursor_click', loop=False, autoplay=True)

    def update(self):
        # Logika Pertumbuhan (Transformasi Skala Dinamis)
        if self.has_plant and self.plant.scale_x < 1.8:
            self.plant.scale += Vec3(1, 1, 1) * self.growth_speed * time.dt
            self.plant.y += self.growth_speed * 0.5 * time.dt
            
            # Perubahan Warna saat tumbuh (Ilusi Kematangan)
            if self.plant.scale_x > 1.2:
                self.plant.color = color.lime

# Generate Pot secara otomatis
pots = []
for x in range(-16, 17, 8):
    for z in range(-16, 17, 8):
        pots.append(Pot(position=(x, 0.4, z)))

# ==========================================
# 3. AKTOR & KONTROL KAMERA (Viewing & Proyeksi)
# ==========================================
player = Entity(model='cube', color=color.azure, scale=(1, 2, 1), position=(0, 1, 0), origin_y=-0.5, collider='box')
head = Entity(parent=player, model='sphere', scale=0.6, y=1.2, color=color.peach)

# Menggunakan SmoothFollow untuk kamera yang lebih sinematik
camera.position = (0, 15, -20)
camera.rotation_x = 35

def update():
    # Pergerakan Karakter
    move_speed = 10 * time.dt
    direction = Vec3(
        (held_keys['d'] - held_keys['a']),
        0,
        (held_keys['w'] - held_keys['s'])
    ).normalized()
    
    player.position += direction * move_speed
    
    # Rotasi Karakter menghadap arah jalan
    if direction != Vec3(0,0,0):
        player.look_at(player.position + direction)
        player.rotation_x = 0 # Mengunci agar tidak miring ke bawah

    # Kamera mengikuti player secara halus
    camera.x = lerp(camera.x, player.x, 2 * time.dt)
    camera.z = lerp(camera.z, player.z - 15, 2 * time.dt)

    # Zoom dengan Mouse Wheel
    if held_keys['scroll up']: camera.fov -= 2
    if held_keys['scroll down']: camera.fov += 2

# Instruksi UI
info = Text(
    text='KLIK POT UNTUK MENANAM | WASD: JALAN | MOUSE: ZOOM',
    origin=(0, -18),
    color=color.white,
    background=True
)

# Cahaya Dasar
sun = DirectionalLight(y=10, rotation=(45, 45, 0))

app.run()
