from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Pengaturan kamera dan langit
sky = Sky(texture='sky_sunset')
camera.position = (0, 20, -30)
camera.rotation_x = 30

# Ground/Base
ground = Entity(
    model='plane',
    scale=(50, 1, 50),
    texture='grass',
    color=color.rgb(100, 200, 100),
    collider='box'
)

# Kelas untuk membuat tile papan
class BoardTile(Entity):
    def __init__(self, position, tile_number, **kwargs):
        super().__init__(
            model='cube',
            position=position,
            scale=(1.8, 0.3, 1.8),
            color=color.random_color(),
            collider='box',
            **kwargs
        )
        self.tile_number = tile_number
        
        # Label nomor tile
        self.label = Text(
            text=str(tile_number),
            position=self.position + Vec3(0, 0.2, 0),
            scale=2,
            origin=(0, 0),
            color=color.black
        )

# Kelas untuk Tangga
class Ladder(Entity):
    def __init__(self, start_pos, end_pos, **kwargs):
        super().__init__(
            model='cube',
            **kwargs
        )
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # Buat tangga dengan multiple rungs
        mid_point = (start_pos + end_pos) / 2
        direction = end_pos - start_pos
        distance = direction.length()
        
        # Side rails
        for offset in [-0.2, 0.2]:
            rail = Entity(
                model='cube',
                position=mid_point + Vec3(offset, 0, 0),
                scale=(0.1, distance, 0.1),
                color=color.rgb(139, 69, 19),
                rotation=Vec3(0, 0, 90)
            )
            rail.look_at(end_pos, up=Vec3(0, 1, 0))
        
        # Rungs
        steps = int(distance / 1.5) + 1
        for i in range(steps):
            t = i / max(steps - 1, 1)
            rung_pos = lerp(start_pos, end_pos, t)
            Entity(
                model='cube',
                position=rung_pos,
                scale=(0.5, 0.1, 0.1),
                color=color.rgb(160, 82, 45),
                rotation=Vec3(0, 0, 0)
            )

# Kelas untuk Ular
class Snake(Entity):
    def __init__(self, start_pos, end_pos, **kwargs):
        super().__init__(
            **kwargs
        )
        self.start_pos = start_pos
        self.end_pos = end_pos
        
        # Buat badan ular dengan kurva
        segments = 15
        for i in range(segments):
            t = i / segments
            # Kurva sinusoidal untuk efek ular
            curve_offset = sin(t * 4 * pi) * 0.5
            pos = lerp(start_pos, end_pos, t)
            pos += Vec3(curve_offset, 0, 0)
            
            # Segment ular
            segment = Entity(
                model='sphere',
                position=pos,
                scale=0.4 - (t * 0.1),
                color=color.rgb(34, 139, 34) if i % 2 == 0 else color.rgb(0, 100, 0)
            )
        
        # Kepala ular
        head = Entity(
            model='sphere',
            position=end_pos,
            scale=0.5,
            color=color.rgb(255, 0, 0)
        )
        
        # Mata ular
        for offset in [-0.15, 0.15]:
            Entity(
                model='sphere',
                position=end_pos + Vec3(offset, 0.2, 0.3),
                scale=0.1,
                color=color.yellow
            )

# Kelas untuk Pemain
class Player(Entity):
    def __init__(self, position, player_color, **kwargs):
        super().__init__(
            model='sphere',
            position=position,
            scale=0.5,
            color=player_color,
            **kwargs
        )
        self.current_tile = 0
        self.target_tile = 0

# Kelas untuk Dadu
class Dice(Entity):
    def __init__(self, **kwargs):
        super().__init__(
            model='cube',
            position=(5, 2, -5),
            scale=1,
            color=color.white,
            **kwargs
        )
        self.current_value = 1
        self.is_rolling = False
        
    def roll(self):
        if not self.is_rolling:
            self.is_rolling = True
            self.current_value = random.randint(1, 6)
            
            # Animasi rotasi dadu
            self.animate_rotation(
                Vec3(random.randint(0, 360), random.randint(0, 360), random.randint(0, 360)),
                duration=0.5,
                curve=curve.out_bounce
            )
            
            invoke(self.finish_roll, delay=0.5)
            return self.current_value
    
    def finish_roll(self):
        self.is_rolling = False

# Buat papan monopoli dengan path melingkar
tiles = []
tile_positions = []

# Buat path papan (kotak melingkar)
board_size = 10  # 10x10 tiles
tile_spacing = 2

# Bottom row (kiri ke kanan)
for i in range(board_size):
    pos = Vec3(-board_size + i * tile_spacing, 0.5, -board_size)
    tile_positions.append(pos)

# Right column (bawah ke atas)
for i in range(1, board_size):
    pos = Vec3(board_size - tile_spacing, 0.5, -board_size + i * tile_spacing)
    tile_positions.append(pos)

# Top row (kanan ke kiri)
for i in range(1, board_size):
    pos = Vec3(board_size - tile_spacing - i * tile_spacing, 0.5, board_size - tile_spacing)
    tile_positions.append(pos)

# Left column (atas ke bawah)
for i in range(1, board_size - 1):
    pos = Vec3(-board_size, 0.5, board_size - tile_spacing - i * tile_spacing)
    tile_positions.append(pos)

