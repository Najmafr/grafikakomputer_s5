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

# --- ALGORITMA LINGKARAN: Midpoint Circle Algorithm ---
def draw_circle_midpoint(xc, yc, r, color="red"):
    """Menggambar lingkaran dengan pusat (xc, yc) dan radius r menggunakan Midpoint Circle Algorithm."""
    x = 0
    y = r
    # Parameter keputusan awal
    p = 1 - r # Menggunakan 1 - r untuk integer

    # Fungsi simetri 8 arah (octant)
    def plot_circle_points(cx, cy, px, py, c):
        draw_pixel(cx + px, cy + py, c)
        draw_pixel(cx - px, cy + py, c)
        draw_pixel(cx + px, cy - py, c)
        draw_pixel(cx - px, cy - py, c)
        draw_pixel(cx + py, cy + px, c)
        draw_pixel(cx - py, cy + px, c)
        draw_pixel(cx + py, cy - px, c)
        draw_pixel(cx - py, cy - px, c)

    # Plot titik awal
    plot_circle_points(xc, yc, x, y, color)

    while x < y:
        x += 1
        if p < 0:
            # Titik berikutnya di (x+1, y)
            p = p + 2 * x + 1
        else:
            # Titik berikutnya di (x+1, y-1)
            y -= 1
            p = p + 2 * x + 1 - 2 * y

        plot_circle_points(xc, yc, x, y, color)

# --- Contoh Penggunaan Lingkaran ---
print("Menggambar Lingkaran menggunakan Midpoint Circle...")
# Pusat (0, 0), Radius 100
draw_circle_midpoint(0, 0, 100, "red") 
# Pusat (150, 150), Radius 50
draw_circle_midpoint(150, 150, 50, "brown")

turtle.done()