import turtle
import math

def draw_points(points, scale=20):
    """Menggambar titik-titik pada koordinat yang diberikan"""
    turtle.speed(0)
    turtle.penup()
    turtle.hideturtle()
    
    for x, y in points:
        turtle.goto(x * scale, y * scale)
        turtle.dot(5, "black")
    
    turtle.done()

def midpoint_circle(r):
    """Algoritma Midpoint Circle untuk menghasilkan titik-titik lingkaran"""
    points = []
    x = 0
    y = r
    d = 1 - r
    
    # Fungsi untuk menambahkan 8 titik simetris
    def add_circle_points(x, y):
        points.extend([
            (x, y),
            (-x, y),
            (x, -y),
            (-x, -y),
            (y, x),
            (-y, x),
            (y, -x),
            (-y, -x)
        ])
    
    add_circle_points(x, y)
    
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y = y - 1
        x = x + 1
        add_circle_points(x, y)
    
    return points

# Setup window
turtle.title("Algoritma Gambar Lingkaran")
turtle.setup(width=600, height=600)

# Menggunakan algoritma Midpoint Circle dengan radius 6
r = 6
points = midpoint_circle(r)

# Menggambar titik-titik
draw_points(points)