# Buat tiles
for i, pos in enumerate(tile_positions):
    tile = BoardTile(pos, i + 1)
    tiles.append(tile)

# Tambahkan rintangan dekoratif
# Trees
for _ in range(8):
    tree_pos = Vec3(
        random.uniform(-12, 12),
        0,
        random.uniform(-12, 12)
    )
    # Batang
    Entity(
        model='cylinder',
        position=tree_pos,
        scale=(0.5, 3, 0.5),
        color=color.rgb(101, 67, 33)
    )
    # Daun
    Entity(
        model='sphere',
        position=tree_pos + Vec3(0, 3, 0),
        scale=2,
        color=color.rgb(34, 139, 34)
    )

# Rocks/Obstacles
for _ in range(10):
    rock_pos = Vec3(
        random.uniform(-13, 13),
        0.3,
        random.uniform(-13, 13)
    )
    Entity(
        model='sphere',
        position=rock_pos,
        scale=(random.uniform(0.5, 1), random.uniform(0.3, 0.6), random.uniform(0.5, 1)),
        color=color.rgb(128, 128, 128)
    )

# Tambahkan tangga dan ular
# Tangga (naik)
ladders_data = [
    (5, 15),
    (12, 22),
    (18, 28),
    (25, 33)
]

for start, end in ladders_data:
    if start < len(tile_positions) and end < len(tile_positions):
        Ladder(tile_positions[start] + Vec3(0, 0.5, 0), 
               tile_positions[end] + Vec3(0, 0.5, 0))

# Ular (turun)
snakes_data = [
    (16, 6),
    (24, 10),
    (30, 14),
    (35, 20)
]

for start, end in snakes_data:
    if start < len(tile_positions) and end < len(tile_positions):
        Snake(tile_positions[start] + Vec3(0, 0.5, 0), 
              tile_positions[end] + Vec3(0, 0.5, 0))

# Buat pemain
player = Player(
    tile_positions[0] + Vec3(0, 1, 0),
    color.rgb(255, 100, 100)
)

# Buat dadu
dice = Dice()

# UI
dice_button = Button(
    text='Roll Dice',
    color=color.azure,
    scale=(0.2, 0.1),
    position=(-0.7, 0.4),
    on_click=lambda: roll_and_move()
)

info_text = Text(
    text='Press Roll Dice to start!',
    position=(-0.85, 0.35),
    scale=1.5,
    origin=(0, 0),
    background=True
)

timer_text = Text(
    text='Time: 00:00',
    position=(0.6, 0.45),
    scale=1.5,
    origin=(0, 0),
    background=True
)

# Pause button
pause_button = Button(
    text='||',
    color=color.rgb(255, 100, 100),
    scale=(0.08, 0.08),
    position=(-0.85, 0.45),
    on_click=lambda: toggle_pause()
)

# Variables
game_time = 0
is_paused = False
is_moving = False

def roll_and_move():
    global is_moving
    if not is_moving and not is_paused:
        roll = dice.roll()
        info_text.text = f'Rolled: {roll}'
        
        # Hitung tile tujuan
        target = min(player.current_tile + roll, len(tile_positions) - 1)
        
        invoke(lambda: move_player(target), delay=0.6)

def move_player(target_tile):
    global is_moving
    is_moving = True
    
    # Animasi bergerak
    steps = abs(target_tile - player.current_tile)
    for i in range(steps):
        next_tile = player.current_tile + 1
        invoke(lambda t=next_tile: move_to_tile(t), delay=i * 0.3)
    
    invoke(lambda: check_special_tile(target_tile), delay=steps * 0.3 + 0.1)

def move_to_tile(tile_num):
    player.current_tile = tile_num
    target_pos = tile_positions[tile_num] + Vec3(0, 1, 0)
    player.animate_position(target_pos, duration=0.2, curve=curve.out_cubic)

def check_special_tile(tile_num):
    global is_moving
    
    # Cek tangga
    for start, end in ladders_data:
        if tile_num == start:
            info_text.text = f'Ladder! Going up to {end + 1}'
            invoke(lambda: move_to_tile(end), delay=0.5)
            tile_num = end
            break
    
    # Cek ular
    for start, end in snakes_data:
        if tile_num == start:
            info_text.text = f'Snake! Going down to {end + 1}'
            invoke(lambda: move_to_tile(end), delay=0.5)
            tile_num = end
            break
    
    # Cek menang
    if tile_num >= len(tile_positions) - 1:
        info_text.text = 'YOU WIN!'
        dice_button.enabled = False
    
    is_moving = False

def toggle_pause():
    global is_paused
    is_paused = not is_paused
    pause_button.text = '▶' if is_paused else '||'
    info_text.text = 'PAUSED' if is_paused else 'Playing...'

def update():
    global game_time
    if not is_paused:
        game_time += time.dt
        minutes = int(game_time // 60)
        seconds = int(game_time % 60)
        timer_text.text = f'Time: {minutes:02d}:{seconds:02d}'
    
    # Rotasi dadu saat idle
    if not dice.is_rolling:
        dice.rotation_y += time.dt * 20

# Lighting
DirectionalLight(y=2, z=3, shadows=True)
AmbientLight(color=color.rgba(100, 100, 100, 0.3))

app.run()