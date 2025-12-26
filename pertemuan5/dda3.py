import turtle
import math

# --- Setup Turtle ---
t = turtle.Turtle()
t.screen.setup(width=600, height=600)
t.speed(0) # Kecepatan tercepat
t.hideturtle()
t.penup()

# Fungsi Pembantu: Menggambar 'piksel'
def draw_pixel(x, y, color="black"):
    """Menggambar sebuah 'piksel' di koordinat integer (x, y)"""
    t.goto(x, y)
    t.dot(2, color)

# --- Algoritma Garis DDA (Dibutuhkan untuk Poligon) ---
def draw_line_dda(x1, y1, x2, y2, color="blue"):
    """Menggambar garis dari (x1, y1) ke (x2, y2) menggunakan algoritma DDA."""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x = x1
    y = y1
    draw_pixel(round(x), round(y), color)
    for _ in range(int(steps)):
        x += x_increment
        y += y_increment
        draw_pixel(round(x), round(y), color)

# --- Menggambar POLIGON menggunakan Algoritma Garis DDA ---
def draw_polygon(vertices, color="green"):
    """Menggambar poligon berdasarkan daftar titik sudut (vertices) menggunakan draw_line_dda."""
    num_vertices = len(vertices)
    if num_vertices < 2:
        return

    for i in range(num_vertices):
        # Titik awal segmen
        x1, y1 = vertices[i]
        # Titik akhir segmen (sambungkan ke titik berikutnya, atau ke titik awal jika sudah segmen terakhir)
        x2, y2 = vertices[(i + 1) % num_vertices]

        draw_line_dda(x1, y1, x2, y2, color)

# --- Contoh Penggunaan Poligon ---
print("Menggambar Poligon (Segitiga) menggunakan DDA...")
triangle_vertices = [
    (-200, -100),
    (-100, 50),
    (-300, 50)
]
draw_polygon(triangle_vertices, "green")

print("Menggambar Poligon (Persegi Lima) menggunakan DDA...")
pentagon_vertices = [
    (100, 150),
    (200, 180),
    (230, 80),
    (170, 0),
    (70, 30)
]
draw_polygon(pentagon_vertices, "teal")

turtle.done()