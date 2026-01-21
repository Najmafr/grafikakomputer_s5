import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# =============================
# FUNGSI GAMBAR KUBUS
# =============================
def draw_cube(ax, points, color):
    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    for edge in edges:
        ax.plot(
            [points[edge[0]][0], points[edge[1]][0]],
            [points[edge[0]][1], points[edge[1]][1]],
            [points[edge[0]][2], points[edge[1]][2]],
            color=color
        )

# =============================
# KUBUS AWAL
# =============================
cube = np.array([
    [-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],
    [-1,-1, 1],[1,-1, 1],[1,1, 1],[-1,1, 1]
])

# =============================
# FIGURE
# =============================
fig = plt.figure(figsize=(8,8))
ax = fig.add_subplot(111, projection='3d')

# =============================
# VARIABEL ANIMASI
# =============================
angle = 0
tx = 0
scale = 1
direction = 1  # untuk refleksi

# =============================
# UPDATE FRAME
# =============================
def update(frame):
    global angle, tx, scale, direction

    ax.cla()

    # ===== SKALA 3D =====
    scale += 0.01 * direction
    if scale > 1.5 or scale < 0.7:
        direction *= -1   # refleksi skala

    S = np.array([
        [scale,0,0],
        [0,scale,0],
        [0,0,scale]
    ])

    # ===== ROTASI 3D (Z) =====
    angle += 2
    theta = np.radians(angle)
    R = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta),  np.cos(theta), 0],
        [0,0,1]
    ])

    # ===== TRANSLASI 3D =====
    tx += 0.05 * direction
    if abs(tx) > 3:
        direction *= -1   # refleksi translasi

    T = np.array([tx, 0, 0])

    # ===== TRANSFORMASI TOTAL =====
    transformed = cube @ S @ R + T

    # ===== GAMBAR =====
    draw_cube(ax, transformed, 'blue')

    ax.set_xlim(-5,5)
    ax.set_ylim(-5,5)
    ax.set_zlim(-5,5)
    ax.set_title("Animasi Transformasi 3D\nTranslasi • Rotasi • Skala • Refleksi")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

# =============================
# JALANKAN ANIMASI
# =============================
ani = FuncAnimation(fig, update, frames=300, interval=50)
plt.show()
