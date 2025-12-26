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

# --- ALGORITMA GARIS: Digital Differential Analyzer (DDA) ---
def draw_line_dda(x1, y1, x2, y2, color="blue"):
    """Menggambar garis dari (x1, y1) ke (x2, y2) menggunakan algoritma DDA."""
    dx = x2 - x1
    dy = y2 - y1

    # Tentukan jumlah langkah
    steps = max(abs(dx), abs(dy))

    # Tentukan inkremen untuk x dan y
    x_increment = dx / steps
    y_increment = dy / steps

    # Mulai dari titik awal
    x = x1
    y = y1

    draw_pixel(round(x), round(y), color) # Gambar piksel awal

    for _ in range(int(steps)):
        x += x_increment
        y += y_increment
        draw_pixel(round(x), round(y), color)

# --- Contoh Penggunaan Garis ---
print("Menggambar Garis menggunakan DDA...")
draw_line_dda(-250, 20, 250, 20, "purple") # Garis horizontal
draw_line_dda(100, -150, -150, 100, "orange") # Garis diagonal

turtle.done()